import machine, neopixel

# Set up the NeoPixel debug strip
np = neopixel.NeoPixel(machine.Pin(47), 1)
np.ORDER = (0,1,2,3) # On Wemos S3 mini board, red and green are swapped
brightness = 22

def set_pixel_color(color):
    if color == "red":
        np[0] = (brightness,0,0) # Red
    elif color == "green":
        np[0] = (0,brightness,0) # Green
    elif color == "blue":
        np[0] = (0,0,brightness) # Blue
    elif color == "yellow":
        np[0] = (brightness,brightness,0) # Yellow
    elif color == "cyan":
        np[0] = (0,brightness,brightness) # Cyan
    elif color == "purple":
        np[0] = (brightness,0,brightness) # Purple
    elif color == "white":
        np[0] = (brightness,brightness,brightness) # White 
    elif color == "off":
        np[0] = (0,0,0) # Off
    elif color == "on":
        np[0] = (brightness,brightness,brightness) # On
    else:
        np[0] = (0,0,0) # Off
        print("Invalid color")
    np.write()