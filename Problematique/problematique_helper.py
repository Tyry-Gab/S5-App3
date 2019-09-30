import wave
import sys
import numpy as np
import scipy.signal as sp

TEMPO = 16000

def param_wav(wav_file):
    """
    :param wav_file: The filename of the wav file to open
    :type wav_file: String
    :returns: signal: Temporal signal, fs: Framerate of signal, N: Number of samples
    :rtype: int16 array, float, int
    """
    spf = wave.open(wav_file, 'r')
    if spf.getnchannels() == 2:
        print("Just mono files")
        sys.exit(0)

    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    fs = spf.getframerate()

    N = spf.getnframes()
    print("Fréquence d'échantillonage: " + str(fs))
    print("Nombre d'échantillons: " + str(N))

    return signal, fs, N

def get_useful_sine_waves_params(signal, fs, N):
    # Only first half is kept as information is only mirrored in second half.
    fft_result = np.fft.fft(signal * np.hanning(N))[0:N//2]

    # todo perform on windowed or original??
    angle = np.angle(fft_result)

    m_width = np.where(fft_result == max(fft_result))[0][0]
    db_fft_result = 20*np.log10(fft_result[0:N//2]/102734.57571665409)
    f_peaks, d = sp.find_peaks(db_fft_result, height= -25, distance = m_width)

    amplitude = fft_result[f_peaks]
    phase = angle[f_peaks]

    f_peaks = f_peaks * fs / N
    return f_peaks, amplitude, phase

def create_RIF_equi_coeff(nb_coeffs):
    return [1/nb_coeffs] * nb_coeffs

# Redresse le signal (abs) et applique un filtre sur ce dernier.
def convolution(signal, filter):
    # todo Verify mode between "full" (default), "same", "valid"
    return np.convolve(filter, abs(signal), "valid")

def generate_sine_wave(amplitude, f, fs, phase, n, ecart_note = 0):
    return np.multiply(amplitude, (np.sin((2 * np.pi * f * n / fs) * (2 ** (ecart_note / 12)) + phase)))

def generate_signal(amplitudes, f_peaks, fs, phases, n, ecart_note = 0):
    sine_waves_sum = [0]
    for i in range(len(f_peaks)):
        sine_waves_sum += generate_sine_wave(amplitudes[i], f_peaks[i], fs, phases[i], n, ecart_note)
    return sine_waves_sum

def generate_half_note(note_signal, filtered_signal):
    output = np.multiply(note_signal, filtered_signal)
    # Lower sound volume
    output = output / (max(output) / 10000)
    output = np.resize(output, (1, TEMPO))
    return output[0]

def generate_note(note_signal, filtered_signal):
    output = np.multiply(note_signal, filtered_signal)
    # Lower sound volume
    output = output / (max(output) / 10000)
    output = np.resize(output, (1, 2*TEMPO))
    return output[0]

def generate_double_note(note_signal, filtered_signal):
    output = np.multiply(note_signal, filtered_signal)
    # Lower sound volume
    output = output / (max(output) / 10000)
    output = np.resize(output, (1, 4*TEMPO))
    return output[0]

def generate_half_silence():
    return [0] * TEMPO


def is_in_list_with_tolerance(some_list, element_to_add, accept_factor):
    if element_to_add == None or element_to_add == 0.0:
        return False
    for element in some_list:
        element_l = element[0] * (1.0 - accept_factor)
        element_h = element[0] * (1.0 + accept_factor)
        if element_to_add >= element_l and element_to_add <= element_h:
            return False
    return True


