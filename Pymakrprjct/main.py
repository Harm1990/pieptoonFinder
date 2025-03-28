import time
import machine
from use_neopixel import set_pixel_color
from post_output import write_value_to_datafile
import use_INMP

# Set up the button
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
previous_button_state = button.value()

# Keep track of time
time_last_sample = 0
INTERVAL_SAMPLES = 600 # Sample every 600 seconds for now
time_last_blink = 0
INTERVAL_BLINK = 5 # Blink every 5 seconds

while True:
    if button.value() == 0:
        print("Button pressed!")
        previous_button_state = button.value()
        set_pixel_color("red")
    else:
        # Change pixels to empty
        set_pixel_color("off")
        if previous_button_state != button.value():
            print("Button not pressed!")
            previous_button_state = button.value()

    if (time.time() - time_last_blink ) > INTERVAL_BLINK:
        time_last_blink = time.time()
        set_pixel_color("green")
        time.sleep(0.5)
        set_pixel_color("off")
        time.sleep(0.5)
        if (time.time() < 1e6):
            set_pixel_color("green")
            time.sleep(0.5)
            set_pixel_color("off")           

    if (time.time() - time_last_sample ) > INTERVAL_SAMPLES:
        time_last_sample = time.time()
        print("Starting recording of 1650 Hz peak")
        set_pixel_color("blue")
        sound_value = use_INMP.determine_1650Hz_intensity(5) # Use 5 iterations
        write_value_to_datafile(sound_value)
        set_pixel_color("off")