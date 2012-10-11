'''
A demonstration that power transfer of a quantized
signal depends on the quantization resolution.

This shows that, for each bit depth, there is a range
where power out is equal to power in (a plateau in the plot),
but that for values outside of that range, power out stays
constant as a function of power in (below the minimum resolution
and above the clipping level of our quantizer).
'''

import numpy as np
import matplotlib.pyplot as plt

def quantize_me(signal, bits):
    ''' return the quantized signal to bits depth, assuming signal has a mean of zero '''
    minn = -int(2**bits)/2
    maxx = int(2**bits)/2+1
    quantized = np.round(signal).astype('int') #assumes we quantize by rounding
    #quantized = np.array(signal).astype('int') #assumes we quantize by clipping
    quantized[ quantized<minn ] = minn
    quantized[ quantized>maxx ] = maxx  
    return np.array(quantized)


multipliers = np.logspace(0, 5, num=500)
bit_depths  = [1,2,4,8,16]
powers_in   = np.empty(len(multipliers))
powers_out  = np.empty( [len(multipliers), len(bit_depths)] )
for i,mult in enumerate(multipliers):
    if not i%100: print 'working on',i
    x = np.linspace(-6*np.pi, 6*np.pi, 1000)
    signal = mult*np.sin(x)
    p_sig = np.trapz(signal**2)/(x[-1]-x[0])
    powers_in[i] = p_sig
    for j,depth in enumerate(bit_depths):
        sig_q = quantize_me(signal, depth)
        p_sig_q = np.trapz(sig_q**2)/(x[-1]-x[0])
        powers_out[i,j] = p_sig_q

for j in range(len(bit_depths)):
    plt.loglog(powers_in, powers_out[:,j]/powers_in, label=str(bit_depths[j])+' bits')

plt.xlabel(r'$P_{in}$')
plt.ylabel(r'$P_{out} / P_{in}$')
plt.legend(loc='best')
plt.show()