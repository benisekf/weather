from flask import Blueprint, render_template, request
import requests
bp = Blueprint('main', __name__)
@bp.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        print(f"Received city: {city}")  
        if city:
            weather, error = get_weather(city)
            print(f"Weather: {weather}, Error: {error}")  
    return render_template('index.html', weather=weather, error=error)
def get_weather(city):
    try:
        geocoding_api_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geocoding_response = requests.get(geocoding_api_url)
        geocoding_response.raise_for_status()
        geo_data = geocoding_response.json()
        if not geo_data or 'results' not in geo_data or not geo_data['results']:
            return None, "City not found"
        geo_data = geo_data['results'][0]
        latitude = geo_data['latitude']
        longitude = geo_data['longitude']
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if 'hourly' not in data or 'temperature_2m' not in data['hourly']:
            return None, "Weather data not found"
        weather = {
            'city': city,
            'temperature': data['hourly']['temperature_2m'][0],
        }
        return weather, None
    except requests.RequestException as e:
        print(f"RequestException: {str(e)}") 
        return None, str(e)
