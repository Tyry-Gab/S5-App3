import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile
import sys
#import SoundsUtil
from Problematique.problematique_helper import *


# Opening file, continuing only if mono
signal, fs, N = param_wav('note_guitare_LAd.wav')

# Find most significative frequencies from their amplitude (f (Hz), amplitude, phase (rad))
f_peaks, amplitude, phase = get_useful_sine_waves_params(signal, fs, N)

# todo Find the right number of coefficients
rif_filter = create_RIF_equi_coeff(1000)

convolution = convolution(signal, rif_filter)

n = np.arange(len(convolution))

#Generate notes: (A# is the base note)

do_signal = generate_signal(amplitude, f_peaks, fs, phase, n, -10)
re_signal = generate_signal(amplitude, f_peaks, fs, phase, n, -8)
mi_signal = generate_signal(amplitude, f_peaks, fs, phase, n, -6)
fa_signal = generate_signal(amplitude, f_peaks, fs, phase, n, -5)
sol_signal = generate_signal(amplitude, f_peaks, fs, phase, n, -3)
la_signal = generate_signal(amplitude, f_peaks, fs, phase, n, -1)
si_signal = generate_signal(amplitude, f_peaks, fs, phase, n, 1)
do_signal2 = generate_signal(amplitude, f_peaks, fs, phase, n, 2)

output_signal = generate_note(do_signal, convolution)
output_signal = np.append(output_signal, generate_note(re_signal, convolution))
output_signal = np.append(output_signal, generate_note(mi_signal, convolution))
output_signal = np.append(output_signal, generate_note(fa_signal, convolution))
output_signal = np.append(output_signal, generate_note(sol_signal, convolution))
output_signal = np.append(output_signal, generate_note(la_signal, convolution))
output_signal = np.append(output_signal, generate_note(si_signal, convolution))
output_signal = np.append(output_signal, generate_note(do_signal2, convolution))

wavfile.write("Test_Gamme.wav",fs,np.int16(np.real(output_signal)))

# 5th symphony
symph_signal = generate_half_silence()
symph_signal = np.append(symph_signal, generate_half_note(sol_signal, convolution))
symph_signal = np.append(symph_signal, generate_half_note(sol_signal, convolution))
symph_signal = np.append(symph_signal, generate_half_note(sol_signal, convolution))
symph_signal = np.append(symph_signal, generate_double_note(mi_signal, convolution))
symph_signal = np.append(symph_signal, generate_half_silence())
symph_signal = np.append(symph_signal, generate_half_note(fa_signal, convolution))
symph_signal = np.append(symph_signal, generate_half_note(fa_signal, convolution))
symph_signal = np.append(symph_signal, generate_half_note(fa_signal, convolution))
symph_signal = np.append(symph_signal, generate_double_note(re_signal, convolution))

wavfile.write("Fifth_Symphony.wav",fs,np.int16(np.real(symph_signal)))


# Test to look if sine seems good
test_sine = generate_sine_wave(amplitude[0], f_peaks[0], fs, phase[0], n)
plt.figure(0)
plt.plot(n, do_signal)
plt.show()


# # Plotting
# Time = np.linspace(0, len(signal)/fs, num=len(signal))
#
# # Base signal plotting
# plt.figure(1)
# plt.title('Guitar A# signal')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.plot(Time, signal)
# plt.show()
# plt.close('all')
#
# w_normalized = np.linspace(0, N-1, N)
# w_normalized = 2*np.pi*w_normalized/N
# plt.plot(w_normalized, np.abs(np.fft.fft(signal)))
# plt.show()
#
# window = np.hanning(N)
# windowed_signal = signal * window
# plt.figure()
# plt.title('Windowed A#')
# plt.plot(Time, windowed_signal)
# plt.show()
#
# plt.figure()
# plt.title('Windowed transformed')
# amp_abs_fft_signal = np.abs(np.fft.fft(windowed_signal))
# # find a reference frequency for dB
# plt.plot(w_normalized, 20*np.log10(amp_abs_fft_signal/amp_abs_fft_signal[22100]))
# plt.show()
# plt.close('all')
#
# elem_to_take = int(len(amp_abs_fft_signal)/2)
# sorted_freq = sorted(amp_abs_fft_signal[0:elem_to_take], reverse = True)
# highest_32_sin_Hz = []
# i = 0
# while len(highest_32_sin_Hz) < 32:
#     index = np.where(amp_abs_fft_signal[0:elem_to_take] == sorted_freq[i])[0]
#     for f in index:
#         frequency = w_normalized[f]*fs/2/np.pi
#         if is_in_list_with_tolerance(highest_32_sin_Hz, frequency, 0.01):
#             # Save in a list a tuple with structure = (Freq(Hz), Amplitude(raw), n)
#             highest_32_sin_Hz.append((frequency, sorted_freq[i], f))
#     i += 1
#
# plt.figure()
# plt.title('Half Windowed transformed')
# db_signal = 20*np.log10(amp_abs_fft_signal / amp_abs_fft_signal[highest_32_sin_Hz[31][2]])
# print(amp_abs_fft_signal[highest_32_sin_Hz[31][2]])
# plt.plot(w_normalized[0:elem_to_take], db_signal[0:elem_to_take])
# plt.show()
# plt.close('all')
#
#
# # Create all 32 sinus again
# sin_32 = []
# reconstructed_signal = np.empty(N)
# i = 0
# for sinus in highest_32_sin_Hz:
#     temp_sinus = sinus[1] * np.sin(windowed_signal[sinus[2]] * Time * sinus[2])
#     reconstructed_signal += temp_sinus
#     sin_32.append(temp_sinus)
#
#
# plt.figure()
# plt.title('Sinus')
# plt.plot(Time, sin_32[1])
# plt.show()
# plt.close('all')

print("Done!")