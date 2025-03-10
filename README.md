<div align="center">

# [Malicious URLs & Accounts DB](https://thatsinewave.github.io/Malicious-URLs-DB/)

![Banner](https://raw.githubusercontent.com/ThatSINEWAVE/Malicious-URLs-DB/refs/heads/main/.github/SCREENSHOTS/Malicious-URLs-DB.png)

A comprehensive security dashboard tracking malicious activities with advanced analytics capabilities

</div>

## Enhanced Features

### Advanced Visualization Suite

- **8 Interactive Charts** including:
  - Attack timeline with date filtering
  - Method distribution (doughnut/pie charts)
  - Geographic origin analysis
  - Behavior type classification
  - Attack vector breakdown
  - Platform targeting trends
  - URL status comparison (surface vs final)
  - Attack surface distribution

### Intelligent Data Handling

- **Dynamic Risk Assessment** with color-coded status:
  - Real-time Active URL counter with risk level indicators (Low/Med/High/Critical)
  - Auto-updating "Most Common Attack Method" and "Top Targeted Platform" stats
  - Smart date range presets based on dataset

### Enhanced Interaction

- **Deep Filter System**:
  - Multi-criteria search (username, behavior, Discord ID, attack vector)
  - Combined date range + attack method filters
  - Persistent filter states between sessions
- **Data Exploration**:
  - Tabular data with hover tooltips
  - Case number based quick search
  - Paginated results (10 entries/page)

### Security & Usability

- **Safe Preview System**:
  - Truncated URLs with domain highlighting
  - Non-clickable malicious links
  - Status badges for quick visual assessment
- **Dark/Light Mode** with persistent theme memory
- **Announcement System** with version-aware dismissals

### Enterprise Features

- **Full Data Export**:
  - CSV export with complete dataset
  - Filter-preserved exports
  - Clean data formatting with proper escaping
- **Embeddable Components**:
  - Standalone charts with filter context
  - Stats cards for external dashboards
- **API-Ready Structure** with clean JSON data

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Technical Highlights

### Data Architecture

- **Normalized JSON Structure** with 16 standardized fields
- **Automatic Data Refresh** with GitHub raw URL integration
- **LocalStorage Optimization** for user preferences
- **Mobile-First Design** with full responsive support

### Visualization Engine

- Chart.js integration with dynamic updates
- Color-coded risk indicators
- Smart chart destruction/recreation
- Interactive data point selection
- Percentage calculations in tooltips

### Security Measures

- Content Security Policy (CSP) ready
- XSS protection through text sanitization
- Safe URL handling with domain isolation
- No external dependencies except Chart.js

## Complete Data Schema

| Field                      | Type        | Description                              | Example Value                      |
|----------------------------|-------------|------------------------------------------|------------------------------------|
| CASE_NUMBER                | Integer     | Unique investigation identifier          | 202503101                          |
| FOUND_ON                   | ISO Date    | Discovery timestamp                      | 2025-03-10T07:16:00Z               |
| DISCORD_ID                 | Snowflake   | 18-digit Discord user ID                 | 123456789012345678                 |
| USERNAME                   | String      | Current account username                 | PhishMaster_01                     |
| BEHAVIOUR                  | Text        | Observed malicious patterns              | "Mass DMing fake nitro links"      |
| ATTACK_METHOD              | Categorical | Primary attack classification            | Credential Harvesting              |
| ATTACK_VECTOR              | Categorical | Technical implementation method          | Fake Discord Nitro Portal          |
| ATTACK_GOAL                | Text        | Campaign objectives                      | Steal 2FA codes                    |
| ATTACK_SURFACE             | Categorical | Targeted platform/service                | Discord Marketplace                |
| SUSPECTED_REGION_OF_ORIGIN | Geolocation | Suspected origin region                  | Eastern Europe                     |
| SURFACE_URL                | URL         | Initial contact URL                      | https://discord-nitro[.]gift/claim |
| SURFACE_URL_DOMAIN         | Domain      | Registered domain of surface URL         | discord-nitro[.]gift               |
| SURFACE_URL_STATUS         | Enum        | Current status (ACTIVE/INACTIVE/UNKNOWN) | ACTIVE                             |
| FINAL_URL                  | URL         | Endpoint malicious URL                   | https://steallogin[.]xyz/submit    |
| FINAL_URL_DOMAIN           | Domain      | Registered domain of final URL           | steallogin[.]xyz                   |
| FINAL_URL_STATUS           | Enum        | Current status (ACTIVE/INACTIVE/UNKNOWN) | INACTIVE                           |

## Repository Structure

```markdown
├── 📂 docs/                                      # Web dashboard and assets
│   ├── 📜 index.html                             # Main web interface
│   ├── 🎨 styles.css                             # Dashboard styling
│   ├── 🎨 tailwind.min.css                       # Tailwind CSS framework
│   ├── ⚙️ script.js                              # Interactive dashboard logic
│   ├── 🕒 dayjs.min.js                           # Date handling library
│   ├── 📊 chart.min.js                           # Chart.js for visualizations
│   ├── 📂 site-data/                             # Miscellaneous site data
│   │   ├── 🔗 social-share/                      # Social sharing related assets
│   │   └── 🖼️ Malicious-URLs-DB.png              # Embed image for social sharing
│   ├── 📂 icons/                                 # Various platform icons
│   │   ├── 🤖 android-icon-*.png                 # Android icons (36x36 → 192x192)
│   │   ├── 🍏 apple-icon-*.png                   # Apple icons (57x57 → 180x180)
│   │   ├── 🏁 favicon-*.png                      # Favicons (16x16 → 96x96)
│   │   ├── 🖥️ ms-icon-*.png                      # Microsoft icons (70x70 → 310x310)
│   ├── 📝 site.manifest                          # Web app manifest
├── 📂 data/                                      # Data storage
│   └── 🔒 Compromised-Discord-Accounts.json      # Dataset of compromised accounts
└── 📂 Tools/                                     # Utility scripts
    ├── 🔄 XLSX-to-JSON.py                        # Excel to JSON converter
    ├── 🌐 URL-Tester.py                          # Bulk URL tester via IPInfo API
    ├── ✏️ Number-Editor.py                       # Script for editing case numbers
    ├── 🔍 Discord-Invite-Tester.py               # Discord invite testing tool
    ├── 📊 ExporterSheet.xlsx                     # Exported dataset from private Google Sheet
    └── 🔒 Compromised-Discord-Accounts.json  # Backup copy of dataset that is used in edits
```

## Deployment Options

### Local Development

```bash
git clone https://github.com/ThatSINEWAVE/Malicious-URLs-DB.git
cd docs && python3 -m http.server 8000
```
Access via `http://localhost:8000`

### Production Setup

1. Configure CORS headers for JSON data
2. Implement caching strategy for static assets
3. Set up automated data sync from Google Sheets
4. Enable security headers (CSP, HSTS, X-Content-Type)

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Advanced Usage

### Researcher Workflow

1. Filter by date range of interest
2. Sort by attack surface/platform
3. Export filtered dataset to CSV
4. Cross-reference with domain WHOIS data
5. Submit takedown requests for active URLs

## Security Protocols

1. **Automated URL Testing** via `URL-Tester.py`
2. **Data Sanitization** with regex patterns
3. **Version Control** for dataset changes
4. **Activity Logging** through GitHub commits
5. **Access Control** via GitHub raw URL

## Contributing

Contributions are welcome! If you would like to contribute:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.