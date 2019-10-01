import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile
import sys
#import SoundsUtil
from Problematique.problematique_helper import *

### Bassoon

signal, fs, N = param_wav('note_basson_plus_sinus_1000_Hz.wav')

time = np.linspace(0, len(signal) / fs, num=len(signal))
show_figure(time, signal, "Signal de base")

h_fpb = filtre_coupe_bande(1024, 20, fs, 1000)
# remove 1 kHz
signal = np.convolve(signal, h_fpb, "same")

# Find most significative frequencies from their amplitude (f (Hz), amplitude, phase (rad))
f_peaks, amplitude, phase = get_useful_sine_waves_params(signal, fs, N, -25, 1000000.0, 5)

rif_filter = create_RIF_equi_coeff(885)

enveloppe = redress_and_filter(signal, rif_filter)

n = np.arange(len(enveloppe))

signal_recreated = generate_signal(amplitude, f_peaks, fs, phase, n)

signal_recreated_adjusted = adjust_sound(signal_recreated, enveloppe)

wavfile.write("Filtered_Basson.wav", fs, np.int16(signal_recreated_adjusted))

print("Done!")


# Test section only
# plt.figure()
# plt.title('Windowed transformed')
# amp_abs_fft_signal = np.abs(np.fft.fft(signal))
# sorted_freq = sorted(amp_abs_fft_signal[0:N//2], reverse = True)
# # find a reference frequency for dB
# w_normalized = np.linspace(0, N - 1, N)
# plt.plot(w_normalized, 20*np.log10(amp_abs_fft_signal/1000000.0))
# plt.show()
# plt.close('all')

# plt.figure()
# plt.title('Windowed transformed')
# amp_abs_fft_signal = np.abs(np.fft.fft(signal))
# sorted_freq = sorted(amp_abs_fft_signal[0:N//2], reverse = True)
# print(sorted_freq[0:64])
# # find a reference frequency for dB
# w_normalized = np.linspace(0, N - 1, N)
# plt.plot(w_normalized, amp_abs_fft_signal)
# plt.show()
# plt.close('all')