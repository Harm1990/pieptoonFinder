# boot.py -- run on boot-up
import wifi_config
import network
import time
import webrepl
from use_neopixel import set_pixel_color
from ntptime import settime

wifi_counter = 0

set_pixel_color("green")
wlan = network.WLAN(network.STA_IF)
network.hostname(wifi_config.WIFI_HOSTNAME)
wlan.active(True)

if not wlan.isconnected():
    print("Connecting to WiFi...")
    wlan.connect(wifi_config.WIFI_AP1, wifi_config.WIFI_PW)
    
    while not wlan.isconnected() and wifi_counter < 30:
        time.sleep(1)
        wifi_counter += 1
    
    print("Trying other WIFI_AP")
    wlan.active(False) # Reset Wifi counters
    wlan.active(True)
    wlan.connect(wifi_config.WIFI_AP2, wifi_config.WIFI_PW)

    while not wlan.isconnected():
        time.sleep(1)    

print("Connected to WiFi:", wlan.ifconfig())
webrepl.start()

settime()

# Set the pixel color to off
set_pixel_color("off")