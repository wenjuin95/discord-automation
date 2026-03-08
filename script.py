from datetime import datetime, timedelta
import requests
import os

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

requests.post(WEBHOOK_URL, json={
	"username": "Morning Bot",
	"content": message
})
print("Message sent to Discord!")
