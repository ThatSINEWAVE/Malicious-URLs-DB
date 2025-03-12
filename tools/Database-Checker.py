import json
import time
import requests
import os
import socket
import unicodedata
from urllib.parse import urlparse
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
IPINFO_API_TOKEN = os.getenv("IPINFO_API_TOKEN")
DISCORD_RATE_LIMIT = 20  # Max API calls per second
REQUEST_TIMEOUT = 10  # seconds

# Ensure log directory and file exist
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "log.txt")


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(formatted_message + "\n")
        log_file.flush()
        os.fsync(log_file.fileno())  # Ensure data is written to disk immediately


# Check if log directory exists, create if it doesn't
if not os.path.exists(LOG_DIR):
    print(f"Log directory not found. Creating {LOG_DIR} directory...")
    os.makedirs(LOG_DIR)
    print(f"Created {LOG_DIR} directory successfully.")
else:
    print(f"Log directory {LOG_DIR} already exists.")

# Check if log file exists
if not os.path.exists(LOG_FILE):
    print(f"Log file not found. Creating {LOG_FILE}...")
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Log file created.\n")
    print(f"Created {LOG_FILE} successfully.")
else:
    print(f"Log file {LOG_FILE} already exists.")

# Check for required API tokens
if not DISCORD_BOT_TOKEN:
    print("WARNING: DISCORD_BOT_TOKEN not found in .env file.")
    log_message("WARNING: DISCORD_BOT_TOKEN not found in .env file.")

if not IPINFO_API_TOKEN:
    print("WARNING: IPINFO_API_TOKEN not found in .env file.")
    log_message("WARNING: IPINFO_API_TOKEN not found in .env file.")


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(formatted_message + "\n")
        log_file.flush()
        os.fsync(log_file.fileno())  # Ensure data is written to disk immediately


def is_non_ascii(username):
    """
    Check if the username contains non-ASCII characters.
    This function returns True if the username has characters outside
    the ASCII range.
    """
    return any(unicodedata.category(c) != "Cc" and not c.isascii() for c in username)


def get_discord_username(discord_id, bot_token, request_tracker):
    log_message(f"Fetching username for Discord ID: {discord_id}")
    url = f"https://discord.com/api/v10/users/{discord_id}"
    headers = {"Authorization": f"Bot {bot_token}"}

    request_tracker["count"] += 1
    enforce_rate_limit(request_tracker)

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        username = response.json().get("username", "")
        log_message(f"Retrieved username: {username}")
        return username
    elif response.status_code == 401:
        log_message(
            f"ERROR: Unauthorized access for Discord ID {discord_id}. Invalid token or insufficient permissions."
        )
    return None


def check_discord_invite_status(url, request_tracker, cache):
    if "discord.gg" not in url and "discord.com" not in url:
        log_message(f"URL {url} is not a Discord invite. Skipping check.")
        return None

    invite_code = url.split("/")[-1]
    if invite_code in cache:
        log_message(
            f"Using cached status for invite: {invite_code} -> {cache[invite_code]}"
        )
        return cache[invite_code]

    log_message(f"Checking status for Discord invite: {invite_code}")
    api_url = f"https://discord.com/api/v10/invites/{invite_code}"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}

    request_tracker["count"] += 1
    enforce_rate_limit(request_tracker)

    response = requests.get(api_url, headers=headers)
    status = "ACTIVE" if response.status_code == 200 else "INACTIVE"
    cache[invite_code] = status
    log_message(f"Invite {invite_code} is {status}")
    return status


def is_discord_url(url):
    """Check if a URL is from Discord's domains."""
    return "discord.com" in url or "discord.gg" in url


