import time
import machine
from use_neopixel import set_pixel_color
from use_INMP import sound_level, stop_INMP

# Set up the button
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
previous_button_state = button.value()

while True:
    if button.value() == 0:
        print("Button pressed!")
        previous_button_state = button.value()
        set_pixel_color("red")
        time.sleep(0.2)
        set_pixel_color("green")
        time.sleep(0.2)
        set_pixel_color("blue")
        time.sleep(0.2)


        print("# INMP441 Sound Level Monitor")
        print("# Based on Mike Teachman's I2S implementation")
        print("# Make sounds to see the levels change")
        print("# Running for 10 s")

        try:
            # Moving average window for smoothing
            window_size = 3
            values = [0] * window_size
            loop_counter = 0

            while loop_counter < 1e2:
                # Get current sound level
                level = sound_level()

                # Apply simple moving average
                values.pop(0)
                values.append(level)
                smoothed_level = int(sum(values) / window_size)

                # Output for Thonny plotter
                print(smoothed_level)

                # Small delay
                time.sleep(0.1)
                loop_counter += 1

        except KeyboardInterrupt:
            print("# Monitoring stopped")
        finally:
            print("Loop ended")
    else:
        if previous_button_state != button.value():
            print("Button not pressed!")
            previous_button_state = button.value()
            # Change pixels to empty
            set_pixel_color("off")
   
