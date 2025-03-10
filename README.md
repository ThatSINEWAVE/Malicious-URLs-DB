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
│   └── script.js             # Interactive dashboard logic
├── data/
│   └── Compromised-Discord-Accounts.json  # Primary dataset
└── Tool/
    ├── exporter_script.py    # Excel to JSON converter
    └── ExporterSheet.xlsx    # Data collection template
```

## Features

- **Dark/Light Mode Toggle** - Eye-friendly theme switching
- **Interactive Analytics** - 4 real-time charts tracking:
  - Attack timeline
  - Method distribution
  - Targeted platforms
  - Geographic origins
- **Advanced Filtering** - Search by:
  - Username/Discord ID
  - Attack method
  - Date range
- **CSV Export** - Download filtered data
- **Pagination** - 10 entries per page
- **Account Details Modal** - Full case overview

## Quick Start

1. Clone repository:
```bash
git clone https://github.com/ThatSINEWAVE/Malicious-URLs-DB.git
```

2. Host the web app:
```bash
cd docs && python3 -m http.server 8000
```

3. Access dashboard at:
`http://localhost:8000`

## 🔧 Data Management

1. Update Excel sheet in `Tool/ExporterSheet.xlsx`

2. Run exporter script:
```bash
python3 Tool/exporter_script.py
```

3. Updated JSON will be generated in root directory

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

- Real-time URL status tracking (Active/Inactive)
- Automatic data refresh button
- Visual status indicators (🔴 Active/🟢 Neutral)
- Malicious domain tracking

## Disclaimer

This tool is provided "as-is" for educational and research purposes. Always:
- Verify URL status independently
- Exercise caution when interacting with listed domains
- Follow platform ToS when investigating accounts

## Contributing

Contributions are welcome! If you want to contribute, feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.