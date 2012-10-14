# 
#  digital_utils.py 
#  functions for dealing with reading/plotting digitally sampled signals
#  
#  Created by Nick Hand on 2012-10-10.
# 
import argparse, struct
import numpy as np
import pylab as pl
from scipy.ndimage import gaussian_filter1d


def compute_lof_int(f_MHz, clk_MHz=200., freq_bits=10):
    """
    @brief compute the integer corresponding to the 
    local oscillator frequency (LOF)
        
    @param f_MHz: the desired LOF to set in MHz (float)
    @param clk_MHZ: the clock frequency of the ROACH in MHz (float)
    @param freq_bit: number of bits in the frequency period is 2**freq_bits (int)
    """
    
    # compute the int corresponding to desired LOF
    lof_int = int(f_MHz / clk_MHz * 2**freq_bits)

    return lof_int
    
def process_ddc_bram(filename, timestep = 5e-9, data=None):
    """
    @brief convert binary representation of ddc_bram file into 
    timestream of data
    
    @param filename: the name of the ddc_bram file
    @param data: binary representation of data from ddc_bram (str)
    @param timestep: the timestep in seconds of the data (float)
    @param data: the binary representation of the data (string)
    
    @return times, data: the processed timestream values
    """ 
    if data is None:
        # read the data if not supplied already
        data = open(filename, 'r').read()
    
    # number of samples in data to read
    N_samps = len(data)/2
    
    # unpack the binary data, in 2 byte packets 
    data = struct.unpack('>%dh' %N_samps, data)
    
    # the corresponding times for each sample
    times = np.arange(0, N_samps*timestep/2., timestep )

    # get the sin/cos components of the read values
    sin = np.array(data[0::2])
    cos = np.array(data[1::2])
    data = cos + 1j*sin
    
    return times, data
    
def process_data_bram(filename, timestep=5e-9, data=None):
    """
    @brief convert binary representation of data_bram file into 
    timestream of data
    
    @param filename: the name of the data_bram file
    @param data: binary representation of data from ddc_bram (str)
    @param timestep: the timestep in seconds of the data (float)
    @param data: the binary representation of the data (string)

    @return times, data: the processed timestream values
    """
    if data is None:
        # read the data, if not supplied already
        data = open(filename, 'r').read()
    
    # number of samples to read
    N_samps = len(data)/4
    
    # unpack the binary data, in 4 byte packets
    data = struct.unpack('>%di' %N_samps, data)
    
    # the corresponding times for each sample
    times = np.arange(0, N_samps*timestep, timestep )
        
    return times, np.array(data)

def power(signal, timestep, smoothing=0, keepDC=False):
    """
    @brief compute the power spectrum of the input signal
    
    @param signal: the input signal to find spectrum of (array)
    @param timestep: the timestep between signal samples (float)
    @param smoothing: the kernel of the gaussian filter to smooth power with (int)
    @param keepDC: whether to keep any DC signals in the input signal (bool)
    
    @return freqs, power: the power spectrum and corresponding frequencies
    """
    
    # remove the DC bias from the input signal
    if not keepDC:
        dc = np.mean(signal)
        signal -= np.mean(signal)
    
    # get the frequencies corresponding to the times
    freqs = np.fft.fftfreq(len(signal), d=timestep)
    
    # take the FFT
    fft = np.fft.fft(signal)
    
    # get power from the FFT
    power = abs(fft)**2
    
    # smooth power with a Gaussian, if smoothing is nonzero
    if smoothing:
        power = gaussian_filter1d(power, smoothing)
        
    # return the shifted frequency and power array
    freqs, power = np.fft.fftshift(freqs), np.fft.fftshift(power)       

    return freqs, power
    
    