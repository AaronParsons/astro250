# 
#  digitalUtils.py 
#  functions for dealing with reading/plotting digitally sampled signals
#  
#  Created by Nick Hand on 2012-10-10.
# 
import argparse, struct
import numpy as np
import pylab as pl
from scipy.ndimage import gaussian_filter1d

def read_bram(filename, timestep = 5e-9, filtered=False):
    """
    @brief plot the digitally sampled time series 
    stored in filenames as binary, assuming 32 bit integers
    
    @param filenames: the filenames to read in (list)
    @param f_s: the sampling rate which determines the time step (float)
    """
    data = file(filename, 'r').read()
        
    
    if not filtered: 
        N_samps = len(data)/4
        data = struct.unpack('>%di' %N_samps, data)
        times = np.arange(0, N_samps*timestep, timestep )
        
        return times, data
        
    else:
        N_samps = len(data)/2
        data = struct.unpack('>%dh' %N_samps, data)
        times = np.arange(0, N_samps*timestep/2.0, timestep )

        cos = data[0::2]
        sin = data[1::2]
        
        return times, cos, sin

def power(signal, timestep, smoothing=0, keepDC=False):
    
    
    if not keepDC:
        dc = np.mean(signal)
        signal -= np.mean(signal)
    
    freqs = np.fft.fftfreq(len(signal), d=timestep)
    fft = np.fft.fft(signal)
    
    power = abs(fft)**2
    if smoothing:
        power = gaussian_filter1d(power, smoothing)
    
    return np.fft.fftshift(freqs), np.fft.fftshift(power)       
    
    
    