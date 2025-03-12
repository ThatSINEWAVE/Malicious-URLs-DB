import json
import time
import requests
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()


# Function to fetch Discord username using Discord's API with bot token
def get_discord_username(discord_id, bot_token):
    url = f"https://discord.com/api/v10/users/{discord_id}"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return user_data.get("username", "")
        elif response.status_code == 401:
            print(f"Unauthorized: Invalid bot token or no permissions for user {discord_id}")
            return None
        else:
            print(f"Error fetching data for {discord_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data for {discord_id}: {e}")
        return None


# Function to load the compromised accounts data from JSON file
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Function to update the account username if needed
def update_account_username(accounts, file_path, bot_token):
    for account_key, account_data in accounts.items():
        case_number = account_data.get("CASE_NUMBER", "Unknown")
        discord_id = account_data.get("DISCORD_ID")
        current_username = account_data.get("USERNAME")

        if discord_id:
            print(f"Processing case number {case_number} ({discord_id})...")

            # Fetch current username from Discord API
            new_username = get_discord_username(discord_id, bot_token)

            if new_username and new_username != current_username:
                print(f"Case {case_number}: Updating username for {discord_id}: {current_username} -> {new_username}")
                account_data["USERNAME"] = new_username
                # Write changes to file after each update to save RAM usage
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(accounts, file, ensure_ascii=False, indent=4)
            else:
                print(f"Case {case_number}: No update needed for {discord_id}, username is correct.")

        # Slow down the loop to avoid hitting rate limits
        time.sleep(1)


def main():
    file_path = "Compromised-Discord-Accounts.json"
    bot_token = os.getenv("DISCORD_BOT_TOKEN")  # Load the token from the .env file
    if not bot_token:
        print("Error: Bot token not found. Please check the .env file.")
        return
    # Load the data from JSON file
    accounts = load_json_data(file_path)
    # Update usernames and save after each change
    update_account_username(accounts, file_path, bot_token)


if __name__ == "__main__":
    main()
