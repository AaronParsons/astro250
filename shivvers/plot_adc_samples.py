'''
a quick script to look at the signals and frequencies from 
Radio Skillz Digital lab 1
'''

import struct
import numpy as np
import matplotlib.pyplot as plt

# open files as signed 32-bit integers
bram_str = open('bram_files/data_bram_10MHz','r').read()
data10 = struct.unpack('{}i'.format(len(bram_str)/4), bram_str)

bram_str = open('bram_files/data_bram_90MHz','r').read()
data90 = struct.unpack('{}i'.format(len(bram_str)/4), bram_str)

bram_str = open('bram_files/data_bram_110MHz','r').read()
data110 = struct.unpack('{}i'.format(len(bram_str)/4), bram_str)

# clock is 200MHz, so each time step is 5 nanoseconds
x = np.linspace(0., 5e-6 * len(data10), len(data10))
plt.figure(1)
ax = plt.subplot(111)
ax.plot(x[:100], data10[:100], label='10MHz')
ax.plot(x[:100], data90[:100], label='90MHz')
ax.plot(x[:100], data110[:100], label='110MHz')
ax.set_xlabel('time (s)')
plt.title('Three signals sampled at 200MHz')
ax.set_yticklabels([])
plt.legend()

# do a fft and make periodograms
n = len(data10)
freq = np.fft.fftfreq(n, 5e-6)[:n/2] #include nyquist cutoff

f10 = np.fft.fft(data10)
power10 = abs(np.array(f10[:n/2]))**2  #include nyquist cutoff

f90 = np.fft.fft(data90)
power90 = abs(np.array(f90[:n/2]))**2  

f110 = np.fft.fft(data110)
power110 = abs(np.array(f110[:n/2]))**2 


# make plots to compare these
f, axs = plt.subplots(nrows=3, ncols=1, sharex=True)
axs[0].plot(freq, power10)
axs[1].plot(freq, power90)
axs[2].plot(freq, power110)

labels = ['10MHz', '90MHz', '110MHz']
for i,ax in enumerate(axs):
    ax.set_yticklabels([])
    ax.set_ylabel( labels[i] )
axs[2].set_xlabel( 'Frequency (Hz)' )
axs[0].set_title('Periodograms of three signals')
plt.show()


