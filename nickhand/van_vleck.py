# 
#  van_vleck.py
#  <Radio: Digital lab 1, plot power transfer curves>
#  
#  Created by Nick Hand on 2012-09-28.
# 
from scipy.stats import norm
import numpy as np
import pylab as pl
import argparse

def quantize(signal, bit, max_val):
    """
    @brief quantize the signal given a level of bit sampling 
    and max value for quantization range
    
    @param signal: input signal to quantize (array)
    @param bit: the number of bits for 2**bit quant levels (int)
    @param max_val: max of quantization range (float)
    
    @return quantized_signal: the quantized input signal (array)
    """

    levels = 2**bit
    level_size = max_val*2/levels

    quantized_signal = np.ones(len(signal))*max_val
    
    if bit == 1:
        inds = np.where(signal <= 0)[0]
        quantized_signal[inds] = 0.0
        
        return quantized_signal
        
    
    for i in range(1, levels):
        
        lower =  max_val-level_size*i
        upper = max_val-level_size*(i-1)

        if i == levels-1:
            inds = np.where(signal <= upper)[0]
            quantized_signal[inds] = lower
        else:
            inds = np.where((signal <= upper)*(signal > lower ))[0]
            quantized_signal[inds] = lower
        
    
    return quantized_signal
        
        
    
def plot_power_transfer_curves(bits, p_in_max=100., quantization_max=1.0):
    """
    @brief plot power transfer curves for a given bit quantization level
    
    @param bits: number of bits for sampling (list of ints)
    @param p_in_max: max input power amplitude (float)
    @param quantization_max: max of quantization range (float)
    """
    
    # input voltage rms
    sigmas_in = np.logspace(-3, np.log10(np.sqrt(p_in_max)), 1000)
    
    # plot transfer curve for each input bit
    for bit in bits:

        pout_over_pin = [] # ratio of output power to input power
        p_ins         = [] # input powers 


        # run for various power inputs
        for sigma in sigmas_in:
            
            # input voltage is white noise with mean 0 and std dev sigma    
            voltage = norm.rvs(loc=0.0, scale=sigma, size=10000)
            
            # quantize the signal given a bit sampling
            quantized_signal = quantize(voltage, bit, quantization_max)
            
            # power is the mean squared voltage 
            p_out = np.mean(quantized_signal**2)
            p_in = np.mean(voltage**2)
            
            pout_over_pin.append(p_out/p_in)
            p_ins.append(p_in)
        
        
        # plot and label the power transfer curve in loglog space
        lab = '1 bit' if bit == 1 else '%d bits' %bit
        pl.loglog(p_ins, pout_over_pin, label=lab)
        
    pl.legend(loc='upper right')
    pl.xlabel(r'$P_\mathrm{in}$ (arbitrary units)', fontsize=16)
    pl.ylabel(r'$P_\mathrm{out} / P_\mathrm{in}$', fontsize=16)
    pl.title("Power Transfer Curves for Various Quantization Levels")
    pl.show()
    
    return  
            

if __name__ == '__main__':    
    
    # parse the input arguments
    parser = argparse.ArgumentParser(description="Plot power transfer curves for various quantization levels")
    parser.add_argument('bits', metavar='N', type=int, nargs='+', help='integers represent bit sampling for quantization')
    parser.add_argument('--input_max', type=float, help='maximum value of input power')
    parser.add_argument('--quant_max', type=float, help='maximum value of quantization range')
    args = parser.parse_args()
    
    plot_power_transfer_curves(args.bits, p_in_max=args.input_max, quantization_max=args.quant_max)
