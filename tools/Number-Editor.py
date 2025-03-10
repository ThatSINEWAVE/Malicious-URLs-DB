import json


def update_case_numbers(file_path):
    # Read the JSON file
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Sort accounts by their current case number (in case they are not in order)
    accounts = list(data.items())
    accounts.sort(key=lambda x: int(x[1]["CASE_NUMBER"]))

    # Update case numbers and account keys
    updated_data = {}
    for index, (old_key, account) in enumerate(accounts, start=1):
        new_key = f"ACCOUNT_NUMBER_{index}"
        account["CASE_NUMBER"] = str(index)

        # Ensure usernames remain in their original encoding
        if "USERNAME" in account:
            account["USERNAME"] = account["USERNAME"].encode("utf-8").decode("utf-8")

        updated_data[new_key] = account

    # Write the updated data back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(updated_data, file, indent=2, ensure_ascii=False)


# Call the function with your file path
update_case_numbers("Compromised-Discord-Accounts.json")
