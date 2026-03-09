# Discord Automation 🤖

A GitHub Actions-powered bot that automatically sends daily greetings with live weather information to a Discord channel via webhook.

## Features

- 📅 Sends time-based greetings throughout the day:
  - 🌅 **Good Morning** (08:00 – 09:00)
  - 🌤️ **Good Afternoon** (12:00 – 13:00)
  - 🌆 **Good Evening** (17:00 – 18:00)
  - 🌃 **Good Night** (21:00 – 22:00)
- 🌡️ Includes real-time weather for **Subang, Malaysia** (temperature + weather icon)
- ⏰ Displays the current day, date, and time (Malaysia Time, UTC+8)
- 🔒 Deduplication guard — each greeting is sent only once per day
- ⚡ Runs automatically every 5 minutes via GitHub Actions (only posts during the greeting windows)

## How It Works

```
GitHub Actions (cron every 5 min)
        │
        ▼
  script.py runs
        │
        ├── Fetches current weather from Open-Meteo API
        ├── Checks current Malaysia time
        ├── Determines if it's a greeting window (morning/afternoon/evening/night)
        ├── Checks last_sent.txt to avoid duplicate messages
        └── POSTs message to Discord Webhook
```

## Example Discord Message

```
🌅 Good Morning!

📅 Monday, 09 March 2026
⏰ 08:05
🌤 Subang 27°C

Have a great day everyone 🚀
```

## Setup

### 1. Create a Discord Webhook

1. Open your Discord server.
2. Go to **Channel Settings → Integrations → Webhooks**.
3. Click **New Webhook**, give it a name (e.g. `MAKAN`), and copy the webhook URL.

### 2. Add the Webhook URL as a GitHub Secret

1. In your repository, go to **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**.
3. Name it `DISCORD_WEBHOOK` and paste the webhook URL as the value.

### 3. Enable GitHub Actions

GitHub Actions is already configured in `.github/workflows/morning.yml`. Once the secret is set, the workflow will run automatically on schedule.

You can also trigger it manually from the **Actions** tab using the **workflow_dispatch** option.

## Project Structure

```
discord-automation/
├── .github/
│   └── workflows/
│       └── morning.yml   # GitHub Actions workflow (runs every 5 min)
├── script.py             # Main automation script
└── README.md
```

## Dependencies

| Package    | Purpose                        |
|------------|--------------------------------|
| `requests` | HTTP calls (weather API + Discord webhook) |
| `pytz`     | Timezone handling (Asia/Kuala_Lumpur) |

Dependencies are installed automatically by the GitHub Actions workflow.

## Local Development

```bash
# Install dependencies
pip install requests pytz

# Set the webhook URL
export DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."

# Run the script
python script.py
```

## Weather API

Weather data is provided by [Open-Meteo](https://open-meteo.com/) — a free, open-source weather API. No API key required.

The location is set to **Subang, Selangor, Malaysia** (latitude `3.043`, longitude `101.580`).

## License

This project is open source and available under the [MIT License](LICENSE).
