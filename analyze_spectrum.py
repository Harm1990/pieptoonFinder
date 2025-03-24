import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file (Modify path as needed for offline use)
def load_audio_data(file_path):
    df = pd.read_csv(file_path, header=None)  # Ensure no header row is assumed
    return df.iloc[:, 0].values  # Extract audio sample values

# Compute FFT and plot frequency spectrum
def analyze_audio(audio_samples, fs=16000):
    n = len(audio_samples)
    freqs = np.fft.rfftfreq(n, d=1/fs)  # Frequency axis
    fft_magnitude = np.abs(np.fft.rfft(audio_samples))  # Magnitude of FFT
    
    # Plot frequency spectrum
    plt.figure(figsize=(10, 5))
    plt.plot(freqs, fft_magnitude, label="Magnitude Spectrum")
    plt.xlim(0, fs / 2)  # Show frequencies up to Nyquist frequency (fs/2)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Frequency Spectrum of Audio Sample")
    plt.legend()
    plt.grid()
    plt.show()
    
    return freqs, fft_magnitude

# Function to compute intensity in a given frequency range
def compute_avg_intensity(freqs, fft_magnitude, f_min, f_max):
    mask = (freqs >= f_min) & (freqs <= f_max)
    selected_magnitudes = fft_magnitude[mask]
    return np.mean(selected_magnitudes) if len(selected_magnitudes) > 0 else 0

# Main execution (Modify file path accordingly)
if __name__ == "__main__":
    file_path = "audio.csv"  # Change to actual file location
    audio_samples = load_audio_data(file_path)
    
    freqs, fft_magnitude = analyze_audio(audio_samples)
    
    # Compute intensity in the specified ranges
    intensity_320_340 = compute_avg_intensity(freqs, fft_magnitude, 320, 340)
    intensity_1625_1675 = compute_avg_intensity(freqs, fft_magnitude, 1625, 1675)
    intensity_4000_8000 = compute_avg_intensity(freqs, fft_magnitude, 4000, 8000)
    
    print(f"Intensity in 320-340 Hz wrt 4 to 8 kHz: {intensity_320_340/intensity_4000_8000}")
    print(f"Intensity in 1625-1675 Hz wrt 4 to 8 kHz: {intensity_1625_1675/intensity_4000_8000}")
