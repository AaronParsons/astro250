'''
This script is designed to collect a set of samples using
a ROACH as set up in Digital Lab 2 (Radio Skillz class)
so as to characterize the filter function of the 1024-adder.
The idea is to set the input tone at our Nyquist frequency,
and mix with a set of internal signals that range from Nyquist
down to zero Hz.  This would yeild a set of measurements
that sample the filter function from 0Hz to Nyquist.
See below, because this doesn't actually work.

HOW TO USE:
 - set clock to 200MHz
 - set input sine wave at 100MHz
 - run this script


IMPORTANT:
I wrote this at home, before actually playing with the ROACH.

This does not actually work, because our frequency resolution
for the internal mixing signal is about 200KHz (so each time we
increment the value in the `freq` file we increase the internal
mixing frequency by ~200KHz), and the way in which we sample the 
post-mixing signal has an effective sampling rate of 200KHz.
So, our effective Nyquist frequency is ~100KHz, but smallest amount
we can change the post-mixing signal frequency is 200KHz, so we can
only put 
'''

#######################################################
# Variables to adjust:
log_range_args = (3, 8.9, 1e4) #log10 Hz
t_wait         = .01 #seconds
clock_freq     = 2e8 #Hz
trigger_file   = 'trig'
freq_file      = 'freq'
original_bram  = 'data_bram'
filtered_bram  = 'ddc_bram'


#######################################################
import struct, pickle
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from scipy.ndimage.filters import gaussian_filter1d


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

def set_LO(f, ncounter=2**10):
    ''' set the ROACH's internal sine/cos wave as close as possible to f Hz '''
    # if one tries to set LO above Nyquist, return an error (fails in ROACH anyways)
    assert( f < clock_freq/2 )
    fund_freq = clock_freq/ncounter
    multiplier = int(f/fund_freq)  #an integer, so we have limited resolution
    binary_string = struct.pack('>i', multiplier)
    open(freq_file).write(binary_string)
    # return the true frequency to which it was set, for our records
    return multiplier*fund_freq

def collect_sample():
    ''' collect a single sample '''
    open(trigger_file).write( struct.pack('>i', 1) )
    sleep(t_wait)
    open(trigger_file).write( struct.pack('>i', 0) )


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

# tstep for filtered response is different because it filters serially, not parallel-wise
tstep_filt = (clock_freq/1024)**-1

x,y = [],[] #lists for tracking frequency tested (x) and filter function (y)
whole_shebang = {}
for i,freq in enumerate( np.logspace(*log_range_args) ):
    print 'working on sample',i,'of',log_range_args[-1]
    true_LO = set_LO( freq )
    collect_sample()
    
    filt = read_bram(filtered_bram, filtered=True)
    f_cos = filt[::2]
    f_sin = filt[1::2]
    filt = f_cos + (0+1j)*f2
    freq_filt, powr_filt = spectrum(filt, tstep=tstep_filt)
    
    imf = np.argmax( powr_filt )
    x.append( filt[imo] )
    y.append( powr_filt[imf] )
    whole_shebang[true_LO] = [freq_filt, powr_filt]

# save for posterity
pickle.dump( whole_shebang, open('saved_trials.p','w') )

# plot the final filter function
plt.plot(x,y)
plt.title('power as a function of post-mixing frequency')
plt.xlabel('Hz')
plt.ylabel('Power')
plt.show()
