import matplotlib.pyplot as mplt
import numpy as np
from scipy import signal

# Test commit push
N = 40
n = range(0, N)
x1 = np.empty(N)
x2 = np.empty(N)
x3 = np.empty(N)

m1 = np.empty(N)
m2 = np.empty(N)
m3 = np.empty(N)

We1 = 2*np.pi/20
We2 = 2*np.pi/2
We3 = 2*np.pi/40
for i in n:
    x1[i] = np.sin(0.1*np.pi*i + np.pi/4)
    x2[i] = (-1)**i
    if i == 10:
        x3[i] = 1
    else:
        x3[i] = 0
    m1 = We1 * i / N
    m2 = We2 * i / N
    m3 = We3 * i / N

m = 0

mplt.stem(n, x1)
mplt.show()
mplt.stem(m1, np.abs(np.fft.fft(x1)))
mplt.show()

mplt.stem(n, x2)
mplt.show()
mplt.stem(m2, np.abs(np.fft.fft(x2)))
mplt.show()

mplt.stem(n, x3)
mplt.show()
mplt.stem(m3, np.abs(np.fft.fft(x3)))
mplt.show()






