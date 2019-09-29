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
    index = np.where(amp_abs_fft_signal[0:elem_to_take] == sorted_freq[i])[0]
    for f in index:
        frequency = w_normalized[f]*fs/2/np.pi
        if is_in_list_with_tolerance(highest_32_sin_Hz, frequency, 0.01):
            # Save in a list a tuple with structure = (Freq(Hz), Amplitude(raw), n)
            highest_32_sin_Hz.append((frequency, sorted_freq[i], f))
    i += 1



print("Done!")