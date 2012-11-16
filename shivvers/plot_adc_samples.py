'''
a quick script to look at the signals and frequencies from 
Radio Skillz Digital lab 1
'''

import struct
import numpy as np
import matplotlib.pyplot as plt

# open files as signed 32-bit integers
bram_str = open('bram_files/data_bram_10MHz','r').read()
n_samps = len(bram_str)/4
#data10 = struct.unpack('>{}i'.format(n_samps), bram_str)
data10 = struct.unpack('>%di' % n_samps, bram_str)

bram_str = open('bram_files/data_bram_90MHz','r').read()
#data90 = struct.unpack('>{}i'.format(n_samps), bram_str)
data90 = struct.unpack('>%di' % n_samps, bram_str)

bram_str = open('bram_files/data_bram_110MHz','r').read()
#data110 = struct.unpack('>{}i'.format(n_samps), bram_str)
data110 = struct.unpack('>%di' % n_samps, bram_str)

# clock is 200MHz, so each time step is 5 nanoseconds
x = np.linspace(0., 5e-6 * len(data10), len(data10)) #in seconds
plt.figure(1)
ax = plt.subplot(111)
cut = 50 #how much of the plot to show
ax.plot(x[:cut], data10[:cut], label='10MHz')
ax.plot(x[:cut], data90[:cut], label='90MHz')
ax.plot(x[:cut], data110[:cut], label='110MHz')
ax.set_xlabel('time (s)')
ax.set_ylabel('ADC value')
plt.title('Three signals sampled at 200MHz')
plt.legend()

# do a fft and make periodograms
n = len(data10)
freq = np.fft.fftfreq(n, 5e-6)
freq = np.hstack( (freq[:n/2], freq[n/2:3*n/4] - 2*freq[n/2]) )

f10 = np.fft.fft(data10)
power10 = np.hstack( (abs(f10[:n/2])**2, abs(f10[n/2:3*n/4])**2) )

f90 = np.fft.fft(data90)
power90 = np.hstack( (abs(f90[:n/2])**2, abs(f90[n/2:3*n/4])**2) )

f110 = np.fft.fft(data110)
power110 = np.hstack( (abs(f110[:n/2])**2, abs(f110[n/2:3*n/4])**2) )


# make plots to compare these
f, axs = plt.subplots(nrows=3, ncols=1, sharex=True)
axs[0].plot(freq, power10)
axs[1].plot(freq, power90)
axs[2].plot(freq, power110)

labels = ['10MHz', '90MHz', '110MHz']
for i,ax in enumerate(axs):
    ylow, yhigh = ax.axis()[2:]
    ax.set_yticklabels([])
    ax.set_ylabel( labels[i] )
    ax.vlines(1e5, ylow, yhigh, color='k', linestyles='dashed', label='Nyquist') #show the nyquist frequency
axs[2].set_xlabel( 'Frequency (Hz)' )
axs[0].set_title('Periodograms of three signals')
axs[0].legend()
plt.show()


