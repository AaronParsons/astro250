'''

quick script to find the filter function in digital lab 2
'''

import struct
import matplotlib.pyplot as plt
import numpy as np

######################################################

def read_bram(file_name):
    ''' returns a numpy array of binary data in bram file '''
    bram_str = open(file_name,'r').read()
    n_samps = len(bram_str)/4
    data = np.array(struct.unpack('>{}i'.format(n_samps), bram_str))
    return data
    
def spectrum(timeseries, tstep=5e-9, ltrim=2, htrim='Nyquist', smoothness=10):
    '''
    plot the fft spectrum of a timeseries consistently sampled
    tstep seconds apart.
    
    options:
      ltrim: number of points to trim from the lower end of the spectrum
      htrim: ditto, or 'Nyquist'
      smoothness: the sigma of a gaussian kernel with which to smooth the data
    '''
    if htrim == 'Nyquist':
        htrim = len(timeseries)/2
    freq = np.fft.fftfreq(len(timeseries), tstep)[ ltrim:htrim ]
    fts  = np.fft.fft(timeseries)
    powr = abs(fts[ ltrim:htrim ])**2
    
    # plot it
    fig = plt.figure()
    plt.plot(freq, powr, c='k')
    plt.xlabel( 'Frequency (Hz)' )
    plt.ylabel('Power')
    
    if smoothness:
        from scipy.ndimage.filters import gaussian_filter1d
        smth_powr = gaussian_filter1d( powr, smoothness )
        plt.plot( freq, smth_powr, c='r', lw=2 )
        return fig, freq, smth_powr
    else:
        return fig, freq, powr

######################################################


data = read_bram('bram_files/data_bram_lp100_fs200')
f, freq, powr = spectrum(data, smoothness=200)
plt.title('Unfiltered noise')
data = read_bram('bram_files/data_bram_lp100_fs200_convolved')
f2, freq_filt, powr_filt = spectrum(data, smoothness=200)
plt.title('Filtered noise')

plt.figure()
plt.plot(freq, powr_filt/powr)

# compare to sinc function
y = np.sinc(freq/freq[-1])/(freq/freq[-1])
plt.plot( freq, y )

ax = plt.axis()
plt.axis( [ax[0], ax[1], 0, 5] )
plt.xlabel('frequency (Hz)')
plt.ylabel('response')
plt.title('Filter response vs sinc')
plt.show()

