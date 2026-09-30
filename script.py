import os
from dotenv import load_dotenv
from datetime import datetime
import pytz
import requests
from google import genai

load_dotenv()

tz = pytz.timezone("Asia/Kuala_Lumpur")
now = datetime.now(tz)

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# ---------- CONSTANTS & MAPPINGS ----------
LAT, LON = 3.0438, 101.5806 # Subang Jaya

WX = {
    0: "Clear", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Fog", 51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain", 80: "Showers",
    81: "Showers", 82: "Violent showers", 95: "Thunderstorm",
    96: "Thunderstorm", 99: "Thunderstorm"
}

def get_aqi_label(v):
    if v <= 50: return "Good"
    if v <= 100: return "Moderate"
    if v <= 150: return "Unhealthy for sensitive groups"
    if v <= 200: return "Unhealthy"
    if v <= 300: return "Very unhealthy"
    return "Hazardous"

def get_weather_icon(code):
    match code:
        case 0 | 1: return "☀️"
        case 2 | 3: return "☁️"
        case 45 | 48: return "🌫️"
        case 51 | 53 | 55 | 61 | 63 | 65 | 80 | 81 | 82: return "🌧️"
        case 95 | 96 | 99: return "⛈️"
        case _: return "🌡️"

# ---------- 1. DETERMINE TIME & GREETING ----------
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

# Only proceed if it is the correct time
if greeting:
    today = now.strftime("%Y-%m-%d")
    state_file = "last_sent.txt"
    current_state = f"{today}-{tag}"

    # Check if we already sent it today for this time block
    if os.path.exists(state_file):
        with open(state_file) as f:
            if f.read().strip() == current_state:
                print(f"Message for {tag} already sent today.")
                exit()

    # ---------- 2. FETCH WEATHER & AQI ----------
    try:
        w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,weather_code&timezone=Asia%2FKuala_Lumpur").json()
        a_res = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={LAT}&longitude={LON}&current=us_aqi&timezone=Asia%2FKuala_Lumpur").json()

        cur_w = w_res.get("current", {})
        temp = round(cur_w.get("temperature_2m", 0))
        wx_code = cur_w.get("weather_code", -1)
        wx_text = WX.get(wx_code, "Unknown")

        cur_a = a_res.get("current", {})
        aqi_val = round(cur_a.get("us_aqi", 0))
        aqi_label = get_aqi_label(aqi_val)
    except Exception as e:
        print(f"Error fetching data: {e}")
        temp, wx_code, wx_text, aqi_val, aqi_label = 0, -1, "Error", 0, "Unknown"

    # ---------- 3. GET GEMINI ADVICE ----------
    advice = ""
    if GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = (
                f"You are MAKAN, a friendly Discord bot for a community in Subang Jaya. "
                f"It is currently the {tag}. "
                f"The weather is {temp}°C, with {wx_text}. "
                f"The Air Quality Index is {aqi_val} ({aqi_label}). "
                f"Write 1-2 short, punchy sentences of friendly advice for the users based on these specific conditions. "
                f"Do not include greetings like 'Good morning'. Use an appropriate emoji."
            )
            response = client.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=prompt
            )
            advice = f"\n💡 **Maka.vis Advice:** {response.text.strip()}\n"
        except Exception as e:
            print(f"Gemini API error: {e}")

    # ---------- 4. BUILD & SEND MESSAGE ----------
    day = now.strftime("%A")
    date = now.strftime("%d %B %Y")
    time_str = now.strftime("%H:%M")
    icon = get_weather_icon(wx_code)

    message = f"""{greeting}
📅 {day}, {date}
⏰ {time_str}

{icon}  **Subang Jaya Weather**
🌡️  Temp: {temp}°C
🌬️  AQI: {aqi_val} ({aqi_label})
{advice}
Have a great day everyone 🚀
"""

    print(message)

    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"username": "MAKAN", "content": message})
        print("Webhook sent successfully.")

        # Save state to prevent duplicate sending
        with open(state_file, "w") as f:
            f.write(current_state)
    else:
        print("DISCORD_WEBHOOK environment variable not set. Message not sent.")

else:
    print("Not the correct time. Exiting script.")
