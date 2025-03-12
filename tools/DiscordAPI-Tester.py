import json
import time
import requests
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Fetch the bot token from the .env file
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


# Function to fetch Discord username using Discord's API with bot token
def get_discord_username(discord_id, bot_token):
    url = f"https://discord.com/api/v10/users/{discord_id}"
    headers = {"Authorization": f"Bot {bot_token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return user_data.get("username", "")
        elif response.status_code == 401:
            print(
                f"Unauthorized: Invalid bot token or no permissions for user {discord_id}"
            )
            return None
        else:
            print(f"Error fetching data for {discord_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data for {discord_id}: {e}")
        return None


# Check if a Discord invite is still active using the bot API
def check_discord_invite_status(url):
    print(f"Checking status of invite URL: {url}...")
    if "discord.gg" not in url and "discord.com" not in url:
        print(f"Skipping non-Discord URL: {url}")
        return None

    invite_code = url.split("/")[-1]
    api_url = f"https://discord.com/api/v10/invites/{invite_code}"

    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            print(f"Invite {invite_code} is ACTIVE.")
            return "ACTIVE"
        elif response.status_code == 404:
            print(f"Invite {invite_code} is INACTIVE.")
            return "INACTIVE"
        else:
            print(
                f"Invite {invite_code} status is INACTIVE (response code: {response.status_code})."
            )
            return "INACTIVE"
    except requests.RequestException as e:
        print(f"Error checking invite {invite_code}: {e}")
        return "INACTIVE"


# Load the compromised accounts data from JSON file
def load_json_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Save the updated JSON file with non-ASCII characters intact
def save_json(data, filename):
    print(f"Saving updated data to {filename}...")
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Successfully saved updated data to {filename}.")
    except Exception as e:
        print(f"Error saving JSON file: {e}")


# Process the compromised accounts
def process_accounts(data, filename):
    print(f"Starting to process {len(data)} accounts...")

    for account_key, account_data in data.items():
        print(f"\nProcessing account: {account_key}")

        discord_id = account_data.get("DISCORD_ID")
        surface_url = account_data.get("SURFACE_URL")
        final_url = account_data.get("FINAL_URL")

        # Fetch username from Discord API
        if discord_id:
            print(f"Fetching username for Discord ID: {discord_id}...")
            current_username = account_data.get("USERNAME")
            new_username = get_discord_username(discord_id, DISCORD_BOT_TOKEN)

            # Update username if different
            if new_username:
                if new_username != current_username:
                    print(
                        f"Updating username for {discord_id}: {current_username} -> {new_username}"
                    )
                    account_data["USERNAME"] = new_username
                else:
                    print(f"Username for {discord_id} is correct, no update needed.")

        # Wait for 2 seconds before processing URLs
        time.sleep(2)

        # Process Surface URL
        if surface_url and (
            "discord.gg" in surface_url or "discord.com" in surface_url
        ):
            print(f"Found Discord surface URL: {surface_url}")
            surface_status = check_discord_invite_status(surface_url)
            account_data["SURFACE_URL_STATUS"] = (
                surface_status if surface_status else "UNKNOWN"
            )
        else:
            print(f"No valid Discord surface URL found for {account_key}")

        # Process Final URL
        if final_url and ("discord.gg" in final_url or "discord.com" in final_url):
            print(f"Found Discord final URL: {final_url}")
            final_status = check_discord_invite_status(final_url)
            account_data["FINAL_URL_STATUS"] = (
                final_status if final_status else "UNKNOWN"
            )

            # If FINAL_URL_STATUS is INACTIVE, update SURFACE_URL_STATUS
            if final_status == "INACTIVE":
                print(
                    f"FINAL_URL_STATUS for {account_key} is INACTIVE, updating SURFACE_URL_STATUS."
                )
                account_data["SURFACE_URL_STATUS"] = "INACTIVE"
        else:
            print(f"No valid Discord final URL found for {account_key}")

        # Save the data after each account is processed to reduce memory usage
        save_json(data, filename)

        # Only wait 2 seconds if the URLs are Discord URLs
        if surface_url and (
            "discord.gg" in surface_url or "discord.com" in surface_url
        ):
            print("Waiting for 2 seconds before checking next account...")
            time.sleep(2)

    print("Finished processing all accounts.")


# Main function
def main():
    filename = "Compromised-Discord-Accounts.json"

    # Load data
    data = load_json_data(filename)
    if not data:
        print("No data to process, exiting.")
        return

    # Process the accounts
    process_accounts(data, filename)

    print("Testing finished.")


if __name__ == "__main__":
    print("Starting the Discord account checker...")
    main()
