from datetime import datetime
import pytz # timezone handling
import requests # HTTP requests
import os # environment variables and file handling

tz = pytz.timezone("Asia/Kuala_Lumpur")
now = datetime.now(tz)
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

# ---------- WEATHER ----------
weather = requests.get(
	"https://api.data.gov.my/weather/forecast?contains=Subang@location__location_name"
).json()

for key in weather:
	today_date = datetime.now().date()
	today_hour = datetime.now().hour
	temp = key['max_temp']
	if key['date'] == str(today_date):
		if today_hour < 12:
			weather_text = key['morning_forecast']
		elif today_hour < 18:
			weather_text = key['afternoon_forecast']
		else:
			weather_text = key['night_forecast']
		break

# ---------- TIME ----------
day = now.strftime("%A")
date = now.strftime("%d %B %Y")
time = now.strftime("%H:%M")

# ---------- FUNCTION ----------
def get_weather_icon(forecast_text):
	match forecast_text:
		case "Tiada hujan":
			return "☀️ "

		case "Berjerebu":
			return "🌫️ "

		case "Hujan" | "Hujan di beberapa tempat" | "Hujan di satu dua tempat":
			return "🌧️ "

		case "Hujan di satu dua tempat di kawasan pantai" | "Hujan di satu dua tempat di kawasan pedalaman":
			return "🌦️ "

		case "Ribut petir" | "Ribut petir di beberapa tempat" | "Ribut petir di satu dua tempat":
			return "⛈️ "

		case "Ribut petir di satu dua tempat di kawasan pantai" | "Ribut petir di satu dua tempat di kawasan pedalaman":
			return "🌩️ "

		case _:
			return "🌡️ "

# ---------- MESSAGE ----------
icon = get_weather_icon(weather_text)

message = f"""
📅 {day}, {date}
⏰ {time}
{icon} Subang ({temp}°C)

Have a great day everyone 🚀
"""

# ---------- GREETING ----------
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

print(message)

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
