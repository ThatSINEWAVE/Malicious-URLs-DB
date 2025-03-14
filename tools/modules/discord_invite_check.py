import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import time

# Load environment variables from .env file in the parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

# Discord bot token from .env file
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Check if the token is found in the .env file
if not DISCORD_TOKEN:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Discord token not found in the .env file. Exiting.")
    exit()  # Stop execution if token is not found

# Rate limit value (requests per minute) from .env file
DISCORD_INVITE_RATE_LIMIT = os.getenv("DISCORD_INVITE_RATE_LIMIT", 10)  # Default to 10 requests per minute if not set in the .env
try:
    DISCORD_INVITE_RATE_LIMIT = int(DISCORD_INVITE_RATE_LIMIT)
except ValueError:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Invalid rate limit value in .env. Using default value of 10.")
    DISCORD_INVITE_RATE_LIMIT = 10  # Use default if the rate limit value is invalid

# Headers for the Discord API request
headers = {
    'Authorization': f'Bot {DISCORD_TOKEN}'
}


# Helper function to check invite validity
def check_invite_validity(invite_url):
    invite_code = invite_url.split('/')[-1]  # Extract invite code from the URL
    url = f"https://discord.com/api/v10/invites/{invite_code}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Invite {invite_url} is valid.")
        return True  # Invite is valid
    elif response.status_code == 404:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Invite {invite_url} is invalid or expired.")
        return False  # Invite is invalid or expired
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error checking invite {invite_url}: {response.status_code}")
        return False  # If an error occurs, treat it as invalid


# Function to process the JSON file and update invite status
def update_invite_status():
    # Load the compromised account data
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Loading compromised account data...")
    with open('../Compromised-Discord-Accounts.json', 'r') as f:
        accounts_data = json.load(f)

    # Count total accounts and valid Discord URLs
    total_accounts = len(accounts_data)
    valid_accounts = 0

    for account, details in accounts_data.items():
        surface_url = details.get("SURFACE_URL", "")
        final_url = details.get("FINAL_URL", "")

        # Check if the URLs are from discord domains
        if "discord.gg" in surface_url or "discord.com" in surface_url:
            valid_accounts += 1

    # Print out the total and valid accounts
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Total accounts: {total_accounts}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Accounts with valid discord URLs: {valid_accounts}")

    # Calculate the delay between requests based on the rate limit
    request_delay = 60 / DISCORD_INVITE_RATE_LIMIT  # Delay in seconds per request
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Rate limit is set to {DISCORD_INVITE_RATE_LIMIT} requests per minute.")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Request delay set to {request_delay:.2f} seconds.")

    for account, details in accounts_data.items():
        surface_url = details.get("SURFACE_URL", "")
        final_url = details.get("FINAL_URL", "")

        # Check if the URLs are from discord domains
        if "discord.gg" in surface_url or "discord.com" in surface_url:
            # Extract the invite code from the URLs
            surface_invite_code = surface_url.split('/')[-1]  # Assuming the invite code is the last part of the URL
            final_invite_code = final_url.split('/')[-1] if final_url else surface_invite_code

            # Log what we're doing with timestamps
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking Discord URLs for account {account}")

            # Check surface URL
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking Surface URL: {surface_url}")
            surface_valid = check_invite_validity(surface_url)
            new_surface_status = "ACTIVE" if surface_valid else "INACTIVE"
            if surface_valid:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updating Surface URL {surface_url} to ACTIVE")
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updating Surface URL {surface_url} to INACTIVE")

            # Check final URL if it differs
            if final_url and final_url != surface_url:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking Final URL: {final_url}")
                final_valid = check_invite_validity(final_url)
                new_final_status = "ACTIVE" if final_valid else "INACTIVE"
                if final_valid:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updating Final URL {final_url} to ACTIVE")
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Updating Final URL {final_url} to INACTIVE")
            else:
                new_final_status = new_surface_status

            # Update the account data with the new status and final invite link
            details["SURFACE_URL_STATUS"] = new_surface_status
            details["FINAL_URL_STATUS"] = new_final_status
            if final_url != surface_url:
                details["FINAL_URL"] = f"https://discord.com/invite/{final_invite_code}"
                details["FINAL_URL_DOMAIN"] = "discord.com"

            # Save the updated data back to the file
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Saving updated account data for {account}...")
            with open('../Compromised-Discord-Accounts.json', 'w') as f:
                json.dump(accounts_data, f, indent=4)

            # Log the rate limit delay and pause for the calculated time
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sleeping for {request_delay:.2f} seconds to maintain rate limit...")
            time.sleep(request_delay)  # Sleep for the calculated delay to respect rate limit

        else:
            # If the account doesn't have a valid Discord URL, print a skip message
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Skipping account {account} - No valid Discord URL found.")


# Start the process
if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting invite status check...")
    update_invite_status()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Finished invite status check.")
