from machine import Pin, I2S
import math
import struct
import time

def bytearray_to_ints(data):
    """ Convert a bytearray of I2S data (32-bit words) to a list of 24-bit signed integers. """
    ints = []
    for i in range(0, len(data), 4):  # Process 4 bytes at a time (32-bit word)
        sample = data[i:i+3]  # Take the first 3 bytes (24-bit data)
        int_value = int.from_bytes(sample, 'little')  # Convert to int (unsigned)

        # Convert to signed 24-bit integer manually
        if int_value & 0x800000:  # If the 24th bit is set, sign extend
            int_value -= 0x1000000  # Convert to negative value

        ints.append(int_value) # Shift 8 bits
    return ints

# INMP441 I2S Microphone Example for Raspberry Pi Pico
# Based on Mike Teachman's micropython-i2s-examples
# https://github.com/miketeachman/micropython-i2s-examples/tree/master

I2S_ID = 0
SD_PIN = Pin(44) # INMP441 SD pin (Green)
SCK_PIN = Pin(2) # INMP441 SCK pin (Yellow)
WS_PIN = Pin(4) # INMP441 WS pin (Brown)

SAMPLE_SIZE_IN_BITS = 32
FORMAT = I2S.MONO
SAMPLE_RATE = 16000 # Hz
BUFFER_LENGTH_IN_BYTES = 40000
FILENAME = "audio.csv"

"""Capture audio and calculate sound level

Based on Mike Teachman's example but simplified for sound level monitoring.
"""
# Initialize I2S for microphone
audio_in = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.RX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)

# Number of samples to read each time
NUM_SAMPLE_BYTES = 16000*4 # Returns 8000 samples
# Raw samples will be stored in this buffer (signed 32-bit integers)
samples_raw = bytearray(NUM_SAMPLE_BYTES)



# Perform startup read
# 2^18 cycles needed, which is 32768 bytes, but since we use mono, divide by two
IGNORE_BYTES = 16384
samples_startup = bytearray(1024)
# Read samples from I2S microphone
ignored = 0
while ignored < IGNORE_BYTES:
    bytes_read = audio_in.readinto(samples_startup)
    if bytes_read:
        ignored += bytes_read


# Read samples from I2S microphone
num_bytes_read = audio_in.readinto(samples_raw)

if num_bytes_read == 0:
    print("Error num_bytes_read=0")

# Process raw samples
samples = bytearray_to_ints(samples_raw)


with open(FILENAME, "w") as f:
    for sample in samples:
        f.write(f"{sample}\n") # Write line to csv

f.close()
print(f"Recording complete. Saved {len(samples)} samples to {FILENAME}")


    
    