def get_country_from_ip(ip):
    """Fetches country information based on an IP address."""
    log_message(f"Getting country for IP: {ip}")

    if not IPINFO_API_TOKEN:
        log_message(
            "ERROR: IPINFO_API_TOKEN not set in .env file. Cannot determine country."
        )
        return "UNKNOWN"

    try:
        response = requests.get(
            f"https://ipinfo.io/{ip}/country?token={IPINFO_API_TOKEN}",
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            country = response.text.strip()
            log_message(f"Country found for IP {ip}: {country}")
            return country
        else:
            log_message(
                f"Failed to get country for IP {ip}, status code: {response.status_code}"
            )
    except Exception as e:
        log_message(f"Error fetching country for IP {ip}: {e}")
    return "UNKNOWN"


def check_url_status(url):
    """Checks if a URL is active or inactive."""
    print(f"[INFO] Checking status for URL: {url}")
    try:
        response = requests.head(url, allow_redirects=True, timeout=REQUEST_TIMEOUT)
        final_url = response.url
        status = "ACTIVE" if response.status_code < 400 else "INACTIVE"
        print(f"[SUCCESS] URL checked: {url} -> Status: {status}, Final URL: {final_url}")
        return status, final_url
    except Exception as e:
        print(f"[EXCEPTION] Failed to check URL: {url}, Error: {e}")
        return "INACTIVE", "UNKNOWN"


def get_domain_country(domain):
    """Get the country associated with a domain's IP address."""
    log_message(f"Resolving domain IP for: {domain}")
    try:
        domain_ip = socket.gethostbyname(domain)
        return get_country_from_ip(domain_ip)
    except Exception as e:
        log_message(f"Failed to resolve domain {domain}: {e}")
        return "UNKNOWN"


def enforce_rate_limit(request_tracker):
    elapsed_time = time.perf_counter() - request_tracker["start_time"]
    if request_tracker["count"] >= DISCORD_RATE_LIMIT:
        if elapsed_time < 1:
            log_message("Rate limit reached. Pausing requests...")
            time.sleep(1 - elapsed_time)
        request_tracker["start_time"] = time.perf_counter()
        request_tracker["count"] = 0


def load_json_data(file_path):
    log_message(f"Loading data from {file_path}...")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, filename):
    log_message(f"Saving updated data to {filename}...")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def update_case_numbers(data):
    log_message("Updating case numbers for accounts...")
    sorted_accounts = sorted(
        data.items(), key=lambda x: int(x[1].get("CASE_NUMBER", "0"))
    )
    updated_data = {
        f"ACCOUNT_NUMBER_{i + 1}": {**account, "CASE_NUMBER": str(i + 1)}
        for i, (_, account) in enumerate(sorted_accounts)
    }
    log_message("Case numbers updated.")
    return updated_data


def check_non_ascii_usernames(data):
    log_message("Checking for non-ASCII usernames...")
    non_ascii_count = 0
    non_ascii_cases = []

    for account_key, account in data.items():
        username = account.get("USERNAME", "")
        case_number = account.get("CASE_NUMBER", "Unknown")

        if username and is_non_ascii(username):
            log_message(f"Non-ASCII username found in case {case_number}: {username}")
            account["NON_ASCII_USERNAME"] = True
            non_ascii_count += 1
            non_ascii_cases.append(case_number)
        else:
            account["NON_ASCII_USERNAME"] = False

    if non_ascii_count > 0:
        log_message(
            f"Found {non_ascii_count} accounts with non-ASCII usernames: Cases {', '.join(non_ascii_cases)}"
        )
    else:
        log_message("No accounts with non-ASCII usernames were found.")

    return data, non_ascii_count, non_ascii_cases


