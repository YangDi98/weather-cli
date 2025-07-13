import argparse
import requests

from typing import Optional
from requests import RequestException
from datetime import datetime

from config import WEATHER_API_KEY, WEATHER_API
from utils import WEATHER_EMOJI, get_unit_label

def take_argument():
    parser = argparse.ArgumentParser(
        prog='MyWeatherCli'
    )
    parser.add_argument('--city', required=True)
    parser.add_argument('--country', required=False)
    parser.add_argument('--unit', required=False, choices=['metric', 'imperial'])
    parser.add_argument('-f', '--forecast', action="store_true")
    args = parser.parse_args()
    return args

def get_coordinates(city: str, country: Optional[str] = None) -> Optional[dict[str, float]]:
    params = { 
        'appid': WEATHER_API_KEY,
        'q': f'{city},{country}' if country else city,
        'limit': 1,
    }
    try:
        res = requests.get(f'{WEATHER_API}/geo/1.0/direct', params=params)
        res.raise_for_status()
    except RequestException:
        print('something went wrong when trying to fetch location')
        return
    locations = res.json()
    if len(locations) == 0:
        print(f'Cannot find coordinates for {city},{country}')
        return
    location = locations[0]
    return {
        'lat': location.get('lat'),
        'lon': location.get('lon'),
    }

def get_weather(lat: float, lon: float, unit: str) -> Optional[dict [str, str]]:
    unit_label = get_unit_label(unit)
    params = {
        'appid': WEATHER_API_KEY,
        'lat': lat,
        'lon': lon,
        'units': unit
    }
    try:
        res = requests.get(f'{WEATHER_API}/data/2.5/weather', params=params)
        res.raise_for_status()
        data = res.json()
        weather_info = {
            'icon': WEATHER_EMOJI.get(data['weather'][0]['main'], "❓"),
            'description': data['weather'][0]['description'],
            'temp': f"{data['main']['temp']}{unit_label}",
            'feels_like': f"{data['main']['feels_like']}{unit_label}"
        }
        return weather_info
    except RequestException:
        print('Something went wrong when trying to fetch weather')

def get_forecast(lat: float, lon: float, unit: str) -> Optional[dict [str, str]]:
    unit_label = get_unit_label(unit)
    params = {
        'appid': WEATHER_API_KEY,
        'lat': lat,
        'lon': lon,
        'units': unit,
        'cnt': 3
    }
    try:
        res = requests.get(f'{WEATHER_API}/data/2.5/forecast', params=params)
        res.raise_for_status()
        data = res.json()
        forecast = data.get('list', [])
        for day_forecast in forecast:
            datetime_obj = datetime.fromtimestamp(day_forecast['dt'])
            datetime_str = datetime_obj.strftime("%Y-%m-%d %H")
            min_temp = f'{day_forecast['main']['temp_min']}{unit_label}'
            max_temp = f'{day_forecast['main']['temp_max']}{unit_label}'
            description = day_forecast['weather'][0]['description']
            icon = WEATHER_EMOJI.get(day_forecast['weather'][0]['main'],"❓")
            print(f'{datetime_str}:00:\t {icon}  {description} \tMax {max_temp} \tMin {min_temp}')
    except RequestException:
        print('Something went wrong when trying to fetch forecast')
    
    
def main():
    args = take_argument()
    coordinates = get_coordinates(args.city, args.country) 
    if not coordinates:
        return
    unit = args.unit if args.unit else 'metric'
    current_weather = get_weather(coordinates['lat'], coordinates['lon'], unit)
    if not current_weather:
        return
    location_name_str = f'{args.city},{args.country}' if args.country else args.city
    print(f'Weather in {location_name_str}')
    print(f"{current_weather['icon']}\t{current_weather['description']}, temperature {current_weather['temp']}, feels like {current_weather['feels_like']}")
    if args.forecast:
        get_forecast(coordinates['lat'], coordinates['lon'], unit)
    

if __name__ == '__main__':
    main()