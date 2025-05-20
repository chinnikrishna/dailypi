import os
import sys
import time
import imgkit
from PIL import Image
from html2image import Html2Image

from config import CONFIG

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in3f

class Display:
    def __init__(self, width=800, height=480):
        self.width = width
        self.height = height


    def capture_image(self, url, output_path):
        
        try:
            hti = Html2Image(size=(self.width, self.height+130), 
                             output_path=CONFIG.OUTPUT_DIR)
            hti.screenshot(url=url, save_as=os.path.basename(output_path))
        except Exception as e:
            print(f"Error using html2image: {str(e)}")
        
    def capture_weather_dashboard(self):
        os.makedirs(CONFIG.OUTPUT_DIR, exist_ok=True)
        output_png = os.path.join(CONFIG.OUTPUT_DIR, "temp_weather.png")
        output_bmp = os.path.join(CONFIG.OUTPUT_DIR, "weather_dashboard.bmp")

        self.capture_image(f"http://localhost:{CONFIG.FLASK_PORT}", 
                           output_path=output_png)
        
        img = Image.open(output_png)
        img = img.resize((self.width, self.height), Image.LANCZOS)
        dithered = self.dither_image(img)
        dithered.save(output_bmp, format="BMP")
        os.remove(output_png)
        
        return output_bmp

    def find_closest_color(self, pixel):
        """Find the closest color in the palette to the given pixel"""
        r, g, b = pixel
        min_distance = float('inf')
        closest_color = CONFIG.EPAPER_PALETTE[0]
        
        for color in CONFIG.EPAPER_PALETTE:
            # Simple Euclidean distance
            dr = r - color[0]
            dg = g - color[1]
            db = b - color[2]
            distance = dr*dr + dg*dg + db*db
            
            if distance < min_distance:
                min_distance = distance
                closest_color = color
                
        return closest_color

    def dither_image(self, img):
        """Apply Floyd-Steinberg dithering using standard library"""
        width, height = img.size
        img = img.convert("RGB")
        pixel_map = img.load()
        
        for y in range(height-1):
            for x in range(width-1):
                old_pixel = pixel_map[x, y]
                new_pixel = self.find_closest_color(old_pixel)
                pixel_map[x, y] = new_pixel
                
                # Calculate error
                error_r = old_pixel[0] - new_pixel[0]
                error_g = old_pixel[1] - new_pixel[1]
                error_b = old_pixel[2] - new_pixel[2]
                
                # Distribute error to neighboring pixels (Floyd-Steinberg)
                if x + 1 < width:
                    r, g, b = pixel_map[x+1, y]
                    pixel_map[x+1, y] = (
                        int(r + error_r * 7/16),
                        int(g + error_g * 7/16),
                        int(b + error_b * 7/16)
                    )
                
                if x > 0 and y + 1 < height:
                    r, g, b = pixel_map[x-1, y+1]
                    pixel_map[x-1, y+1] = (
                        int(r + error_r * 3/16),
                        int(g + error_g * 3/16),
                        int(b + error_b * 3/16)
                    )
                
                if y + 1 < height:
                    r, g, b = pixel_map[x, y+1]
                    pixel_map[x, y+1] = (
                        int(r + error_r * 5/16),
                        int(g + error_g * 5/16),
                        int(b + error_b * 5/16)
                    )
                
                if x + 1 < width and y + 1 < height:
                    r, g, b = pixel_map[x+1, y+1]
                    pixel_map[x+1, y+1] = (
                        int(r + error_r * 1/16),
                        int(g + error_g * 1/16),
                        int(b + error_b * 1/16)
                    )
        
        # Convert to palette image
        palette_img = Image.new('P', img.size)
        palette = []
        for color in CONFIG.EPAPER_PALETTE:
            palette.extend(color)
        # Fill remaining palette entries
        palette.extend([0] * (256 * 3 - len(palette)))
        palette_img.putpalette(palette)
        
        return img.quantize(colors=7, palette=palette_img)
    
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
                    self.update_epaper(bmp_path)
                
                time.sleep(CONFIG.WEATHER_UPDATE_INTERVAL)
            except Exception as e:
                print(f"Error in display update loop: {e}")
                time.sleep(CONFIG.RETRY_INTERVAL)