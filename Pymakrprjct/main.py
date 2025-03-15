import time
import machine, neopixel

# Set up the NeoPixel debug strip
np = neopixel.NeoPixel(machine.Pin(47), 1)
brightness = 22
# Set up the button
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    if button.value() == 0:
        print("Button pressed!")
    else:
        print("Button not pressed!")
    time.sleep(1)
    np[0] = (0,brightness,0) # On Wemos board, red and green are swapped
    np.write()
    time.sleep(1)
    np[0] = (brightness,0,0) # Red
    np.write()
    time.sleep(1)
    np[0] = (0,0,brightness) # Blue
    np.write()
    time.sleep(1)
    np[0] = (0,0,0)
    np.write()
    time.sleep(1)   
