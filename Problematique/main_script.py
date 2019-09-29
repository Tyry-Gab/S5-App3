import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
#import SoundsUtil
from problematique_helper import *


# Opening file, continuing only if mono
spf = wave.open('note_guitare_LAd.wav', 'r')
if spf.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)

# Playing sound
#SoundsUtil.playSound(spf)


# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()

# Plotting
Time = np.linspace(0, len(signal)/fs, num=len(signal))

# Base signal plotting
plt.figure(1)
plt.title('Guitar A# signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.plot(Time, signal)
plt.show()
plt.close('all')

N = spf.getnframes()
w_normalized = np.linspace(0, N-1, N)
w_normalized = 2*np.pi*w_normalized/N
plt.plot(w_normalized, np.abs(np.fft.fft(signal)))
plt.show()

window = np.hanning(N)
windowed_signal = signal * window
plt.figure()
plt.title('Windowed A#')
plt.plot(Time, windowed_signal)
plt.show()

plt.figure()
plt.title('Windowed transformed')
amp_abs_fft_signal = np.abs(np.fft.fft(windowed_signal))
plt.plot(w_normalized, np.abs(np.fft.fft(windowed_signal)))
plt.show()
plt.close('all')

elem_to_take = int(len(amp_abs_fft_signal)/2)
sorted_freq = sorted(amp_abs_fft_signal[0:elem_to_take], reverse = True)
highest_32_sin_Hz = []
i = 0
while len(highest_32_sin_Hz) < 32:
    frequency = w_normalized[np.where(amp_abs_fft_signal[0:elem_to_take] == sorted_freq[i])[0]]*fs/2/np.pi
    for f in frequency:
        highest_32_sin_Hz = add_if_far_enough(highest_32_sin_Hz, f, 0.01)
        print(frequency)
        print(f)
    i += 1

print(highest_32_sin_Hz)


print("Done!")