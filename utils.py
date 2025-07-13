WEATHER_EMOJI = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Smoke": "💨",
    "Haze": "🌫️",
    "Dust": "🌪️",
    "Fog": "🌁",
    "Sand": "🏜️",
    "Ash": "🌋",
    "Squall": "🌬️",
    "Tornado": "🌪️"
}

def get_unit_label(unit: str) -> str:
    return f'\u00B0{"C" if unit == 'metric' else "F"}'

