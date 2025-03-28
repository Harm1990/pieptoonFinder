# boot.py -- run on boot-up
import wifi_config
import network
import time
import webrepl
from use_neopixel import set_pixel_color
from ntptime import settime

set_pixel_color("green")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Connecting to WiFi...")
    wlan.connect(wifi_config.WIFI_AP, wifi_config.WIFI_PW)
    
    while not wlan.isconnected():
        time.sleep(1)

print("Connected to WiFi:", wlan.ifconfig())
webrepl.start()

settime()

# Set the pixel color to off
set_pixel_color("off")