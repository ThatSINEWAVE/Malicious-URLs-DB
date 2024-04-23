
<div align="center">

# [Malicious-Users-DB](https://thatsinewave.github.io/Malicious-URLs-DB/)

This repository serves as a curated JSON file containing lists of websites associated with malicious activities. 
The list is compiled based on personal findings of the repository owner and are intended to help identify and mitigate threats posed by these sites.

![malicious-users](https://github.com/ThatSINEWAVE/Malicious-URLs-DB/assets/133239148/31fb42fc-35ef-4d00-bf27-636e18c6f7b7)

</div>

## Included Files:

- `Tool/exporter_script.py`: This Python script extracts data from an Excel file (`ExporterSheet.xlsx`) and converts it into JSON format, populating the `Compromised-Discord-Accounts.json` file with details of compromised accounts found over time.

- `Compromised-Discord-Accounts.json`: This JSON file contains the full list of details and info about all the compromised accounts found over time. Most of the compromised accounts in this list were used / are actively used in phishing campaigns.

- `index.html`: HTML file for displaying the data in a table format.
  
- `script.js`: JavaScript file for loading and rendering the JSON data into the HTML table, with sorting and sticky navigation functionality.
  
- `styles.css`: CSS file for styling the HTML elements.

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Definitions:

<div align="center">

|            **Definition**            |                              **Description**                             |
|:-----------------------------------:|:-----------------------------------------------------------------------:|
|          CASE_NUMBER            |                 The unique identifier for the case.                |
|              FOUND_ON                |           The date when the compromised account was discovered.          |
|             DISCORD_ID             |           The unique identifier associated with the user on Discord.          |
|              USERNAME              |                 The username of the compromised account.                |
|             BEHAVIOUR             |        Description of the suspicious activities associated with the account.       |
|          ATTACK_METHOD        |             The method used in the attack.             |
|          ATTACK_VECTOR          |     The specific approach or technique used in the attack.     |
|           ATTACK_GOAL           |          The objective of the attack.         |
|        ATTACK_SURFACE        |           The platform or service targeted / used in the attack.           |
| SUSPECTED_REGION_OF_ORIGIN | The suspected geographical location from which the attack originated. |
|            SURFACE_URL            |      The URL associated with the initial interaction or surface level of the attack.      |
|      SURFACE_URL_DOMAIN     |                    The domain of the surface URL.                    |
|    SURFACE_URL_STATUS     |      The status of the surface URL, whether it is active or not.      |
|              FINAL_URL               |       The URL to which the attack directs users after initial interaction.       |
|        FINAL_URL_DOMAIN         |                    The domain of the final URL.                    |
|      FINAL_URL_STATUS      |        The status of the final URL, whether it is active or not.        |

</div>

<div align="center">

# [Join my discord server](https://discord.gg/2nHHHBWNDw)

</div>

## Contributions:

Contributions to this repository are not currently accepted. 
The list is based solely on my discoveries but If anyone wants to add other URLs and you have an extensive collection that you would like to add them to the repo feel free to submit a request.

## Usage:

The data within this JSON file can be used to enhance threat detection and protect users from encountering malicious online content. 
Information provided here serves as a valuable resource for threat intelligence and cybersecurity analysis.

## Disclaimer:

The information provided in this repository is for informational purposes only. 
While efforts are made to ensure accuracy, the repository owner cannot guarantee the completeness or currentness of the data. 
Users are advised to exercise caution when interacting with websites listed herein and to conduct their own investigations as necessary.

## License:

This repository is provided under the MIT License. 
By utilizing the contents of this repository, you agree to abide by the terms of this license.
