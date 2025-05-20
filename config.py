import os


class CONFIG:
    WEATHER_API_KEY = ""
    LAT = 37.3394
    LON = -121.895
    WEATHER_UPDATE_INTERVAL = 1800
    RETRY_INTERVAL = 60
    OUTPUT_DIR = "screenshots"
    FLASK_PORT = 8085
    EPAPER_PALETTE = [
        (0, 0, 0),       # Black
        (255, 255, 255), # White
        (255, 0, 0),     # Red
        (0, 255, 0),     # Green
        (0, 255, 255),   # Blue
        (255, 0, 255),   # Yellow        
        (255, 255, 0),   # Orange
        
    ]

