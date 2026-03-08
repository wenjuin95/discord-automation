from datetime import datetime
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
code = weather["current_weather"]["weathercode"]

# ---------- TIME ----------
day = now.strftime("%A")
date = now.strftime("%d %B %Y")
time = now.strftime("%H:%M")

# ---------- FUNCTION ----------
def weather_icon(code):
    if code == 0:
        return "☀️"   # clear sky
    elif code in [1, 2]:
        return "🌤"   # partly cloudy
    elif code == 3:
        return "☁️"   # cloudy
    elif code in [45, 48]:
        return "🌫"   # fog
    elif code in [51, 53, 55, 61, 63, 65]:
        return "🌧"   # rain
    elif code in [71, 73, 75]:
        return "❄️"   # snow
    elif code in [95, 96, 99]:
        return "⛈"   # thunderstorm
    else:
        return "🌡"

# ---------- MESSAGE ----------
icon = weather_icon(code)

message = f"""
📅 {day}, {date}
⏰ {time}
{icon} Subang {temp}°C

Have a great day everyone 🚀
"""

greeting = None
tag = None

if 8 <= now.hour < 9:
    greeting = "🌅 **Good Morning!**"
    tag = "morning"
elif 12 <= now.hour < 13:
    greeting = "🌤️ **Good Afternoon!**"
    tag = "afternoon"
elif 17 <= now.hour < 18:
    greeting = "🌆 **Good Evening!**"
    tag = "evening"
elif 21 <= now.hour < 22:
    greeting = "🌃 **Good Night!**"
    tag = "night"

if greeting:
    today = now.strftime("%Y-%m-%d")
    state_file = "last_sent.txt"

    last = ""
    if os.path.exists(state_file):
        with open(state_file) as f:
            last = f.read().strip()

    current = f"{today}-{tag}"

    if last != current:
        requests.post(
            WEBHOOK_URL,
            json={"username": "MAKAN", "content": greeting + message},
        )
        print("Message sent")

        with open(state_file, "w") as f:
            f.write(current)
    else:
        print("Already sent today")
else:
    print("Not the correct time")
#requests.post(
#    os.environ["DISCORD_WEBHOOK"],
#    json={"username": "MAKAN", "content": message},
#)
#print("Message sent")