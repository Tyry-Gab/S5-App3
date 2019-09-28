import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from Problematique import SoundsUtil


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
w_normalized = np.linspace(0, 1, N)
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
plt.plot(w_normalized, np.abs(np.fft.fft(windowed_signal)))
plt.show()
plt.close('all')
print("Done!")