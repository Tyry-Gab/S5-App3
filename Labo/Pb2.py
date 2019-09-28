import matplotlib.pyplot as mplt
import numpy as np
from scipy import signal

x = [0.5, 1.8]
h = [1, 0.5]
j = np.sqrt(1)

H = [1.5, 0.75 - 0.433j, 0.75 + 0.433j ]
X = [2.3, 0.4 -1.55j, 0.4+1.55j]
Y = []



y = np.convolve(x,h)

print(h)