import matplotlib.pyplot as mplt
import numpy as np
from scipy import signal

# Test commit push
N = 42
n = range(0, N)
x1 = np.empty(N)
x1_hanning = x1
x2 = np.empty(N)
x2_hanning = x2
x3 = np.empty(N)
x3_hanning = x3
Hanning_Window = np.empty(N)

F_by_Fe = np.empty(N)

W_normalised = np.hanning(N)


for i in n:
    x1[i] = np.sin(0.1*np.pi*i + np.pi/4)
    x1_hanning[i] = x1[i] * Hanning_Window[i]
    x2[i] = (-1)**i
    if i == 10:
        x3[i] = 1
    else:
        x3[i] = 0
    F_by_Fe[i] = i/N
    W_normalised[i] = 2*np.pi*F_by_Fe[i]


mplt.stem(n, x1)
#mplt.show()
mplt.stem(W_normalised, np.abs(np.fft.fft(x1)))
#mplt.show()

mplt.stem(n, x2)
#mplt.show()
mplt.stem(W_normalised, np.abs(np.fft.fft(x2)))
#mplt.show()

mplt.stem(n, x3)
#mplt.show()
mplt.stem(W_normalised, np.abs(np.fft.fft(x3)))
#mplt.show()

mplt.stem(np.hanning(42))
mplt.show()

