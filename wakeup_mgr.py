
import time
import requests
import subprocess
from datetime import datetime, timedelta

class WakeupMgr:
    def __init__(self, wake_hours=2):
        self.pisugar_api = "http://localhost:8421"
        self.wake_hours = wake_hours
    
    def schedule_wake_and_shutdown(self):
        """Set alarm and shutdown Pi"""
        print(f"Setting wake alarm for {self.wake_hours} hours from now...")
        
        # Calculate next wake time
        next_wake = datetime.now() + timedelta(hours=self.wake_hours)
        wake_time = next_wake.strftime("%H:%M:%S")
        
        try:
            # Set PiSugar alarm
            alarm_data = {
                "alarm_time": wake_time,
                "alarm_weekdays": 127  # Every day
            }
            
            requests.post(f"{self.pisugar_api}/api/alarm", json=alarm_data, timeout=5)
            requests.post(f"{self.pisugar_api}/api/alarm_enable", json={"enabled": True}, timeout=5)
            
            print(f"Alarm set for: {next_wake.strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"Alarm setting failed: {e}")
        
        # Wait a moment then shutdown
        print("💤 Shutting down in 3 seconds...")
        time.sleep(3)
        
        subprocess.run(['sudo', 'shutdown', '-h', 'now'])