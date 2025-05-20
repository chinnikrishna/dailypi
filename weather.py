import requests
from datetime import datetime, timedelta, timezone
from config import CONFIG

class Weather:
    def __init__(self):   
        self.currw_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={CONFIG.LAT}&lon={CONFIG.LON}&exclude=minutely,hourly,daily&appid={CONFIG.WEATHER_API_KEY}&units=metric"             
        self.city_url = f"https://api.openweathermap.org/data/2.5/weather?lat={CONFIG.LAT}&lon={CONFIG.LON}&appid={CONFIG.WEATHER_API_KEY}&units=metric"
        self.airq_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={CONFIG.LAT}&lon={CONFIG.LON}&appid={CONFIG.WEATHER_API_KEY}&units=metric"
        
    def get_data(self):
        weather_data = self.get_weather_data()
        city_data = self.make_request(self.city_url)
        air_data = self.get_air_data()
        timezone_offset = weather_data['timezone_offset']
        final_data = {
            'city': city_data['name'],
            'icon': weather_data['current']['weather'][0]['icon'],
            'temperature': round(weather_data['current']['temp']),
            'feels_like': round(weather_data['current']['feels_like']),
            'sunrise': self.convert_time(weather_data['current']['sunrise'], 
                                         timezone_offset),
            'sunset': self.convert_time(weather_data['current']['sunset'], 
                                         timezone_offset),
            'humidity': weather_data['current']['humidity'],
            'pressure': weather_data['current']['pressure'],
            'visibility': weather_data['current']['visibility'],
            'wind_speed': weather_data['current']['wind_speed'],
            'air_quality_text': air_data['list'][0]['main']['aqi'],
            'uv_index': weather_data['current']['uvi']
        }
        return final_data
    
    def convert_time(self, timestamp, timezone_offset):
        utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        tz = timezone(timedelta(seconds=timezone_offset))
        local_time = utc_time.astimezone(tz)
        return local_time.strftime("%-I:%M")
    


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

