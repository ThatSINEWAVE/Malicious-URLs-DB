import json
import requests
import time
import logging
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_USERS_RATE_LIMIT = int(
    os.getenv("DISCORD_USERS_RATE_LIMIT", 10)
)  # Requests per minute

# Set up the logger for nice prints
logging.basicConfig(level=logging.INFO, format="%(message)s")


def log_message(message):
    """Print formatted log messages."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")


def check_discord_username(discord_id, expected_username):
    """Check the current username for a given Discord ID using the Discord API."""
    url = f"https://discord.com/api/v10/users/{discord_id}"
    headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        current_username = user_data["username"]

        if current_username == expected_username:
            log_message(
                f"Username for Discord ID {discord_id} is correct: {expected_username}"
            )
            return None  # Username is correct, no update needed

        elif "deleted_user" in current_username:
            log_message(
                f"User with Discord ID {discord_id} has been deleted. Updating status."
            )
            return "DELETED"  # User is deleted, return deleted status

        else:
            log_message(
                f"Username for Discord ID {discord_id} has changed from {expected_username} to {current_username}. Updating."
            )
            return current_username  # Username is incorrect, return new username

    else:
        log_message(
            f"Error retrieving user data for Discord ID {discord_id}: {response.status_code}"
        )
        return None


def update_json_file(file_path, updated_data):
    """Update the JSON file with the corrected information."""
    with open(file_path, "w") as file:
        json.dump(updated_data, file, indent=4)
    log_message(f"Updated JSON file with new data.")


def main():
    file_path = "../Compromised-Discord-Accounts.json"

    try:
        # Read the existing data from the JSON file
        with open(file_path, "r") as file:
            data = json.load(file)

        # Print how many cases were found in the JSON file
        log_message(f"Found {len(data)} accounts in the JSON file.")

        # Check if the token is available in the env
        if not DISCORD_TOKEN:
            log_message(
                "DISCORD_TOKEN not found in the environment variables. Exiting."
            )
            return

        # Print the rate limit
        log_message(
            f"Rate limit found: {DISCORD_USERS_RATE_LIMIT} requests per minute."
        )

        # Loop through all accounts and check usernames
        for account_number, account_data in data.items():
            discord_id = account_data["DISCORD_ID"]
            expected_username = account_data["USERNAME"]
            current_status = account_data["ACCOUNT_STATUS"]

            log_message(
                f"Checking account {account_number}: {discord_id} ({expected_username})"
            )

            # Get the updated username or account status
            updated_username_or_status = check_discord_username(
                discord_id, expected_username
            )

            if updated_username_or_status:
                if updated_username_or_status == "DELETED":
                    account_data["ACCOUNT_STATUS"] = "DELETED"
                else:
                    account_data["USERNAME"] = updated_username_or_status

            # Rate limit: Sleep if necessary
            time.sleep(60 / DISCORD_USERS_RATE_LIMIT)  # Sleep to respect the rate limit

        # Update the JSON file after processing
        update_json_file(file_path, data)

    except Exception as e:
        log_message(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
