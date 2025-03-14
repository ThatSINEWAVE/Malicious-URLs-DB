import json
import time


def get_current_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def fix_account_numbers(file_path):
    print(
        f"[{get_current_timestamp()}] Starting to fix account numbers in the file: {file_path}"
    )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(
            f"[{get_current_timestamp()}] Successfully loaded the data from the file."
        )
    except Exception as e:
        print(f"[{get_current_timestamp()}] Error loading the file: {e}")
        return

    # Sorting account entries by current CASE_NUMBER just in case they are unordered
    print(f"[{get_current_timestamp()}] Sorting account entries by CASE_NUMBER.")
    sorted_entries = sorted(data.items(), key=lambda x: int(x[1]["CASE_NUMBER"]))

    total_accounts = len(sorted_entries)
    updated_count = 0
    new_data = {}

    for index, (old_key, account) in enumerate(sorted_entries, start=1):
        new_key = f"ACCOUNT_NUMBER_{index}"
        if account["CASE_NUMBER"] != str(index):  # If the case number has changed
            updated_count += 1
        account["CASE_NUMBER"] = str(index)
        new_data[new_key] = account

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)
        print(
            f"[{get_current_timestamp()}] Successfully saved the corrected data back to the file."
        )
    except Exception as e:
        print(f"[{get_current_timestamp()}] Error saving the file: {e}")
        return

    print(f"[{get_current_timestamp()}] Found {total_accounts} accounts in the file.")
    print(f"[{get_current_timestamp()}] {updated_count} accounts were updated.")


# Run the function on the JSON file
fix_account_numbers("../Compromised-Discord-Accounts.json")
