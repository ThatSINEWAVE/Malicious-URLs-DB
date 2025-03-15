import discord
from discord import app_commands
from discord.ext import commands
import re
import pandas as pd
import os
import asyncio
import datetime
import json
from dotenv import load_dotenv

# Load the .env file with the correct path
load_dotenv("../.env")

# Retrieve both the bot token and client ID from the .env file
TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")  # Now getting Client ID from .env file

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Add message content intent for reading message content


# Create the bot
class MessageCollectorBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.logging_channels = {}  # Store channels for logging by guild_id

    async def setup_hook(self):
        # Sync commands with Discord
        await self.tree.sync()
        print("Commands synced!")


bot = MessageCollectorBot()

# File to save progress state
PROGRESS_FILE = "scan_progress.json"

# Default scan settings
DEFAULT_BATCH_SIZE = 100
DEFAULT_COOLDOWN = 10  # seconds


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Generate invite URL with proper permissions, now using CLIENT_ID from .env
    invite_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=66560&scope=bot%20applications.commands"

    # Print the invite URL for the bot
    print(f"Invite your bot using this URL: {invite_url}")


@bot.event
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check message content first
    has_target_text = "Message sent by" in message.content

    # Then check embeds if no match in content
    if not has_target_text and message.embeds:
        for embed in message.embeds:
            # Check embed title
            if embed.title and "Message sent by" in embed.title:
                has_target_text = True
                break

            # Check embed description
            if embed.description and "Message sent by" in embed.description:
                has_target_text = True
                break

            # Check embed fields
            for field in embed.fields:
                if "Message sent by" in field.name or "Message sent by" in field.value:
                    has_target_text = True
                    break

    # Process if target text was found anywhere
    if has_target_text:
        # Get basic information
        guild_id = message.guild.id if message.guild else None

        # Check if we're currently logging messages in this guild
        if guild_id in bot.logging_channels:
            log_channel_id = bot.logging_channels[guild_id]
            log_channel = bot.get_channel(log_channel_id)

            if log_channel:
                # Prepare a simple log message with available information
                try:
                    # Extract whatever information we can from the message
                    content_lines = message.content.split("\n")
                    main_line = content_lines[0] if content_lines else message.content

                    # If content is empty, but we have embeds, get information from embeds
                    if not main_line and message.embeds:
                        embed = message.embeds[0]
                        main_line = (
                            embed.title or embed.description or "Embedded Message"
                        )
                        # Add field contents if available
                        for field in embed.fields:
                            content_lines.append(f"{field.name}: {field.value}")

                    # Get channel mention if available in the message
                    channel_info = "Unknown"
                    if "in" in main_line:
                        parts = main_line.split("in")
                        if len(parts) > 1:
                            channel_info = parts[1].strip().rstrip(".")

                    await log_channel.send(
                        f"**Deleted Message Detected**\n"
                        f"**Source:** {message.channel.mention}\n"
                        f"**Original Message:** {message.content or 'Embedded content'}\n"
                        f"**Detected In:** {channel_info}\n"
                        f"**Detection Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                except discord.HTTPException as e:
                    print(f"Error sending log message: {e}")

    # Process commands
    await bot.process_commands(message)


def save_progress(channel_id, last_message_id, matched_messages):
    """Save the current scan progress to a file"""
    progress = {
        "channel_id": channel_id,
        "last_message_id": last_message_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "matched_messages_count": len(matched_messages),
    }

    # Save the matched messages separately to avoid the file getting too large
    df = pd.DataFrame(matched_messages)
    df.to_csv(
        "matched_messages_partial.csv",
        index=False,
        mode="a",
        header=not os.path.exists("matched_messages_partial.csv"),
    )

    # Save the progress state
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def load_progress():
    """Load the last scan progress if available"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None


# Hybrid command for collect_messages (works with both / and ! prefix)
@bot.hybrid_command(
    name="collect_messages",
    description="Collects deleted messages from the channel history",
)
@app_commands.describe(
    batch_size="Number of messages to fetch in each batch (default: 100)",
    cooldown="Seconds to wait between batches to avoid rate limits (default: 10)",
)
async def collect_messages(
    ctx, batch_size: int = DEFAULT_BATCH_SIZE, cooldown: int = DEFAULT_COOLDOWN
):
    """
    Collects deleted messages from the channel history.

    Parameters:
    - batch_size: Number of messages to fetch in each batch (default: 100)
    - cooldown: Seconds to wait between batches to avoid rate limits (default: 10)
    """
    channel = ctx.channel
    progress = load_progress()
    matched_messages = []

    # Status message that will be updated
    status_message = await ctx.send("Starting message collection...")

    # Recover any progress from a previous scan
    before_message = None
    if progress and progress["channel_id"] == channel.id:
        try:
            before_message = await channel.fetch_message(progress["last_message_id"])
            await status_message.edit(
                content=f"Resuming scan from message ID: {before_message.id}"
            )

            # Load existing matched messages
            if os.path.exists("../matched_messages_partial.csv"):
                existing_df = pd.read_csv("../matched_messages_partial.csv")
                matched_messages = existing_df.to_dict("records")
        except discord.NotFound:
            await status_message.edit(
                content="Could not find the previous message. Starting a new scan."
            )
            before_message = None

    total_processed = 0
    scanned_everything = False

    try:
        while not scanned_everything:
            try:
                # Fetch a batch of messages
                message_batch = []
                if before_message:
                    history = channel.history(limit=batch_size, before=before_message)
                else:
                    history = channel.history(limit=batch_size)

                # Manually collect messages from the async iterator
                async for message in history:
                    message_batch.append(message)

                # If we got fewer messages than requested, we've reached the end
                if len(message_batch) < batch_size:
                    scanned_everything = True

                if not message_batch:
                    break  # No more messages to process

                # Process the batch
                for message in message_batch:
                    # Check message content first
                    has_target_text = "Message sent by" in message.content
                    embed_content = ""

                    # Then check embeds if no match in content
                    if not has_target_text and message.embeds:
                        for embed in message.embeds:
                            # Check embed title
                            if embed.title and "Message sent by" in embed.title:
                                has_target_text = True
                                embed_content = embed.title
                                break

                            # Check embed description
                            if (
                                embed.description
                                and "Message sent by" in embed.description
                            ):
                                has_target_text = True
                                embed_content = embed.description
                                break

                            # Check embed fields
                            for field in embed.fields:
                                if "Message sent by" in field.name:
                                    has_target_text = True
                                    embed_content = field.name
                                    break
                                if "Message sent by" in field.value:
                                    has_target_text = True
                                    embed_content = field.value
                                    break

                    # Process if target text was found anywhere
                    if has_target_text:
                        # Parse basic information from the content
                        content = message.content or embed_content
                        content_lines = content.split("\n")
                        main_line = content_lines[0] if content_lines else content

                        # If using embed, and we don't have good main line content
                        if not main_line.strip() and message.embeds:
                            embed = message.embeds[0]
                            # Try to build a better content representation from the embed
                            embed_parts = []
                            if embed.title:
                                embed_parts.append(embed.title)
                            if embed.description:
                                embed_parts.append(embed.description)
                            for field in embed.fields:
                                embed_parts.append(f"{field.name}: {field.value}")

                            # Join all parts with newlines
                            content = "\n".join(embed_parts)
                            content_lines = content.split("\n")
                            main_line = content_lines[0] if content_lines else content

                        # Extract user ID if we can find it in the format <@numbers>
                        user_id = "Unknown"
                        if "<@" in main_line and ">" in main_line:
                            start_idx = main_line.find("<@") + 2
                            end_idx = main_line.find(">", start_idx)
                            if start_idx != -1 and end_idx != -1:
                                user_id = main_line[start_idx:end_idx]

                        # Extract channel name if possible
                        channel_name = "Unknown"
                        if "in" in main_line:
                            parts = main_line.split("in")
                            if len(parts) > 1:
                                channel_name = parts[1].strip().rstrip(".")

                        # Get attachment info if any
                        attachment_info = ""
                        if message.attachments:
                            attachment_info = (
                                f", {len(message.attachments)} attachment(s)"
                            )
                        elif len(content_lines) > 1:
                            # Try to get the filename from the next line if it exists
                            attachment_info = (
                                f", possible attachment: {content_lines[1]}"
                            )

                        matched_messages.append(
                            {
                                "Sender ID": user_id,
                                "Channel": channel_name,
                                "Author ID": message.author.id,  # The bot that reported the deletion
                                "Message ID": message.id,
                                "Message Content": content,
                                "Attachment Info": attachment_info,
                                "Timestamp": message.created_at.isoformat(),
                            }
                        )

                # Update the before_message for the next batch
                before_message = message_batch[-1]
                total_processed += len(message_batch)

                # Save progress
                save_progress(channel.id, before_message.id, matched_messages)

                # Update status
                await status_message.edit(
                    content=f"Processed {total_processed} messages, found {len(matched_messages)} matches. Last message date: {before_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )

                # Cooldown to avoid rate limits
                await asyncio.sleep(cooldown)

            except discord.errors.HTTPException as e:
                if e.status == 429:  # Rate limited
                    retry_after = (
                        e.retry_after if hasattr(e, "retry_after") else cooldown * 5
                    )
                    await status_message.edit(
                        content=f"Rate limited! Cooling down for {retry_after} seconds. Will resume after cooldown."
                    )
                    await asyncio.sleep(retry_after)
                else:
                    await status_message.edit(
                        content=f"HTTP Error: {str(e)}. Pausing for {cooldown * 2} seconds."
                    )
                    await asyncio.sleep(cooldown * 2)

    except Exception as e:
        await status_message.edit(
            content=f"Error during scan: {str(e)}. Progress saved - use !collect_messages to resume."
        )
        raise e

    # When done, save final results
    if matched_messages:
        df = pd.DataFrame(matched_messages)
        df.to_csv("matched_messages.csv", index=False)
        await status_message.edit(
            content=f"✅ Complete! Processed {total_processed} messages, found {len(matched_messages)} matches. Results saved to `matched_messages.csv`."
        )
    else:
        await status_message.edit(
            content=f"✅ Complete! Processed {total_processed} messages, but no matches were found."
        )

    # Clean up the progress file
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    if os.path.exists("../matched_messages_partial.csv"):
        os.remove("../matched_messages_partial.csv")


# Hybrid command for scan_status
@bot.hybrid_command(
    name="scan_status", description="Check the status of the current or last scan"
)
async def scan_status(ctx):
    """Check the status of the current or last scan"""
    progress = load_progress()
    if progress:
        channel = bot.get_channel(progress["channel_id"])
        channel_name = channel.name if channel else "Unknown Channel"

        time_diff = datetime.datetime.now() - datetime.datetime.fromisoformat(
            progress["timestamp"]
        )
        hours, remainder = divmod(time_diff.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        status = f"**Scan Status**\n"
        status += f"Channel: {channel_name} (ID: {progress['channel_id']})\n"
        status += f"Last message ID: {progress['last_message_id']}\n"
        status += f"Matched messages so far: {progress['matched_messages_count']}\n"
        status += f"Last updated: {progress['timestamp']} ({int(hours)}h {int(minutes)}m {int(seconds)}s ago)"

        await ctx.send(status)
    else:
        await ctx.send("No scan in progress or previous scan data available.")


# Hybrid command for cancel_scan
@bot.hybrid_command(
    name="cancel_scan", description="Cancel an ongoing scan and clean up progress files"
)
async def cancel_scan(ctx):
    """Cancel an ongoing scan and clean up progress files"""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        await ctx.send("Scan canceled and progress data deleted.")
    else:
        await ctx.send("No scan in progress.")


# New command to start logging messages with "Message sent by"
@bot.hybrid_command(
    name="start_logging",
    description="Start logging messages containing 'Message sent by' in this channel",
)
async def start_logging(ctx):
    """Start logging messages containing 'Message sent by' in this channel"""
    guild_id = ctx.guild.id if ctx.guild else None

    if not guild_id:
        await ctx.send("This command can only be used in a server.")
        return

    # Set the current channel as the logging channel for this guild
    bot.logging_channels[guild_id] = ctx.channel.id

    await ctx.send(
        f"✅ Now logging messages containing 'Message sent by' in this channel."
    )


# Command to stop logging messages
@bot.hybrid_command(
    name="stop_logging",
    description="Stop logging messages containing 'Message sent by'",
)
async def stop_logging(ctx):
    """Stop logging messages containing 'Message sent by'"""
    guild_id = ctx.guild.id if ctx.guild else None

    if not guild_id:
        await ctx.send("This command can only be used in a server.")
        return

    if guild_id in bot.logging_channels:
        del bot.logging_channels[guild_id]
        await ctx.send("✅ Stopped logging messages.")
    else:
        await ctx.send("❌ No active logging in this server.")


# Run the bot
bot.run(TOKEN)
