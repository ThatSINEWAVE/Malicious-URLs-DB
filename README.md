<div align="center">

# [Malicious URLs & Accounts DB](https://thatsinewave.github.io/Malicious-URLs-DB/)

![Banner](https://raw.githubusercontent.com/ThatSINEWAVE/Malicious-URLs-DB/refs/heads/main/.github/SCREENSHOTS/Malicious-URLs-DB.png)

A web-based dashboard tracking compromised Discord accounts involved in phishing campaigns and malicious activities

</div>

## Repository Structure

```
├── docs/
│   ├── index.html            # Main web interface
│   ├── styles.css            # Dashboard styling
│   ├── script.js             # Interactive dashboard logic
│   ├── dayjs.min.js         # Date handling library
│   └── chart.min.js         # Chart.js library for visualizations
├── data/
│   └── Compromised-Discord-Accounts.json  # Primary dataset of compromised accounts
└── Tool/
    ├── XLSX-to-JSON.py      # Excel to JSON converter
    ├── URL-Tester.py        # Mass tester for URLs using IPInfo API
    ├── Number-Editor.py     # Script to edit case numbers
    ├── Discord-Invite-Tester.py # Test tool for Discord invites
    ├── ExporterSheet.xlsx   # Exported Excel file from private Google sheet
    └── Compromised-Discord-Accounts.json    # Backup copy of primary dataset
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

| Field          | Description                     |
|----------------|---------------------------------|
| CASE_NUMBER    | Unique case identifier          |
| FOUND_ON       | Discovery date                  |
| DISCORD_ID     | User's Discord Snowflake ID     |
| USERNAME       | Account username                |
| BEHAVIOUR      | Suspicious activity description |
| ATTACK_METHOD  | Primary attack technique        |
| ATTACK_VECTOR  | Implementation method           |
| ATTACK_GOAL    | Campaign objective              |
| ATTACK_SURFACE | Targeted platform/service       |
| SURFACE_URL    | Initial phishing URL            |
| FINAL_URL      | Endpoint malicious URL          |

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