import json
import requests
import time


# Load the JSON file
def load_json(filename):
    print(f"Loading JSON file: {filename}...")
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        print(f"Successfully loaded {len(data)} accounts.")
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return {}


# Save the updated JSON file
def save_json(data, filename):
    print(f"Saving updated data to {filename}...")
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Successfully saved updated data to {filename}.")
    except Exception as e:
        print(f"Error saving JSON file: {e}")


# Check if a Discord invite is still active
def check_discord_invite_status(url):
    print(f"Checking status of invite URL: {url}...")
    if 'discord.gg' not in url and 'discord.com' not in url:
        print(f"Skipping non-Discord URL: {url}")
        return None

    invite_code = url.split('/')[-1]
    api_url = f"https://discord.com/api/v9/invites/{invite_code}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            print(f"Invite {invite_code} is ACTIVE.")
            return 'ACTIVE'
        elif response.status_code == 404:
            print(f"Invite {invite_code} is TAKEN DOWN.")
            return 'TAKEN DOWN'
        else:
            print(f"Invite {invite_code} status is UNKNOWN (response code: {response.status_code}).")
            return 'UNKNOWN'
    except requests.RequestException as e:
        print(f"Error checking invite {invite_code}: {e}")
        return 'UNKNOWN'


# Process the compromised accounts
def process_accounts(data):
    print(f"Starting to process {len(data)} accounts...")

    for account_key, account_data in data.items():
        print(f"\nProcessing account: {account_key}")

        # Only process accounts with discord.gg or discord.com URLs
        surface_url = account_data.get("SURFACE_URL")
        final_url = account_data.get("FINAL_URL")

        if surface_url and ('discord.gg' in surface_url or 'discord.com' in surface_url):
            print(f"Found Discord surface URL: {surface_url}")
            surface_status = check_discord_invite_status(surface_url)
            account_data["SURFACE_URL_STATUS"] = surface_status if surface_status else "UNKNOWN"
        else:
            print(f"No valid Discord surface URL found for {account_key}")

        if final_url and ('discord.gg' in final_url or 'discord.com' in final_url):
            print(f"Found Discord final URL: {final_url}")
            final_status = check_discord_invite_status(final_url)
            account_data["FINAL_URL_STATUS"] = final_status if final_status else "UNKNOWN"
        else:
            print(f"No valid Discord final URL found for {account_key}")

        # Adding a small delay to avoid rate-limiting
        print("Waiting for 2 seconds before checking next account...")
        time.sleep(2)

    print("Finished processing all accounts.")


# Main function
def main():
    filename = 'Compromised-Discord-Accounts.json'

    # Load data
    data = load_json(filename)
    if not data:
        print("No data to process, exiting.")
        return

    # Process the accounts
    process_accounts(data)

    # Save the updated data
    save_json(data, filename)


if __name__ == "__main__":
    print("Starting the Discord invite status checker script...")
    main()
    print("Script finished.")
