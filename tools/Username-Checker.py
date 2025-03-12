import json
import unicodedata


def is_non_english(username):
    """
    Check if the username contains non-standard English characters.
    This function returns True if the username has characters outside
    the ASCII range (which would likely indicate non-English characters).
    """
    return any(unicodedata.category(c) != 'Cc' and not c.isascii() for c in username)


def check_compromised_accounts(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Loop through each account and check the username
    for account_id, account_info in data.items():
        username = account_info.get("USERNAME", "")
        if is_non_english(username):
            print(f"Non-English username found in case {account_info['CASE_NUMBER']}: {username}")


# Path to the JSON file
file_path = 'Compromised-Discord-Accounts.json'

# Run the check
check_compromised_accounts(file_path)
