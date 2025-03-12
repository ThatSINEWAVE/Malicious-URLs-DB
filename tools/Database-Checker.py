import json
import time
import requests
import os
import socket
import unicodedata
import base64
from urllib.parse import urlparse
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
IPINFO_API_TOKEN = os.getenv("IPINFO_API_TOKEN")
VIRUSTOTAL_API_TOKEN = os.getenv("VIRUSTOTAL_API_TOKEN")
DISCORD_RATE_LIMIT = 20  # Max API calls per second
REQUEST_TIMEOUT = 10  # seconds
VIRUSTOTAL_RATE_LIMIT = 4  # 4 requests per minute
VIRUSTOTAL_RATE_LIMIT_PERIOD = 60  # 60 seconds

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
    log_message("WARNING: DISCORD_BOT_TOKEN not found in .env file.")

if not IPINFO_API_TOKEN:
    log_message("WARNING: IPINFO_API_TOKEN not found in .env file.")

if not VIRUSTOTAL_API_TOKEN:
    log_message("WARNING: VIRUSTOTAL_API_TOKEN not found in .env file.")


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


def count_excluded_domains(data, excluded_domains):
    """Counts accounts whose SURFACE_URL_DOMAIN does not contain any of the excluded domains."""
    count = 0
    for account in data.values():
        surface_url_domain = account.get("SURFACE_URL_DOMAIN", "").lower()
        if not any(domain in surface_url_domain for domain in excluded_domains):
            count += 1
    return count


def check_url_status(url, vt_request_tracker, data, filename, account_key):
    """Checks URL status using VirusTotal and saves data immediately"""
    global vt_response
    excluded_domains = {"t.me", "discord.com", "discord.gg", "funpay.com"}
    parsed = urlparse(url)
    domain = parsed.netloc

    # Handle excluded domains first
    if any(excluded in domain for excluded in excluded_domains):
        try:
            response = requests.head(url, allow_redirects=True, timeout=REQUEST_TIMEOUT)
            final_url = response.url
            status = "ACTIVE" if response.status_code < 400 else "INACTIVE"
            log_message(f"Excluded domain check: {url} → {status}")
            return status, final_url
        except Exception as e:
            log_message(f"Excluded domain check failed: {url}, Error: {e}")
            return "INACTIVE", "UNKNOWN"

    vt_malicious = False
    final_url = url
    vt_data = None

    if VIRUSTOTAL_API_TOKEN:
        try:
            # Normalize and encode URL
            parsed = urlparse(url)
            if not parsed.scheme:
                url = f"http://{url}"
                parsed = urlparse(url)

            clean_url = parsed.geturl()
            url_bytes = clean_url.encode("utf-8")
            encoded_url = base64.urlsafe_b64encode(url_bytes).decode("utf-8").strip("=")

            # Enforce rate limit
            vt_request_tracker["count"] += 1
            enforce_vt_rate_limit(vt_request_tracker)

            headers = {"x-apikey": VIRUSTOTAL_API_TOKEN}
            vt_response = requests.get(
                f"https://www.virustotal.com/api/v3/urls/{encoded_url}",
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )

            if vt_response.status_code == 200:
                vt_data = vt_response.json()
                stats = (
                    vt_data.get("data", {})
                    .get("attributes", {})
                    .get("last_analysis_stats", {})
                )
                vt_malicious = stats.get("malicious", 0) > 0

                # Extract final URL from VirusTotal data
                redirection_chain = (
                    vt_data.get("data", {})
                    .get("attributes", {})
                    .get("redirection_chain", [])
                )
                last_final_url = (
                    vt_data.get("data", {})
                    .get("attributes", {})
                    .get("last_final_url", url)
                )
                final_url = (
                    last_final_url
                    if last_final_url
                    else (redirection_chain[-1] if redirection_chain else url)
                )

                log_message(
                    f"VirusTotal check: {url} → Malicious: {vt_malicious}, Final URL: {final_url}"
                )

                # Immediate save after getting VT data
                data[account_key]["LAST_VT_CHECK"] = datetime.now().isoformat()
                save_json(data, filename)

        except Exception as e:
            log_message(f"VirusTotal API error for {url}: {e}")

    if vt_malicious:
        return "INACTIVE", final_url

    # Fallback check if no VT data
    if not vt_data or vt_response.status_code != 200:
        try:
            response = requests.head(url, allow_redirects=True, timeout=REQUEST_TIMEOUT)
            final_url = response.url
            status = "ACTIVE" if response.status_code < 400 else "INACTIVE"
            log_message(f"HTTP check: {url} → {status}")
            return status, final_url
        except Exception as e:
            log_message(f"HTTP check failed: {url}, Error: {e}")
            return "INACTIVE", "UNKNOWN"

    return "ACTIVE", final_url


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


