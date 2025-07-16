from dotenv import load_dotenv

load_dotenv()

import os

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API = os.getenv("WEATHER_API")
