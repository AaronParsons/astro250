import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

#get the frequency response of a summing filter
h, w = scipy.signal.freqz([1,1],whole=True)

#plot in log scale
plt.semilogy(h,np.abs(w))
#put cutoff at 70 db down
plt.ylim([pow(10,-7),pow(10,1)])
plt.show()