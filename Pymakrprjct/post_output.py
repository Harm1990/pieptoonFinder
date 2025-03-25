import network
import urequests
import wifi_config
import time
import json

# Function to connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(wifi_config.WIFI_AP, wifi_config.WIFI_PW)
        
        while not wlan.isconnected():
            time.sleep(1)
    
    print("Connected to WiFi:", wlan.ifconfig())

def get_formatted_datetime():
    # Get the current time from the device (Assumes RTC is set correctly)
    t = time.localtime()
    
    # Define month abbreviations
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    day = f"{t[2]:02d}"  # Two-digit day
    month = months[t[1] - 1]  # Get month abbreviation
    year = f"{t[0] % 100:02d}"  # Two-digit year
    hours = f"{t[3]:02d}"  # Two-digit hour
    minutes = f"{t[4]:02d}"  # Two-digit minute
    
    return f"{day}-{month}-{year} {hours}:{minutes}"

# Function to send an HTTP POST request
def send_post_request(url, value):
    #headers = {"Content-Type": "application/json"}
    data_string = wifi_config.POST_PREFIX + get_formatted_datetime() + wifi_config.POST_INTERFIX + str(value)
    
    try:
        response = urequests.post(url, data=data_string)
        # Todo get post working on http and on own server
        print("Response:", response.text)
        response.close()
    except Exception as e:
        print("Request failed:", e)
    return response