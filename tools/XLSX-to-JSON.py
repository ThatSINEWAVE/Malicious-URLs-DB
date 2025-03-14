import openpyxl
import json
from datetime import datetime
from urllib.parse import urlparse

# Open the Excel file
workbook = openpyxl.load_workbook("ExporterSheet.xlsx")
worksheet = workbook.active

# Load existing data from the output JSON file if it exists
try:
    with open("Compromised-Discord-Accounts.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}

# Create a set of existing DISCORD_IDs from the loaded JSON data
existing_discord_ids = {account["DISCORD_ID"] for account in data.values()}

# Iterate over the rows in the worksheet
for row_number, row in enumerate(
    worksheet.iter_rows(min_row=2, values_only=True), start=1
):
    (
        NOUMBER,
        FOUND_ON,
        DISCORD_ID,
        USERNAME,
        BEHAVIOUR,
        TYPE,
        METHOD,
        TARGET,
        PLATFORM,
        SURFACE_URL,
        REGION,
        STATUS,
    ) = row

    # Convert DISCORD_ID to string for consistency
    discord_id_str = str(DISCORD_ID) if DISCORD_ID is not None else "Unknown"

    # Skip if the DISCORD_ID already exists in the JSON data
    if discord_id_str in existing_discord_ids:
        continue

    # Handle missing date values
    found_on_str = FOUND_ON.strftime("%Y-%m-%d") if FOUND_ON else "Unknown"

    # Get the domain from the SURFACE_URL
    surface_url_domain = ""
    if SURFACE_URL:
        parsed_url = urlparse(SURFACE_URL)
        surface_url_domain = parsed_url.netloc

    # Check if the username contains non-ASCII characters
    non_ascii_username = not USERNAME.isascii() if USERNAME else False

    # Create a dictionary for the current account
    account = {
        "CASE_NUMBER": f"{row_number}",
        "FOUND_ON": found_on_str,
        "DISCORD_ID": discord_id_str,
        "USERNAME": USERNAME if USERNAME is not None else "Unknown",
        "ACCOUNT_STATUS": "",
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
        "FINAL_URL_STATUS": "",
        "NON_ASCII_USERNAME": non_ascii_username,
        "LAST_VT_CHECK": "",
    }

    # Append the new entry at the end of the dictionary
    data[f"ACCOUNT_NUMBER_{len(data) + 1}"] = account

    # Add the new DISCORD_ID to the set of existing DISCORD_IDs
    existing_discord_ids.add(discord_id_str)

# Write the updated JSON data to a file
with open("Compromised-Discord-Accounts.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
