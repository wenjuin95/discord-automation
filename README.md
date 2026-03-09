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

## Setup On Github Action

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

- **Python**
- **pip**

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

### 5. Schedule with Crontab (macOS / Linux)

To replicate the GitHub Actions schedule locally, use **crontab** to run the script automatically every 5 minutes.

**Open the crontab editor:**

```bash
crontab -e
```

**Add the following line**, replacing the paths with your actual Python executable and project directory:

```cron
*/5 * * * * DISCORD_WEBHOOK="https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN" /usr/bin/python3 /path/to/discord-automation/script.py >> /path/to/discord-automation/cron.log 2>&1
```

> **Tip:** Run `which python3` to find your Python path, and `pwd` inside the project folder to get the full path.

**Verify the crontab was saved:**

```bash
crontab -l
```

You should see the entry you just added. The script will now run every 5 minutes and log output to `cron.log`.

**To stop the scheduled job**, open `crontab -e` again and delete or comment out the line.

#### Windows — Task Scheduler

Windows does not have crontab. Use **Task Scheduler** instead:

1. Open **Task Scheduler** (search for it in the Start menu).
2. Click **Create Basic Task…** and give it a name (e.g. `Discord Automation`).
3. Set the trigger to **Daily**, then edit the trigger to repeat every **5 minutes** for a duration of **1 day**.
4. Set the action to **Start a program**:
   - Program: `python` (or the full path, e.g. `C:\Python311\python.exe`)
   - Arguments: `C:\path\to\discord-automation\script.py`
   - Start in: `C:\path\to\discord-automation`
5. In **Properties → Environment Variables** (or a wrapper `.bat` file), set `DISCORD_WEBHOOK` to your webhook URL.
6. Click **Finish**.

### Notes

- The deduplication state is stored in `last_sent.txt` in the project root. Delete this file to force-resend a greeting during testing.
- Weather data is fetched live from the [Open-Meteo API](https://open-meteo.com/) — no API key is required.
- To test outside of a greeting window, temporarily adjust the hour-checking conditions in `script.py` to match the current time.

## Weather API

Weather data is provided by [Open-Meteo](https://open-meteo.com/) — a free, open-source weather API. No API key required.

The location is set to **Subang, Selangor, Malaysia** (latitude `3.043`, longitude `101.580`).
