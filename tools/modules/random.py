import json

# Load the data from the JSON file
with open('../Compromised-Discord-Accounts.json', 'r') as file:
    data = json.load(file)

# Remove the redundant 'ACCOUNT_NUMBER_' field from each account
for account in data.values():
    if 'ACCOUNT_NUMBER_' in account:
        del account['ACCOUNT_NUMBER_']

# Save the modified data back to the file
with open('../Compromised-Discord-Accounts.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Redundant 'ACCOUNT_NUMBER_' fields removed successfully!")
