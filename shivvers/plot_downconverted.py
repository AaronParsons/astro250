'''
Quick script to plot the power from our signal after being
run through the downconverter .bof file.

'''

import struct
import matplotlib.pyplot as plt
import numpy as np

#######################################################

def read_bram(file_name, filtered=False):
    '''
    returns a numpy array of binary data in bram file
    
    unfiltered: returned array is simply time series
    filtered: array[::2] is mixed with cos(theta), and array[1::2] is mixed with sin(theta)
    '''
    bram_str = open(file_name,'r').read()
    if not filtered:
        n_samps = len(bram_str)/4
        data = np.array(struct.unpack('>%di' %n_samps, bram_str))
    else:
        n_samps = len(bram_str)/2
        data = np.array(struct.unpack('>%dh' %n_samps, bram_str))
    return data

def spectrum(timeseries, tstep=5e-9, ltrim=2, htrim='Nyquist', smoothness=0):
    '''
    produce the fft power spectrum of a timeseries consistently sampled
    tstep seconds apart.

    options:
      ltrim: number of points to trim from the lower end of the spectrum
      htrim: ditto for high end, or 'Nyquist'
      smoothness: the sigma of a gaussian kernel with which to smooth the power spectrum
    '''
    if htrim == 'Nyquist':
        htrim = len(timeseries)/2
    freq = np.fft.fftfreq(len(timeseries), tstep)[ ltrim:htrim ]
    fts  = np.fft.fft(timeseries)
    powr = abs(fts[ ltrim:htrim ])**2
    if smoothness:
        smth_powr = gaussian_filter1d( powr, smoothness )
        return freq, smth_powr
    else:
        return freq, powr

#######################################################

# since we sample only once every 1024 clocks, we have a much larger
#  time step between samples in our ddc_bram file
mixed_tstep = 2**10 * 5e-9

data = read_bram('bram_files/ddc_bram_9.981MHz_freq51', filtered=True)
sin  = data[::2]
cos  = data[1::2]
full = cos + (0+1j)*sin
f,p  = spectrum(full, tstep=mixed_tstep)
plt.plot(f,p, c='k')
plt.title('Power expected around 20KHz')
plt.ylabel('power')
plt.xlabel('Hz')
plt.show()

