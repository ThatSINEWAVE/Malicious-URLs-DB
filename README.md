<div align="center">

# [Malicious URLs & Accounts DB](https://thatsinewave.github.io/Malicious-URLs-DB/)

![Banner](https://raw.githubusercontent.com/ThatSINEWAVE/Malicious-URLs-DB/refs/heads/main/.github/SCREENSHOTS/Malicious-URLs-DB.png)

A comprehensive security dashboard tracking malicious activities with advanced analytics capabilities

</div>

## Enhanced Features

### Progressive Web App (PWA) Support

- **Full PWA Implementation** with:
  - Web App Manifest for native installation
  - 30+ platform-specific icons (iOS/Android/Windows)
  - Desktop/mobile screenshots for app stores
  - Dark/light theme adaptation
  - Standalone display mode

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

## Technical Highlights

### PWA Architecture

- **Web Manifest** with:
  - 25+ icon configurations for all platforms
  - Theme color synchronization
  - Splash screen support
  - Installation metadata
- **Service Worker Ready** structure
- **App-like Navigation** with sticky elements

### Security Infrastructure

- **Automated Testing Suite**:
  - `Discord-Invite-Tester.py`: Specialized Discord link validator
  - `URL-Tester.py`: Bulk URL checker with geolocation
  - `Number-Editor.py`: Data normalization tool
  - `XLSX-to-JSON.py`: Data importer tool
- **Data Integrity Checks**:
  - Case number validation
  - URL domain parsing
  - Automatic status updates
  - Regional attribution system

### Visualization Engine

- **Dynamic Theme Support**:
  - Chart recoloring for dark/light modes
  - localStorage theme persistence (Planned)
  - Automatic contrast adjustment
- **Smart Data Binding**:
  - Real-time filter propagation
  - Responsive chart destruction/regeneration
  - Percentage-based tooltip calculations

## Complete Tool Suite

| Tool                       | Purpose                | Key Features                                          |
|----------------------------|------------------------|-------------------------------------------------------|
| `Discord-Invite-Tester.py` | Validate Discord links | API integration, Rate limiting, Status tracking       |
| `URL-Tester.py`            | Bulk URL analysis      | IP geolocation, Redirect tracking, Domain parsing     |
| `Number-Editor.py`         | Data normalization     | Case number sequencing, UTF-8 preservation            |
| `XLSX-to-JSON.py`          | Data import            | Excel conversion, Domain extraction, Field validation |

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
    └── 🔒 Compromised-Discord-Accounts.json      # Backup copy of dataset that is used in edits
```

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

## Deployment Options

### PWA Installation

1. Visit [Live Demo](https://thatsinewave.github.io/Malicious-URLs-DB/)
2. Click "Install" in browser controls (Chrome/Edge on desktop or mobile)
3. Launch as a standalone application
4. 
### Development Setup

```bash
git clone https://github.com/ThatSINEWAVE/Malicious-URLs-DB.git
cd docs && python3 -m http.server 8000
```
Access via `http://localhost:8000`

## Data Lifecycle

1. **Import** via XLSX-to-JSON.py
2. **Normalize** with Number-Editor.py
3. **Validate** using URL-Tester.py
4. **Monitor** with Discord-Invite-Tester.py
5. **Visualize** in web dashboard

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Compliance Features

- **GDPR-ready Data Handling**:
  - Anonymous tracking IDs
  - No persistent user data
- **CSP-Compatible Structure**
- **Accessibility**:
  - Screen reader support
  - Keyboard navigation
  - Color contrast compliance

## Maintenance Protocols

These are the procedures followed by Cybersight Security team members during project updates.

1. Weekly automated URL testing
2. Bi-weekly data normalization
3. Monthly PWA validation
4. Quarterly icon set updates

## Contributing

Contributions are welcome! If you would like to contribute:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.