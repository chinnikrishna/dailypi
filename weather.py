import requests
from config import CONFIG
from pprint import pprint

class Weather:
    def __init__(self):                
        self.currw_url = f"https://api.openweathermap.org/data/2.5/weather?lat={CONFIG.LAT}&lon={CONFIG.LON}&appid={CONFIG.WEATHER_API_KEY}"
        self.airq_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={CONFIG.LAT}&lon={CONFIG.LON}&appid={CONFIG.WEATHER_API_KEY}"
        
    def get_weather_data(self):
        return self.make_request(self.currw_url)
    
    def get_air_data(self):
        return self.make_request(self.airq_url)
    
    def make_request(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")

if __name__ == '__main__':
    weather = Weather()
    print(weather.get_air_data())
    print(weather.get_weather_data())

