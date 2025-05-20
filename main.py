import os
import time
import threading
from flask import Flask, render_template

from config import CONFIG
from weather import Weather
from display import Display

app = Flask(__name__)
display_srvc = Display()
weather_srvc = Weather()

from pkg_resources import require
print(require('gpiozero')[0].version)




@app.route('/')
def index():
    weather_data = weather_srvc.get_data()
    return render_template('index.html', weather=weather_data)

def run_flask_server():
    app.run(port=CONFIG.FLASK_PORT, debug=False)

def display_update_loop():
    display_srvc.run()


if __name__ == "__main__":
    # Create and start the Flask server thread
    server_thread = threading.Thread(target=run_flask_server)
    server_thread.daemon = True
    server_thread.start()
    print("Flask server started in background thread")


    # Create and start the display update thread
    display_thread = threading.Thread(target=display_update_loop)
    display_thread.daemon = True
    display_thread.start()
    print("Display update thread started")

    try:
        while True:
            time.sleep(3)

    except KeyboardInterrupt:
        print("Application shutting down")
