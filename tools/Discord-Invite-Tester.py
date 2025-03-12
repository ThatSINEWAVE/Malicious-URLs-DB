import json
import requests
import time


# Load the JSON file
def load_json(filename):
    print(f"Loading JSON file: {filename}...")
    try:
        with open(
            filename, "r", encoding="utf-8"
        ) as file:  # Ensure the file is read with UTF-8 encoding
            data = json.load(file)
        print(f"Successfully loaded {len(data)} accounts.")
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return {}


# Save the updated JSON file with non-ASCII characters intact
def save_json(data, filename):
    print(f"Saving updated data to {filename}...")
    try:
        with open(
            filename, "w", encoding="utf-8"
        ) as file:  # Ensure the file is saved with UTF-8 encoding
            json.dump(
                data, file, indent=4, ensure_ascii=False
            )  # Prevent ASCII escape sequences
        print(f"Successfully saved updated data to {filename}.")
    except Exception as e:
        print(f"Error saving JSON file: {e}")


# Check if a Discord invite is still active
def check_discord_invite_status(url):
    print(f"Checking status of invite URL: {url}...")
    if "discord.gg" not in url and "discord.com" not in url:
        print(f"Skipping non-Discord URL: {url}")
        return None

    invite_code = url.split("/")[-1]
    api_url = f"https://discord.com/api/v9/invites/{invite_code}"

    try:
        response = requests.get(api_url)
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


# Process the compromised accounts
def process_accounts(data, filename):
    print(f"Starting to process {len(data)} accounts...")

    for account_key, account_data in data.items():
        print(f"\nProcessing account: {account_key}")

        # Only process accounts with discord.gg or discord.com URLs
        surface_url = account_data.get("SURFACE_URL")
        final_url = account_data.get("FINAL_URL")
        surface_status = account_data.get("SURFACE_URL_STATUS")
        final_status = account_data.get("FINAL_URL_STATUS")

        # Process Surface URL
        if surface_url and ("discord.gg" in surface_url or "discord.com" in surface_url):
            print(f"Found Discord surface URL: {surface_url}")
            if not surface_status:
                surface_status = check_discord_invite_status(surface_url)
            account_data["SURFACE_URL_STATUS"] = (
                surface_status if surface_status else "UNKNOWN"
            )
        else:
            print(f"No valid Discord surface URL found for {account_key}")

        # Process Final URL
        if final_url and ("discord.gg" in final_url or "discord.com" in final_url):
            print(f"Found Discord final URL: {final_url}")
            if not final_status:
                final_status = check_discord_invite_status(final_url)
            account_data["FINAL_URL_STATUS"] = (
                final_status if final_status else "UNKNOWN"
            )

            # If FINAL_URL_STATUS is INACTIVE, update SURFACE_URL_STATUS
            if final_status == "INACTIVE":
                print(f"FINAL_URL_STATUS for {account_key} is INACTIVE, updating SURFACE_URL_STATUS.")
                account_data["SURFACE_URL_STATUS"] = "INACTIVE"
        else:
            print(f"No valid Discord final URL found for {account_key}")

        # Save the data after each account is processed to reduce memory usage
        save_json(data, filename)

        # Only wait 2 seconds if the URLs are Discord URLs
        if surface_url and ("discord.gg" in surface_url or "discord.com" in surface_url):
            print("Waiting for 2 seconds before checking next account...")
            time.sleep(2)

    print("Finished processing all accounts.")


# Main function
def main():
    filename = "Compromised-Discord-Accounts.json"

    # Load data
    data = load_json(filename)
    if not data:
        print("No data to process, exiting.")
        return

    # Process the accounts
    process_accounts(data, filename)

    print("Testing finished.")


if __name__ == "__main__":
    print("Starting the Discord invite status checker...")
    main()
