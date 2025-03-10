import json
import os
import socket
import requests
from urllib.parse import urlparse

# Configuration
IPINFO_API_TOKEN = 'TOKEN_GOES_HERE'
REQUEST_TIMEOUT = 10  # seconds


def get_country_from_ip(ip):
    """Fetches country information based on an IP address."""
    print(f"[INFO] Getting country for IP: {ip}")
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/country?token={IPINFO_API_TOKEN}", timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            country = response.text.strip()
            print(f"[SUCCESS] Country found for IP {ip}: {country}")
            return country
        else:
            print(f"[ERROR] Failed to get country for IP {ip}, status code: {response.status_code}")
    except Exception as e:
        print(f"[EXCEPTION] Error fetching country for IP {ip}: {e}")
    return "UNKNOWN"


def check_url_status(url):
    """Checks if a URL is active or taken down."""
    print(f"[INFO] Checking status for URL: {url}")
    try:
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=REQUEST_TIMEOUT,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )
        final_url = response.url
        status = "ACTIVE" if response.status_code < 400 else "TAKEN DOWN"
        print(f"[SUCCESS] URL checked: {url} -> Status: {status}, Final URL: {final_url}")
        return status, final_url
    except Exception as e:
        print(f"[EXCEPTION] Failed to check URL: {url}, Error: {e}")
        return "TAKEN DOWN", "UNKNOWN"


def update_accounts_data():
    """Loads, updates, and saves account data from a JSON file."""
    print("[INFO] Starting account data update...")

    # Get file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'Compromised-Discord-Accounts.json')

    # Load existing data
    print(f"[INFO] Loading data from {data_path}")
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"[SUCCESS] Loaded {len(data)} accounts.")
    except Exception as e:
        print(f"[ERROR] Failed to load JSON file: {e}")
        return

    for account_id, account_data in data.items():
        print(f"\n[INFO] Processing account: {account_id}")

        # Check and fill empty fields
        surface_url = account_data.get('SURFACE_URL', '').strip()
        if not surface_url or surface_url == "UNKNOWN":
            print(f"[WARNING] No valid SURFACE_URL for account {account_id}, skipping...")
            continue

        # Check surface URL status and follow redirects
        print(f"[INFO] Checking SURFACE_URL: {surface_url}")
        surface_status, final_url = check_url_status(surface_url)
        account_data['SURFACE_URL_STATUS'] = surface_status
        account_data['FINAL_URL'] = final_url

        # If FINAL_URL is empty, fetch final URL data
        if not account_data.get('FINAL_URL') or account_data['FINAL_URL'] == "UNKNOWN":
            print(f"[INFO] Resolving final URL for account {account_id}")
            account_data['FINAL_URL'] = final_url

        if account_data.get('FINAL_URL') != "UNKNOWN":
            print(f"[INFO] Parsing final URL: {account_data['FINAL_URL']}")
            parsed_url = urlparse(account_data['FINAL_URL'])
            if not account_data.get('FINAL_URL_DOMAIN') or account_data['FINAL_URL_DOMAIN'] == "UNKNOWN":
                account_data['FINAL_URL_DOMAIN'] = parsed_url.netloc

            final_status, _ = check_url_status(account_data['FINAL_URL'])
            if not account_data.get('FINAL_URL_STATUS') or account_data['FINAL_URL_STATUS'] == "UNKNOWN":
                account_data['FINAL_URL_STATUS'] = final_status

            # Get geolocation for the final URL domain if not set
            if not account_data.get('SUSPECTED_REGION_OF_ORIGIN') or account_data['SUSPECTED_REGION_OF_ORIGIN'] == "UNKNOWN":
                try:
                    print(f"[INFO] Resolving domain IP for: {parsed_url.netloc}")
                    domain_ip = socket.gethostbyname(parsed_url.netloc)
                    account_data['SUSPECTED_REGION_OF_ORIGIN'] = get_country_from_ip(domain_ip)
                except Exception as e:
                    print(f"[EXCEPTION] Failed to resolve domain {parsed_url.netloc}: {e}")
                    account_data['SUSPECTED_REGION_OF_ORIGIN'] = "UNKNOWN"
        else:
            print(f"[WARNING] Final URL is UNKNOWN, setting default values.")
            account_data['FINAL_URL_DOMAIN'] = "UNKNOWN"
            account_data['FINAL_URL_STATUS'] = "UNKNOWN"
            account_data['SUSPECTED_REGION_OF_ORIGIN'] = "UNKNOWN"

        # Save updated account data after each account is processed to save on RAM usage
        print(f"[INFO] Saving updated account {account_id} data to {data_path}")
        try:
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"[SUCCESS] Account {account_id} data updated successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to save updated data for account {account_id}: {e}")

    print("[INFO] All accounts processed and updated.")


if __name__ == "__main__":
    update_accounts_data()
