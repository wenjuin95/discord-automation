import requests
from datetime import datetime
import os

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

# ---------- WEATHER ----------
weather = requests.get(
    "https://api.open-meteo.com/v1/forecast?latitude=3.043&longitude=101.580&current_weather=true"
).json()

temp = weather["current_weather"]["temperature"]

# ---------- QUOTE ----------
try:
	quote_data = requests.get("https://api.quotable.io/random").json()
	quote = quote_data["content"]
	author = quote_data["author"]
except:
	quote = "No quote available today"
	author = ""

# ---------- DATE ----------
now = datetime.now()
day = now.strftime("%A")
date = now.strftime("%d %B %Y")
time = now.strftime("%H:%M")

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
