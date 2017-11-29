from __future__ import division, print_function, absolute_import
import numpy as np
import matplotlib.pyplot as plt


LAT1 = [0.70, 0.42]
LAT2 = [0.70, 0.42]


LAT = [LAT1, LAT2, LAT3, LAT4, LAT5, LAT7]
LATm = [LAT[i][0][0] for i in range(len(LAT))]


plt.close('all')
plt.figure()
plt.subplot(121), plt.plot(LATm), plt.title(np.mean(LATm))
plt.subplot(122), plt.plot(LCKm), plt.title(np.mean(LCKm)) 
plt.show()