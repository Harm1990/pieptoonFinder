import time
import machine, neopixel

# Set up the NeoPixel debug strip
np = neopixel.NeoPixel(machine.Pin(47), 1)
np.ORDER = (0,1,2,3) # On Wemos S3 mini board, red and green are swapped
brightness = 22
# Set up the button
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
previous_button_state = button.value()

while True:
    if button.value() == 0:
        print("Button pressed!")
        previous_button_state = button.value()
        np[0] = (brightness,0,0) # Red
        np.write()
        time.sleep(1)
        np[0] = (0,brightness,0) # Green
        np.write()
        time.sleep(1)
        np[0] = (0,0,brightness) # Blue
        np.write()
        time.sleep(1)
    else:
        if previous_button_state != button.value():
            print("Button not pressed!")
            previous_button_state = button.value()
    np[0] = (0,0,0)
    np.write()
    time.sleep(1)   
