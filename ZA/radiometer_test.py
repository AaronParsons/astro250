#!/opt/local/bin/python -u
'''This script simulates random noise corresponding to a noise tempereature, 
   and demonstrates that the radiometer equation works. That is, 
    P**2 = T/sqrt(Bt) [not 2Bt] ''' 


import numpy as n, pylab as p
import optparse, sys
import scipy.stats as ss

def gen_n_spec(nspec, samp_freq, temp):
    '''Generates an integrated spectra.
       nspec: Number of spetra to integrate.
       samp_freq: number of samples per spectra.
       tsys: system temperature of each spectra. '''

    means = []
    for spec in xrange(nspec):
        v = n.sqrt(temp)*n.random.randn(samp_freq)
        pwr = v**2
        means.append(n.std(pwr)) #rms temp is std dev of power spec. 
    print n.mean(means)
    return means
    

o = optparse.OptionParser()
o.add_option('-t', dest='temp', type='int', default='70',
             help='Temperature of spectra (Kelvin).')
o.add_option('-s', dest='samp_frq', type='int', default=2**15 ,
             help='Sampling frequency.')

opts,args = o.parse_args(sys.argv[1:]) 

#define the sampling frequeuncy. In this case it is just the number of random
#samples we want. We can take this to be 1MHz for arguments sake.Our observable
#bandwith is then just B = samp_freq/2.
nspec = opts.samp_frq
temp = opts.temp

#generate a range of the number of 'channels'. which will effectively increase
#the bandwith.  
x = 2**n.arange(3,13)
#holder for sandard devs.
stderrs = []
for samp_freq in x:
    print '.',
    data = gen_n_spec(nspec,samp_freq,temp)
    stderrs.append(n.std(data))
    print stderrs
p.loglog(x,n.array(stderrs), label='Simulated data')
p.loglog(x,temp*(2)/(n.sqrt(x)), label='Theoretical')
p.loglog(x,temp/(n.sqrt(x)), label='Theoretical with sqrt(2)')
p.legend()
p.show()
 
