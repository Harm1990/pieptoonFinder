from machine import Pin, I2S
import math
import struct

# INMP441 I2S Microphone Example for Raspberry Pi Pico
# Based on Mike Teachman's micropython-i2s-examples
# https://github.com/miketeachman/micropython-i2s-examples/tree/master

I2S_ID = 0
SD_PIN = Pin(44) # INMP441 SD pin (Green)
SCK_PIN = Pin(2) # INMP441 SCK pin (Yellow)
WS_PIN = Pin(4) # INMP441 WS pin (Brown)

SAMPLE_SIZE_IN_BITS = 32
FORMAT = I2S.MONO
SAMPLE_RATE = 16000
BUFFER_LENGTH_IN_BYTES = 40000  # Based on Mike's example

def sound_level():
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

    # First read dummy samples to allow the microphone to settle

    # Number of samples to read each time
    NUM_SAMPLE_BYTES = 2048

    # Raw samples will be stored in this buffer (signed 32-bit integers)
    samples_raw = bytearray(NUM_SAMPLE_BYTES)

    # Read samples from I2S microphone
    num_bytes_read = audio_in.readinto(samples_raw)

    if num_bytes_read == 0:
        return 0

    # Process raw samples
    format_str = "<{}i".format(num_bytes_read // 4)  # '<' for little-endian, 'i' for 32-bit signed integer
    samples = struct.unpack(format_str, samples_raw[:num_bytes_read])

    # Calculate RMS (Root Mean Square) which represents sound level
    sum_squares = 0
    for sample in samples:
        # Need to shift right by 8 bits for INMP441 (24-bit samples in 32-bit words)
        adjusted_sample = sample >> 8
        sum_squares += adjusted_sample * adjusted_sample # square

    # Calculate RMS
    rms = math.sqrt(sum_squares / num_bytes_read) # mean and square root

    # Scale to 0-100 range
    # The maximum value for a 24-bit sample is 2^23 = 8388608
    MAX_VALUE = 8388608
    level = min(100, (rms / MAX_VALUE) * 1000)  # Multiply by 1000 for better scaling

    audio_in.deinit()

    return level

