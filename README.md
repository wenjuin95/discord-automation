# Discord Automation

An automation script that sends scheduled daily greetings, live weather, Air Quality Index (AQI) reports, and AI-powered lifestyle advice to a Discord channel via webhook.

---

## Features

- 📅 **Scheduled Greetings:** Automatically posts time-based messages (Morning, Afternoon, Evening, Night).
- 🌡️ **Live Weather & AQI:** Fetches real-time temperature, humidity, weather conditions, and US AQI levels for **Subang Jaya, Malaysia** via Open-Meteo.
- 💡 **Gemini AI Advisor:** Uses Google Gemini to generate context-aware, practical advice based on live weather and air quality conditions.
- ⏰ **Localized Time:** Accurately pinned to Malaysia Time (Asia/Kuala_Lumpur, UTC+8).
- 🔒 **Deduplication Guard:** Prevents duplicate postings within the same time window using a local state file (`last_sent.txt`).
- ⚙️ **Automated Execution:** Runs on schedule using system `cron` or Task Scheduler.

---

## How It Works

```
System Cron (e.g., hourly)
│
▼
script.py
│
├── Checks current Malaysia time (UTC+8)
├── Identifies if it's within a greeting window
├── Reads last_sent.txt (exits early if already sent)
│
├── Fetches Weather & AQI from Open-Meteo APIs
├── Sends environmental data to Gemini
├── Receives concise AI advisory message
│
├── POSTs final formatted embed/message to Discord Webhook
└── Updates last_sent.txt with current state
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP requests to Open-Meteo and Discord Webhooks |
| `pytz` | Timezone management (`Asia/Kuala_Lumpur`) |
| `google-genai` | Official Google GenAI SDK for Gemini models |
| `python-dotenv` | Loads API keys and configurations from `.env` |

---

## Prerequisites

- Python 3.10+
- PIP
- A Discord server with webhook permissions
- A Google Gemini API key

---

## Local Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/wenjuin95/discord-automation.git
cd discord-automation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```
.env.example -> .env
```
Add your credentials
```
DISCORD_WEBHOOK="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

### 5. Run Manually
Run the script directly to test:

```
python3 script.py
```
>Note: If you run outside greeting hours [8-9 AM, 12-1 PM, 5-6 PM, 9-10 PM], the script will exit without posting. Temporarily adjust the time check in script.py to test immediately

---

## Scheduling Automation

### Linux / macOS / WSL (Crontab)
Open your user crontab editor:

```
crontab -e
```
Add an entry to execute the script at the top of every hour. Make sure to use absolute paths for both your directory and your Python binary:
```
0 * * * * cd /home/yourusername/discord-automation && /usr/bin/python3 script.py >> cron.log 2>&1
```
>Tip: Find your Python executable path using which python3 and your current folder path using pwd

Verify your scheduled task:
```
crontab -l
```

### Windows (Task Scheduler)
1. Open Task Scheduler and select Create Basic Task.

2. Name it Discord Weather Bot and set Trigger to Daily.

3. Under Action, select Start a program:
	- Program/script: wsl.exe (if running inside WSL) or the path to python.exe
	- Add arguments:
		- If WSL: bash -c "cd /home/yourusername/discord-automation && /usr/bin/python3 script.py"
		- If native Windows: script.py
	- Start in: C:\path\to\discord-automation (for native Windows)

4. Finish and configure the task to run repeatedly as needed.

---

## APIs & Data Sources

- Weather & Forecast: Open-Meteo Weather Forecast API (Subang Jaya: 3.0438, 101.5806). Free, no authentication required.

- Air Quality: Open-Meteo Air Quality API providing real-time US AQI calculations.

- Intelligence: Google Gemini API using gemini-3.5-flash for fast, lightweight contextual text generation.
