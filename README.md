<div align="center">

# [Malicious URLs & Accounts DB](https://thatsinewave.github.io/Malicious-URLs-DB/)

![Banner](https://raw.githubusercontent.com/ThatSINEWAVE/Malicious-URLs-DB/refs/heads/main/.github/SCREENSHOTS/Malicious-URLs-DB.png)

A comprehensive security dashboard tracking malicious activities with advanced analytics capabilities and unified processing engine

</div>

## Enhanced Features

### Progressive Web App (PWA) Support

- **Full PWA Implementation** with:
  - Web App Manifest for native installation
  - 30+ platform-specific icons (iOS/Android/Windows)
  - Desktop/mobile screenshots for app stores
  - Dark/light theme adaptation
  - Standalone display mode
  - Dynamic risk level indicators
  - API status monitoring panel
  - Cached invite status display
  - Username character analysis
  - Last check timestamp tracking
  - Dual-layer URL validation status

### Advanced Visualization Suite

- **10 Interactive Charts** including:
  - Attack timeline with date filtering
  - Method distribution (doughnut/pie charts)
  - Geographic origin analysis
  - Behavior type classification
  - Attack vector breakdown
  - URL status comparison (surface vs final)
  - Attack surface distribution
  - Attack goal distribution
  - Compromised account status
  - Method vs goal matrix analysis
  - Non-ASCII username tracker
  - VirusTotal check timestamps
  - Regional attribution mapping
  - URL status lifecycle tracking (planned)
  - API call metrics monitoring
  - Username change history (planned)

### Intelligent Data Handling

- **Dynamic Risk Assessment** with color-coded status:
  - Real-time Active URL counter with risk level indicators (Low/Med/High/Critical)
  - Auto-updating "Most Common Attack Method" and "Top Targeted Platform" stats
  - Smart date range presets based on dataset

### Unified Processing Engine

- **All-in-One Security Tool** (`Database-Checker.py`):
  - Discord invite validation with caching
  - VirusTotal API integration
  - IP geolocation tracking
  - Non-ASCII username detection
  - Automated case number sequencing
  - Dual URL checking (Surface + Final)
  - Smart rate limiting (Discord/VirusTotal APIs)
  - Real-time data persistence
  - Comprehensive logging system

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Technical Highlights

### PWA Architecture

- **Web Manifest** with:
  - 25+ icon configurations for all platforms
  - Theme color synchronization
  - Splash screen support
  - Installation metadata
- **Service Worker Ready** structure
- **App-like Navigation** with sticky elements

### Visualization Engine

- **Dynamic Theme Support**:
  - Chart recoloring for dark/light modes
  - localStorage theme persistence (Planned)
  - Automatic contrast adjustment
- **Smart Data Binding**:
  - Real-time filter propagation
  - Responsive chart destruction/regeneration
  - Percentage-based tooltip calculations

### Core Processing Engine

- **Unified Security Tool**:
  - Integrated Discord API handling
  - VirusTotal malicious URL detection
  - IPInfo geolocation services
  - Automated username normalization
  - Configurable rate limits
  - Multi-API error handling
  - Compressed Base64 URL encoding

### Advanced Data Management

- **Enhanced JSON Schema**:
  - `NON_ASCII_USERNAME` flag
  - `LAST_VT_CHECK` timestamps
  - Dual URL status tracking
  - Automated case numbering
  - Regional attribution system
  - API call counters

### Security Infrastructure

- **Protection Mechanisms**:
  - Request throttling (20/sec Discord, 4/min VirusTotal)
  - Automatic API token validation
  - Immediate disk writes for audit trails
  - Invite status caching system
  - Automatic username synchronization
  - Multi-layer URL validation

## Complete Tool Integration

The `Database-Checker.py` tool represents a significant advancement in our threat detection capabilities, combining previously separate utilities into one powerful security engine. This Python script offers an intelligent multi-API orchestration layer that maintains optimal performance while respecting rate limits of external services.

Key capabilities include:
- **Smart API Management**: Automated token rotation and request throttling to prevent API lockouts
- **Parallel Processing**: Concurrent validation of surface and final URLs for faster analysis
- **Persistent Caching**: Memory-efficient storage of Discord invite validations to reduce API calls
- **Intelligent Retry Logic**: Exponential backoff for failed requests with customizable parameters
- **Comprehensive Reporting**: Real-time terminal output and structured JSON logging for audit trails

The tool implements a robust state machine that tracks the complete lifecycle of each malicious URL, from initial detection through validation to final disposition. Every action is meticulously logged with timestamps and attribution information, creating a detailed forensic record that can be used for trend analysis and incident response.

| Feature                      | Implementation         | Key Technologies                          |
|------------------------------|------------------------|-------------------------------------------|
| Unified Processing           | Database-Checker.py    | Requests, VirusTotal API, Discord API     |
| Data Validation              | Built-in checks        | Unicode normalization, Base64 encoding    |
| Threat Intelligence          | Integrated APIs        | IPInfo, VirusTotal, Discord API           |
| Persistent Logging           | Rotating log system    | Python logging, Immediate fsync           |
| Rate Limit Management        | Adaptive throttling    | Time.perf_counter, Request tracking       |


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
    ├── 📜 Database-Checker.py                    # Unified processing engine
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
| NON_ASCII_USERNAME         | Boolean     | Unicode character detection flag         | true                               |
| LAST_VT_CHECK              | ISO 8601    | Last VirusTotal verification timestamp   | 2025-03-11T14:28:33Z               |
| ACCOUNT_STATUS             | Enum        | Account investigation status             | COMPROMISED                        |
| SURFACE_URL_STATUS         | Enum        | URL status with Discord checks           | ACTIVE                             |
| FINAL_URL_STATUS           | Enum        | URL status with VT verification          | INACTIVE                           |
| INVITE_CACHE               | Object      | Cached Discord invite statuses           | 2025-03-11T12:45:19Z               |

## Deployment Options

### PWA Installation

1. Visit [Live Demo](https://thatsinewave.github.io/Malicious-URLs-DB/)
2. Click "Install" in browser controls (Chrome/Edge on desktop or mobile)
3. Launch as a standalone application

## Data Lifecycle

1. **Import** via XLSX-to-JSON.py
2. **Automated Collection** via Database-Checker.py
3. **API Validation** (Discord + VirusTotal)
4. **Geolocation Tagging**
5. **Username Analysis**
6. **Real-Time Dashboard Updates**

<div align="center">

## [Join my discord server](https://discord.gg/2nHHHBWNDw)

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
- **Extended Security**:
  - API token encryption
  - Request signature validation
  - Audit trail preservation
  - Memory-safe operations
- **Privacy Features**:
  - Anonymized logging
  - Data minimization
  - Secure token handling

## Maintenance Protocols

1. Daily automated API checks
2. Weekly log rotation
3. Monthly cache purges
4. Quarterly schema validation
5. Bi-annual rate limit audits

## Contributing

Contributions are welcome! If you would like to contribute:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request.

This project welcomes contributions through:
- API service integrations
- Enhanced visualization modules
- Localization support
- Additional security checks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.