def process_accounts(data, filename):
    start_time = time.perf_counter()
    log_message(f"Processing {len(data)} accounts...")
    request_tracker = {"count": 0, "start_time": time.perf_counter()}
    invite_cache = {}

    data = update_case_numbers(data)
    save_json(data, filename)

    for account_key, account in data.items():
        log_message(f"Processing account: {account_key}")
        discord_id = account.get("DISCORD_ID")
        surface_url = account.get("SURFACE_URL", "").strip()
        final_url = account.get("FINAL_URL", "").strip()

        # Check Discord username if ID is provided
        if discord_id:
            new_username = get_discord_username(
                discord_id, DISCORD_BOT_TOKEN, request_tracker
            )
            if new_username and new_username != account.get("USERNAME"):
                log_message(
                    f"Updating username for {discord_id}: {account.get('USERNAME')} -> {new_username}"
                )
                account["USERNAME"] = new_username
            else:
                log_message(
                    f"Username for {discord_id} is already correct. Skipping update."
                )

        # Process SURFACE_URL
        if surface_url and surface_url != "UNKNOWN":
            if is_discord_url(surface_url):
                # Discord URL processing
                discord_status = check_discord_invite_status(
                    surface_url, request_tracker, invite_cache
                )
                if discord_status is not None:
                    account["SURFACE_URL_STATUS"] = discord_status
                    account["SUSPECTED_REGION_OF_ORIGIN"] = "US"
                    log_message(
                        f"Updated SURFACE_URL_STATUS to {discord_status} (Discord URL - setting region to US)"
                    )
            else:
                # Non-Discord URL processing
                log_message(f"Processing non-Discord URL: {surface_url}")
                surface_status, redirected_final_url = check_url_status(surface_url)
                account["SURFACE_URL_STATUS"] = surface_status

                # Update FINAL_URL if it's unknown or empty
                if not final_url or final_url == "UNKNOWN":
                    account["FINAL_URL"] = redirected_final_url
                    log_message(f"Updated FINAL_URL to {redirected_final_url}")
                    # Also set the final_url for further processing
                    final_url = redirected_final_url
        else:
            log_message(
                f"No valid SURFACE_URL for account {account_key}, skipping URL check."
            )

        # Process FINAL_URL if it exists and is not a Discord URL
        if final_url and final_url != "UNKNOWN":
            if is_discord_url(final_url):
                # Discord URL processing
                final_status = check_discord_invite_status(
                    final_url, request_tracker, invite_cache
                )
                if final_status is not None:
                    account["FINAL_URL_STATUS"] = final_status
                    account["SUSPECTED_REGION_OF_ORIGIN"] = "US"
                    log_message(
                        f"Updated FINAL_URL_STATUS to {final_status} (Discord URL - setting region to US)"
                    )
                    # Check for consistency between surface and final URLs
                    if (
                        final_status == "INACTIVE"
                        and account.get("SURFACE_URL_STATUS") == "ACTIVE"
                        and is_discord_url(surface_url)
                    ):
                        account["SURFACE_URL_STATUS"] = "INACTIVE"
                        log_message(
                            "Setting SURFACE_URL_STATUS to INACTIVE because FINAL_URL is INACTIVE"
                        )
            else:
                # Non-Discord URL processing
                log_message(f"Processing non-Discord FINAL_URL: {final_url}")
                final_status, _ = check_url_status(final_url)
                account["FINAL_URL_STATUS"] = final_status
                log_message(f"Updated FINAL_URL_STATUS to {final_status}")

                # Extract and store the domain
                parsed_url = urlparse(final_url)
                domain = parsed_url.netloc
                if domain:
                    account["FINAL_URL_DOMAIN"] = domain
                    log_message(f"Updated FINAL_URL_DOMAIN to {domain}")

                    # Get geolocation info for non-Discord domains
                    if (
                        not account.get("SUSPECTED_REGION_OF_ORIGIN")
                        or account["SUSPECTED_REGION_OF_ORIGIN"] == "UNKNOWN"
                    ):
                        country = get_domain_country(domain)
                        account["SUSPECTED_REGION_OF_ORIGIN"] = country
                        log_message(f"Updated SUSPECTED_REGION_OF_ORIGIN to {country}")

        # Save after each account to prevent data loss
        save_json(data, filename)

    # Move the non-ASCII username check to the end
    data, non_ascii_count, non_ascii_cases = check_non_ascii_usernames(data)
    save_json(data, filename)

    total_time = time.perf_counter() - start_time

    # Final summary
    log_message("Finished processing all accounts.")
    if non_ascii_count > 0:
        log_message(
            f"SUMMARY: Found {non_ascii_count} accounts with non-ASCII usernames in cases: {', '.join(non_ascii_cases)}"
        )
    else:
        log_message("SUMMARY: No accounts with non-ASCII usernames were detected.")
    log_message(f"Total processing time: {total_time:.2f} seconds.")


def main():
    log_message("Starting enhanced database checker...")

    filename = "Compromised-Discord-Accounts.json"
    if not os.path.exists(filename):
        log_message(f"ERROR: Data file {filename} not found!")
        return

    data = load_json_data(filename)
    if not data:
        log_message("No data to process.")
        return

    process_accounts(data, filename)
    log_message("Processing completed.\n")


if __name__ == "__main__":
    main()
