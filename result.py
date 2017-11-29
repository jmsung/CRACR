from __future__ import division, print_function, absolute_import
import numpy as np
import matplotlib.pyplot as plt


LAT1 = [[0.63, 0.10], [0.48, 0.11], [0.55, 0.19]] 
LAT2 = [[0.65, 0.19], [0.43, 0.15], [0.39, 0.31]] 
LAT3 = [[0.72, 0.10], [0.80, 0.05], [0.66, 0.09]] 
LAT4 = [[0.81, 0.08], [0.40, 0.10], [0.38, 0.09]] 
LAT5 = [[0.75, 0.11], [0.39, 0.21], [0.35, 0.24]] 
LAT7 = [[0.74, 0.14], [0.46, 0.14], [0.42, 0.25]] 
LAT = [LAT1, LAT2, LAT3, LAT4, LAT5, LAT7]
LATm = [LAT[i][0][0] for i in range(len(LAT))]

LCK1 = [[0.79, 0.03], [0.57, 0.07], [0.65, 0.08]] 
LCK2 = [[0.35, 0.11], [0.26, 0.18], [0.27, 0.18]] 
LCK3 = [[0.60, 0.11], [0.33, 0.11], [0.48, 0.10]] 
LCK4 = [[0.73, 0.06], [0.51, 0.15], [0.56, 0.09]] 
LCK5 = [[0.22, 0.17], [0.07, 0.25], [0.15, 0.07]] 
LCK = [LCK1, LCK2, LCK3, LCK4, LCK5]
LCKm = [LCK[i][0][0] for i in range(len(LCK))]

plt.close('all')
plt.figure()
plt.subplot(121), plt.plot(LATm), plt.title(np.mean(LATm))
plt.subplot(122), plt.plot(LCKm), plt.title(np.mean(LCKm)) 
plt.show()