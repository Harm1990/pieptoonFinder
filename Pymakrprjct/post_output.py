import time
import os

DATAFILE = "data.csv"

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

def write_value_to_datafile(value):
    # Get the current time
    timestamp = get_formatted_datetime()
    
    # Open the data file in append mode
    with open(DATAFILE, "a") as file:
        # Write the timestamp and value to the file
        file.write(f"{timestamp},{value}\n")
        print(f"Written to {DATAFILE}: {timestamp},{value}")