def enforce_vt_rate_limit(vt_request_tracker):
    """Enforces VirusTotal's rate limit of 4 requests per minute"""
    current_time = time.perf_counter()
    elapsed_time = current_time - vt_request_tracker["start_time"]

    if vt_request_tracker["count"] >= VIRUSTOTAL_RATE_LIMIT:
        if elapsed_time < VIRUSTOTAL_RATE_LIMIT_PERIOD:
            sleep_time = VIRUSTOTAL_RATE_LIMIT_PERIOD - elapsed_time
            log_message(
                f"VirusTotal rate limit reached. Sleeping for {sleep_time:.2f} seconds."
            )
            time.sleep(sleep_time)
            # Reset tracker after waiting
            vt_request_tracker["start_time"] = time.perf_counter()
            vt_request_tracker["count"] = 0
        else:
            # Reset tracker if period has expired
            vt_request_tracker["start_time"] = current_time
            vt_request_tracker["count"] = 0


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

    # Ensure sorting works even if "CASE_NUMBER" is missing
    sorted_accounts = sorted(
        data.items(), key=lambda x: int(x[1].get("CASE_NUMBER", "0"))
    )

    # Ensure 'sorted_accounts' is not empty before enumeration
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


def process_accounts(data, filename, starting_case=1):
    start_time = time.perf_counter()
    log_message(f"Processing accounts starting from case {starting_case}...")

    # Calculate and log excluded domain count
    excluded_domains = ["t.me", "discord.com", "discord.gg", "mediafire.com"]
    count = count_excluded_domains(data, excluded_domains)
    log_message(
        f"Total cases without {', '.join(excluded_domains)} in SURFACE_URL_DOMAIN: {count}"
    )

    request_tracker = {"count": 0, "start_time": time.perf_counter()}
    vt_request_tracker = {"count": 0, "start_time": time.perf_counter()}
    invite_cache = {}

    # Sort accounts by CASE_NUMBER
    sorted_accounts = sorted(
        data.items(), key=lambda x: int(x[1].get("CASE_NUMBER", "0"))
    )

    # Filter accounts based on starting_case
    filtered_accounts = []
    for account_key, account in sorted_accounts:
        case_number = int(account.get("CASE_NUMBER", "0"))
        if case_number >= starting_case:
            filtered_accounts.append((account_key, account))

    log_message(
        f"Processing {len(filtered_accounts)} accounts starting from case {starting_case}."
    )

    for account_key, account in filtered_accounts:
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
                log_message(f"Processing non-Discord URL: {surface_url}")
                surface_status, redirected_final_url = check_url_status(
                    surface_url, vt_request_tracker, data, filename, account_key
                )
                account["SURFACE_URL_STATUS"] = surface_status

                if not final_url or final_url == "UNKNOWN":
                    account["FINAL_URL"] = redirected_final_url
                    log_message(f"Updated FINAL_URL to {redirected_final_url}")
                    final_url = redirected_final_url
                    save_json(data, filename)  # Additional save

        else:
            log_message(
                f"No valid SURFACE_URL for account {account_key}, skipping URL check."
            )

        # Process FINAL_URL
        if final_url and final_url != "UNKNOWN":
            if is_discord_url(final_url):
                final_status = check_discord_invite_status(
                    final_url, request_tracker, invite_cache
                )
                if final_status is not None:
                    account["FINAL_URL_STATUS"] = final_status
                    account["SUSPECTED_REGION_OF_ORIGIN"] = "US"
                    log_message(
                        f"Updated FINAL_URL_STATUS to {final_status} (Discord URL - setting region to US)"
                    )
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
                log_message(f"Processing non-Discord FINAL_URL: {final_url}")
                final_status, _ = check_url_status(
                    final_url, vt_request_tracker, data, filename, account_key
                )
                account["FINAL_URL_STATUS"] = final_status
                log_message(f"Updated FINAL_URL_STATUS to {final_status}")
                save_json(data, filename)  # Additional save

                parsed_url = urlparse(final_url)
                domain = parsed_url.netloc
                if domain:
                    account["FINAL_URL_DOMAIN"] = domain
                    log_message(f"Updated FINAL_URL_DOMAIN to {domain}")

                    if (
                        not account.get("SUSPECTED_REGION_OF_ORIGIN")
                        or account["SUSPECTED_REGION_OF_ORIGIN"] == "UNKNOWN"
                    ):
                        country = get_domain_country(domain)
                        account["SUSPECTED_REGION_OF_ORIGIN"] = country
                        log_message(f"Updated SUSPECTED_REGION_OF_ORIGIN to {country}")

        save_json(data, filename)

    data, non_ascii_count, non_ascii_cases = check_non_ascii_usernames(data)
    save_json(data, filename)

    total_time = time.perf_counter() - start_time
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

    # Prompt user for starting point
    print("\nDo you want to start processing from the beginning or a specific case?")
    start_choice = input("Enter 'beginning' or 'specific': ").strip().lower()
    starting_case = 1
    if start_choice == "specific":
        while True:
            try:
                starting_case = int(input("Enter the case number to start from: "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        # Update case numbers to start fresh
        data = update_case_numbers(data)
        save_json(data, filename)

    process_accounts(data, filename, starting_case)
    log_message("Processing completed.\n")


if __name__ == "__main__":
    main()
