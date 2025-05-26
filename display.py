import os
import sys
import time
import imgkit
from PIL import Image
from html2image import Html2Image

from config import CONFIG
from wakeup_mgr import WakeupMgr


libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from lib.waveshare_epd import epd7in3f

class Display:
    def __init__(self, width=800, height=480):
        self.width = width
        self.height = height


    def capture_image(self, url, output_path):
        
        try:
            hti = Html2Image(size=(self.width, self.height + 130), 
                             output_path=CONFIG.OUTPUT_DIR,
                             custom_flags=['--disable-gpu'])
            hti.screenshot(url=url, save_as=os.path.basename(output_path))
        except Exception as e:
            print(f"Error using html2image: {str(e)}")
        
    def capture_weather_dashboard(self):
        os.makedirs(CONFIG.OUTPUT_DIR, exist_ok=True)
        output_png = os.path.join(CONFIG.OUTPUT_DIR, "temp_weather.png")
        output_bmp = os.path.join(CONFIG.OUTPUT_DIR, "weather_dashboard.bmp")

        self.capture_image(f"http://localhost:{CONFIG.FLASK_PORT}", 
                           output_path=output_png)
        
        image = Image.open(output_png)
        # img = img.resize((self.width, self.height), Image.LANCZOS)
        image = image.resize((self.width, self.height), 
                             resample=Image.Resampling.LANCZOS)

        palette = [0, 0, 0,  # black
                   255, 255, 255,  # white
                   0, 255, 0,  # green
                   0, 0, 255,  # blue
                   255, 0, 0,  # red
                   255, 255, 0,  # yellow
                   255, 128, 0]  # orange

        seven_color_palette = Image.new("P", (self.width, self.height))
        seven_color_palette.putpalette(palette)
        image = image.quantize(palette=seven_color_palette, dither=Image.Dither.FLOYDSTEINBERG)
        image = image.convert(colors=24)
        image.save(output_bmp, format="BMP")
        os.remove(output_png)
        
        return output_bmp

    def update_epaper(self):
        try:
            output_bmp = os.path.join(CONFIG.OUTPUT_DIR, "weather_dashboard.bmp")
            epd = epd7in3f.EPD()
            epd.init()
            epd.Clear()
            
            img = Image.open(output_bmp)
            epd.display(epd.getbuffer(img))
            epd.sleep()
            
            print("E-paper display updated successfully")
            wakeup_srvc = WakeupMgr()
            wakeup_srvc.schedule_wake_and_shutdown()
            
        except ImportError:
            print("Waveshare library not found - running in simulation mode")
            print(f"Would display image: {output_bmp}")
        
        except Exception as e:
            print(f"Error updating e-paper: {e}")
        
        except KeyboardInterrupt:
            epd7in3f.epdconfig.module_exit(cleanup=True)


    def run(self):
        while True:
            try:
                time.sleep(5)
                bmp_path = self.capture_weather_dashboard()
                if bmp_path:
                    self.update_epaper()
                
                time.sleep(CONFIG.WEATHER_UPDATE_INTERVAL)
            except Exception as e:
                print(f"Error in display update loop: {e}")
                time.sleep(CONFIG.RETRY_INTERVAL)
