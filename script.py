from datetime import datetime, timedelta
import pytz
import requests
import os

tz = pytz.timezone("Asia/Kuala_Lumpur")
now = datetime.now(tz)

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

# ---------- WEATHER ----------
weather = requests.get(
    "https://api.open-meteo.com/v1/forecast?latitude=3.043&longitude=101.580&current_weather=true"
).json()

temp = weather["current_weather"]["temperature"]

# ---------- DATE ----------
# Malaysia timezone offset
MYT_OFFSET = 8

now_utc = datetime.utcnow()
now_myt = now_utc + timedelta(hours=MYT_OFFSET)
day = now_myt.strftime("%A")
date = now_myt.strftime("%d %B %Y")
time = now_myt.strftime("%H:%M")

# ---------- MESSAGE ----------
message = f"""
🌞 **Good Morning!**

📅 {day}, {date}
⏰ {time}
🌤 Subang {temp}°C

Have a great day everyone 🚀
"""

# Only allow 09:00–09:04
if now.hour == 9 and now.minute < 5:
    requests.post(os.environ["DISCORD_WEBHOOK"], json={
		"username": "Morning bot"
        "content": "Good morning!"
    })
    print("Message sent")
else:
    print("Not the correct time")
