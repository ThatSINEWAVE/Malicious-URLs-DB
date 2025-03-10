<div align="center">

# [Malicious URLs & Accounts DB](https://thatsinewave.github.io/Malicious-URLs-DB/)

![Banner](https://raw.githubusercontent.com/ThatSINEWAVE/Malicious-URLs-DB/refs/heads/main/.github/SCREENSHOTS/Malicious-URLs-DB.png)

A web-based dashboard tracking compromised Discord accounts involved in phishing campaigns and malicious activities

</div>

## Repository Structure

```
├── docs/
│   ├── index.html                  # Main web interface
│   ├── styles.css                  # Dashboard styling
│   ├── tailwind.min.css            # Tailwind CSS framework
│   ├── script.js                   # Interactive dashboard logic
│   ├── dayjs.min.js                # Date handling library
│   ├── chart.min.js                # Chart.js library for visualizations
│   ├── site-data/
│   │   ├── social-share/           # Social sharing related assets
│   │   └── Malicious-URLs-DB.png   # Blank image for malicious URLs database
│   ├── android-icon-36x36.png      # Android icon (36x36)
│   ├── android-icon-48x48.png      # Android icon (48x48)
│   ├── android-icon-72x72.png      # Android icon (72x72)
│   ├── android-icon-96x96.png      # Android icon (96x96)
│   ├── android-icon-144x144.png    # Android icon (144x144)
│   ├── android-icon-192x192.png    # Android icon (192x192)
│   ├── apple-icon.png              # Apple icon (default)
│   ├── apple-icon-57x57.png        # Apple icon (57x57)
│   ├── apple-icon-60x60.png        # Apple icon (60x60)
│   ├── apple-icon-72x72.png        # Apple icon (72x72)
│   ├── apple-icon-76x76.png        # Apple icon (76x76)
│   ├── apple-icon-114x114.png      # Apple icon (114x114)
│   ├── apple-icon-120x120.png      # Apple icon (120x120)
│   ├── apple-icon-144x144.png      # Apple icon (144x144)
│   ├── apple-icon-152x152.png      # Apple icon (152x152)
│   ├── apple-icon-180x180.png      # Apple icon (180x180)
│   ├── apple-icon-precomposed.png  # Apple icon (precomposed)
│   ├── favicon.ico                 # Favicon (ICO format)
│   ├── favicon-16x16.png           # Favicon (16x16)
│   ├── favicon-32x32.png           # Favicon (32x32)
│   ├── favicon-96x96.png           # Favicon (96x96)
│   ├── ms-icon-70x70.png           # Microsoft icon (70x70)
│   ├── ms-icon-144x144.png         # Microsoft icon (144x144)
│   ├── ms-icon-150x150.png         # Microsoft icon (150x150)
│   ├── ms-icon-310x310.png         # Microsoft icon (310x310)
│   └── site.manifest               # Web app manifest
├── data/
│   └── Compromised-Discord-Accounts.json  # Primary dataset of compromised accounts
└── tools/
    ├── XLSX-to-JSON.py                    # Excel to JSON converter
    ├── URL-Tester.py                      # Mass tester for URLs using IPInfo API
    ├── Number-Editor.py                   # Script to edit case numbers
    ├── Discord-Invite-Tester.py           # Test tool for Discord invites
    ├── ExporterSheet.xlsx                 # Exported Excel file from private Google sheet
    └── Compromised-Discord-Accounts.json  # Backup copy of primary dataset
```

## Features

- **Dark/Light Mode Toggle** - Easily switch between dark and light modes to suit your preference.
- **Interactive Analytics** - Visualize the data with 4 real-time charts:
  - Attack timeline
  - Method distribution
  - Targeted platforms
  - Geographic origins
- **Advanced Filtering** - Search by:
  - Username/Discord ID
  - Attack method
  - Date range
- **CSV Export** - Download filtered data as CSV for further analysis.
- **Pagination** - Display 10 entries per page for easy navigation.
- **Account Details Modal** - View full details of each compromised account, including attack method and surface details.

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/ThatSINEWAVE/Malicious-URLs-DB.git
```

2. Host the web app:
```bash
cd docs && python3 -m http.server 8000
```

3. Access the dashboard at:
`http://localhost:8000`

## 🔧 Data Management

1. Update the Excel sheet in `Tool/ExporterSheet.xlsx` with new data.

2. Run the exporter script to convert Excel data into JSON format:
```bash
python3 Tool/exporter_script.py
```

3. The updated JSON dataset will be generated in the root directory.

## Data Definitions

| Field                      | Description                                         |
|----------------------------|-----------------------------------------------------|
| CASE_NUMBER                | Unique case identifier                              |
| FOUND_ON                   | Discovery date                                      |
| DISCORD_ID                 | User's Discord Snowflake ID                         |
| USERNAME                   | Account username                                    |
| BEHAVIOUR                  | Suspicious activity description                     |
| ATTACK_METHOD              | Primary attack technique                            |
| ATTACK_VECTOR              | Implementation method                               |
| ATTACK_GOAL                | Campaign objective                                  |
| ATTACK_SURFACE             | Targeted platform/service                           |
| SUSPECTED_REGION_OF_ORIGIN | Suspected region of origin                          |
| SURFACE_URL                | Initial phishing URL                                |
| SURFACE_URL_DOMAIN         | Domain of the initial phishing URL                  |
| SURFACE_URL_STATUS         | Status of the initial phishing URL (e.g., ACTIVE)   |
| FINAL_URL                  | Endpoint malicious URL                              |
| FINAL_URL_DOMAIN           | Domain of the endpoint malicious URL                |
| FINAL_URL_STATUS           | Status of the endpoint malicious URL (e.g., ACTIVE) |

### Example Entry

For instance, the entry you provided would look like this:

| Field                      | Value                                                    |
|----------------------------|----------------------------------------------------------|
| CASE_NUMBER                | 123                                                      |
| FOUND_ON                   | 2025-03-10                                               |
| DISCORD_ID                 | 123456789012345678                                       |
| USERNAME                   | exampleuser                                              |
| BEHAVIOUR                  | User sending phishing links disguised as game promotions |
| ATTACK_METHOD              | Phishing site                                            |
| ATTACK_VECTOR              | Cloned login page for a popular game                     |
| ATTACK_GOAL                | Stealing login credentials for in-game currency          |
| ATTACK_SURFACE             | Online gaming platform                                   |
| SUSPECTED_REGION_OF_ORIGIN | Canada                                                   |
| SURFACE_URL                | https://example.com/xyz123                               |
| SURFACE_URL_DOMAIN         | example.com                                              |
| SURFACE_URL_STATUS         | ACTIVE                                                   |
| FINAL_URL                  | https://malicioussite.com/login                          |
| FINAL_URL_DOMAIN           | malicioussite.com                                        |
| FINAL_URL_STATUS           | ACTIVE                                                   |

## Security Features

- **Real-time URL Status Tracking**: Monitor the status of URLs (Active/Inactive).
- **Automatic Data Refresh**: Refresh the dashboard data with a button click.
- **Visual Status Indicators**: Use status indicators such as 🔴 for Active and 🟢 for Neutral URLs.
- **Malicious Domain Tracking**: Track and flag domains involved in phishing campaigns.

## Disclaimer

This tool is provided "as-is" for educational and research purposes. Always:
- Verify the status of URLs independently.
- Exercise caution when interacting with listed domains.
- Follow platform ToS (Terms of Service) when investigating accounts.

## Contributing

Contributions are welcome! If you would like to contribute:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.