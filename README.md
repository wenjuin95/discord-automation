# Discord Automation

A GitHub Actions-powered bot that automatically sends daily greetings with live weather information to a Discord channel via webhook.

## Features

- 📅 Sends time-based greetings throughout the day
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

## Setup

### 1. Create a Discord Webhook

1. Open your Discord server.
2. Go to **Channel Settings → Integrations → Webhooks**.
3. Click **New Webhook**, give it a name (e.g. `Test`), and copy the webhook URL.

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

## Local Setup Guide

Follow these steps to run the bot on your local machine for development or testing.

### Prerequisites

- **Python 3.8+** — [Download Python](https://www.python.org/downloads/)
- **pip** — usually bundled with Python
- A **Discord Webhook URL** — see the [Setup](#setup) section above to create one

### 1. Clone the Repository

```bash
git clone https://github.com/wenjuin95/discord-automation.git
cd discord-automation
```

### 2. Install Dependencies

```bash
pip install requests pytz
```

### 3. Configure the Webhook URL

Set the `DISCORD_WEBHOOK` environment variable to your Discord webhook URL.

**macOS / Linux:**

```bash
export DISCORD_WEBHOOK="https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"
```

**Windows (Command Prompt):**

```cmd
set DISCORD_WEBHOOK=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
```

**Windows (PowerShell):**

```powershell
$env:DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"
```

### 4. Run the Script

```bash
python script.py
```

### Expected Output

The script checks the current Malaysia Time (UTC+8) and behaves as follows:

| Scenario | Console output |
|---|---|
| Inside a greeting window and message not yet sent today | `Message sent` |
| Inside a greeting window but message already sent today | `Already sent today` |
| Outside all greeting windows | `Not the correct time` |

> **Greeting windows** are: 08:00–08:59 (Morning), 12:00–12:59 (Afternoon), 17:00–17:59 (Evening), 21:00–21:59 (Night) — all in Malaysia Time.

### Notes

- The deduplication state is stored in `last_sent.txt` in the project root. Delete this file to force-resend a greeting during testing.
- Weather data is fetched live from the [Open-Meteo API](https://open-meteo.com/) — no API key is required.
- To test outside of a greeting window, temporarily adjust the hour-checking conditions in `script.py` to match the current time.

## Weather API

Weather data is provided by [Open-Meteo](https://open-meteo.com/) — a free, open-source weather API. No API key required.

The location is set to **Subang, Selangor, Malaysia** (latitude `3.043`, longitude `101.580`).
