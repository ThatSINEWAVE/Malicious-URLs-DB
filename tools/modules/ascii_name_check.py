import json
import string


# Function to check if a string is ASCII
def is_ascii(s):
    return all(c in string.printable for c in s)


# Load the JSON data from the file
with open('../Compromised-Discord-Accounts.json', 'r') as file:
    data = json.load(file)

# Print the number of cases found
timestamp_start = data['ACCOUNT_NUMBER_1']['LAST_CHECK'][:19]
print(f"[{timestamp_start}] Found {len(data)} cases in the JSON.")

# Initialize counters for the updated usernames
updated_true = 0
updated_false = 0

# Initialize timestamp variable
timestamp_end = timestamp_start  # Default to the start timestamp if no accounts are processed

# Iterate through the accounts
for account_number, account_info in data.items():
    username = account_info["USERNAME"]
    timestamp = account_info["LAST_CHECK"][:19]

    # Check if the username is ASCII
    if is_ascii(username):
        account_info["NON_ASCII_USERNAME"] = False
        updated_false += 1
    else:
        account_info["NON_ASCII_USERNAME"] = True
        updated_true += 1
        print(f"[{timestamp}] Username for {username} is non-ASCII, NON_ASCII_USERNAME set to True.")

    # Update the timestamp_end to the latest timestamp
    timestamp_end = timestamp

# Print the summary of updates with timestamps
print(f"[{timestamp_end}] {updated_true} accounts updated with NON_ASCII_USERNAME set to True.")
print(f"[{timestamp_end}] {updated_false} accounts updated with NON_ASCII_USERNAME set to False.")

# Save the updated data back to the file
with open('../Compromised-Discord-Accounts.json', 'w') as file:
    json.dump(data, file, indent=4)
