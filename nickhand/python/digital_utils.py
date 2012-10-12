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

def read_bram(filename, timestep = 5e-9, mixed=False, wordlength=4):
    """
    @brief plot the digitally sampled time series 
    stored in filenames as binary, assuming 32 bit integers
    
    @param filenames: the filenames to read in (list)
    @param timestep: the timestep in secs of the data (float)
    @param mixed: is the data storing a mixed signal (with sin/cos components)(bool)
    @param wordlength: number of bytes per value (int)
    
    @return times, data: the timestream that has been read
    """
    data = file(filename, 'r').read()
        
    
    if not mixed: 
        N_samps = len(data)/wordlength
        data = struct.unpack('>%di' %N_samps, data)
        times = np.arange(0, N_samps*timestep, timestep )
        
    else:
        N_samps = len(data)/(wordlength/2)
        data = struct.unpack('>%dh' %N_samps, data)
        times = np.arange(0, N_samps*timestep/2., timestep )

        sin = np.array(data[0::2])
        cos = np.array(data[1::2])

        data = cos + 1j*sin
        
    return times, data

def power(signal, timestep, smoothing=0, keepDC=False):
    """
    @brief compute the power spectrum of the input signal
    
    @param signal: the input signal to find spectrum of (array)
    @param timestep: the timestep between signal samples (float)
    @param smoothing: the kernel of the gaussian filter to smooth power with (int)
    @param keepDC: whether to keep any DC signals in the input signal (bool)
    
    @return freqs, power: the power spectrum and corresponding frequencies
    """
    
    
    if not keepDC:
        dc = np.mean(signal)
        signal -= np.mean(signal)
    
    freqs = np.fft.fftfreq(len(signal), d=timestep)
    fft = np.fft.fft(signal)
    
    power = abs(fft)**2
    if smoothing:
        power = gaussian_filter1d(power, smoothing)
    
    return np.fft.fftshift(freqs), np.fft.fftshift(power)       
    
    
    