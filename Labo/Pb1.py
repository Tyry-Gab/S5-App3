import matplotlib.pyplot as mplt
import numpy as np
from scipy import signal

# Test commit push
N = 40
n = range(0, N)
x1 = np.empty(N)

for i in n:
    x1[i] = np.sin(0.1*np.pi*i + np.pi/4)


mplt.stem(n, x1)
mplt.show()
mplt.stem(n, np.abs( np.fft.fft(x1)))
mplt.show()




