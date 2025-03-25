from machine import Pin, I2S
import math

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

# Goertzel algorithm to compute energy at a specific frequency
def goertzel(samples, target_freq, sample_rate):
    N = len(samples)
    k = int(0.5 + (N * target_freq) / sample_rate)
    omega = (2.0 * math.pi * k) / N
    coeff = 2.0 * math.cos(omega)
    s_prev = 0.0
    s_prev2 = 0.0
    
    for sample in samples:
        s = sample + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s
    
    power = s_prev2**2 + s_prev**2 - coeff * s_prev * s_prev2
    return power

# Compute total intensity in a frequency range with higher accuracy
def compute_intensity(samples, f_min, f_max, sample_rate):
    step = 5  # Higher accuracy by scanning every 1 Hz
    return sum(goertzel(samples, f, sample_rate) for f in range(f_min, f_max + 1, step))

# Compute background noise level
def compute_background_noise(samples, sample_rate):
    intensity = 0
    background_levels = [4000,5000,6000,7000,8000]
    for level in background_levels:
        intensity += goertzel(samples,level,sample_rate)
    return intensity / len(background_levels)

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



"""Capture audio and calculate sound level

Based on Mike Teachman's example but simplified for sound level monitoring.
"""
def determine_1650Hz_intensity(iterations):
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
    NUM_SAMPLE_BYTES = SAMPLE_RATE*4 # Returns 1 second of samples
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
    print("Microphone started and dummy read performed")
    
    sound_levels = [] # Create empty list for output
    
    for i in range(iterations):
        print(f"Starting iteration {i}")
        # Read samples from I2S microphone
        num_bytes_read = audio_in.readinto(samples_raw)
        
        if num_bytes_read == 0:
            print("Error num_bytes_read=0")

        # Process raw samples
        samples = bytearray_to_ints(samples_raw)

        # Now use FFT to calculate intensities
        # Compute background noise level
        background_noise = compute_background_noise(samples, SAMPLE_RATE)
        # Compute intensity in the specified ranges, adjusted and scaled for background noise
        # raw_intensity_320_340 = compute_intensity(samples, 320, 340, SAMPLE_RATE)
        raw_intensity_1625_1675 = compute_intensity(samples, 1625, 1675, SAMPLE_RATE)

        # adjusted_intensity_320_340 = (raw_intensity_320_340 - background_noise * (340 - 320 + 1)) / background_noise
        adjusted_intensity_1625_1675 = (raw_intensity_1625_1675 - background_noise * (1675 - 1625 + 1)) / background_noise
        sound_levels.append(adjusted_intensity_1625_1675)
        
        # print(f"Scaled Intensity in 320-340 Hz: {adjusted_intensity_320_340}")
        print(f"Scaled Intensity in 1625-1675 Hz: {adjusted_intensity_1625_1675}")
        
    # Switch off I2S bus
    audio_in.deinit()
    
    # Take output and provide average
    avg_iterations = sum(sound_levels)/iterations
    # Convert to decibel
    return 20*math.log10(max(avg_iterations,1))
    return sum(sound_levels)/iterations
