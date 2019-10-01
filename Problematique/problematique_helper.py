import wave
import sys
import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt

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

def get_useful_sine_waves_params(signal, fs, N, peak_height, f0, m_width=-1):
    # Only first half is kept as information is only mirrored in second half.
    fft_result = np.fft.fft(signal * np.hamming(N))[0:N//2]

    time = np.linspace(0, len(fft_result) / fs, num=len(fft_result))
    # show_figure(time, np.hamming(N)[0:N//2], "Fenetre de hamming")
    show_figure(time, fft_result, "Résultat fft avec fenetre de hamming")

    angle = np.angle(fft_result)

    if m_width < 0:
        m_width = np.where(fft_result == np.max(fft_result))[0][0]
    db_fft_result = 20*np.log10(fft_result/f0)
    show_figure(time, db_fft_result, "Résultat fft en dB")
    f_peaks, d = sp.find_peaks(db_fft_result, height = peak_height, distance = m_width)

    amplitude = fft_result[f_peaks]
    phase = angle[f_peaks]

    f_peaks = f_peaks * fs / N
    return f_peaks, amplitude, phase

def create_RIF_equi_coeff(nb_coeffs):
    return [1/nb_coeffs] * nb_coeffs

# Redresse le signal (abs) et applique un filtre sur ce dernier.
def redress_and_filter(signal, filter):
    # todo Verify mode between "full" (default), "same", "valid"
    return np.convolve(filter, abs(signal), "same")

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

def filtre_coupe_bande(N, largeur, fs, f_to_cut):
    k = int((largeur * 2 * N / fs)) + 1

    h = []
    h.append(1 - 2 * (k / N))
    for i in range(1, N, 1):
        h.append((-2.0 * (1.0/N * np.sin(np.pi * i * k / N) / np.sin(np.pi * i / N)) * np.cos(2.0 * np.pi * f_to_cut / fs * i)))
    return h

# Adjust the signal with enveloppe
def adjust_sound(signal, filter):
    output = np.multiply(signal, filter)
    output = output/(max(output)/12000)
    return output

def show_figure(x, y, titre="", use_scatter = False):
    plt.close('all')
    plt.figure()
    plt.scatter(x, y) if use_scatter else plt.plot(x, y)
    plt.title(titre)
    plt.show()