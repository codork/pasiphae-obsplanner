#logs current weather to a csv file every minute from the OWM API

import csv
import pyowm
from datetime import datetime
import pytz
import time

owm = pyowm.OWM('105429291e4f0783a883e5ad86cc5bdb')

def get_curr_weather():
    obs = owm.weather_at_coords(-32.38722222, 20.81166667) #coords for sutherland site (lat/lon) 
    w = obs.get_weather()
    
    return w

with open('weather-db.csv', 'w') as csvfile:
    fieldnames = ['time', 'sunset_time', 'temp', 'wind_speed', 'wind_dir', 'clouds', 'humidity']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    start_time = time.time()
    while True:
        w = get_curr_weather()
        
        status = w.get_detailed_status()
        ref_time = w.get_reference_time(timeformat='iso')
        sunset_time = w.get_sunset_time(timeformat='iso')
        wind_speed = w.get_wind()['speed']
        wind_dir = w.get_wind()['deg']
        curr_temp = w.get_temperature('celsius')['temp']
        clouds = w.get_clouds()
        humidity = w.get_humidity()
        
        writer.writerow({'time':ref_time, 'sunset_time':sunset_time, 'temp':curr_temp, 'wind_speed':wind_speed, 'wind_dir':wind_dir, 'clouds':clouds, 'humidity':humidity})
        
        time.sleep(60.0 - ((time.time() - start_time) % 60.0))
        
   




