import openpyxl
import json
from datetime import datetime
from urllib.parse import urlparse

# Open the Excel file
workbook = openpyxl.load_workbook('ExporterSheet.xlsx')
worksheet = workbook.active

# Create a dictionary to store the data
data = {}

# Load existing data from the output.json file if it exists
try:
    with open("Compromised-Discord-Accounts.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    pass

# Iterate over the rows in the worksheet
for row_number, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=1):
    # Extract the values from the row
    NOUMBER, FOUND_ON, DISCORD_ID, USERNAME, BEHAVIOUR, TYPE, METHOD, TARGET, PLATFORM, SURFACE_URL, REGION, STATUS = row

    # Handle missing date values
    if FOUND_ON is None:
        found_on_str = "Unknown"
    else:
        found_on_str = FOUND_ON.strftime('%Y-%m-%d')

    # Get the domain from the SURFACE_URL
    surface_url_domain = ""
    if SURFACE_URL:
        parsed_url = urlparse(SURFACE_URL)
        surface_url_domain = parsed_url.netloc

    # Create a dictionary for the current account
    account = {
        "CASE_NUMBER": f"{row_number}",
        "FOUND_ON": found_on_str,
        "DISCORD_ID": str(DISCORD_ID) if DISCORD_ID is not None else "Unknown",
        "USERNAME": USERNAME if USERNAME is not None else "Unknown",
        "BEHAVIOUR": BEHAVIOUR if BEHAVIOUR is not None else "Unknown",
        "ATTACK_METHOD": TYPE if TYPE is not None else "Unknown",
        "ATTACK_VECTOR": METHOD if METHOD is not None else "Unknown",
        "ATTACK_GOAL": TARGET if TARGET is not None else "Unknown",
        "ATTACK_SURFACE": PLATFORM if PLATFORM is not None else "Unknown",
        "SUSPECTED_REGION_OF_ORIGIN": REGION if REGION is not None else "Unknown",
        "SURFACE_URL": SURFACE_URL if SURFACE_URL is not None else "Unknown",
        "SURFACE_URL_DOMAIN": surface_url_domain,
        "SURFACE_URL_STATUS": STATUS if STATUS is not None else "Unknown",
        "FINAL_URL": "",
        "FINAL_URL_DOMAIN": "",
        "FINAL_URL_STATUS": ""
    }

    # Update the data dictionary with the new account
    data[f"ACCOUNT_NUMBER_{row_number}"] = account

# Convert the data dictionary to JSON
json_data = json.dumps(data, indent=2)

# Write the JSON data to a file
with open("Compromised-Discord-Accounts.json", "w") as file:
    file.write(json_data)
