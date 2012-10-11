#! /opt/local/bin/python -u
import numpy as n
import pylab as p
import optparse,sys


def quantize(volts, bits):
    '''Quantizer function: 
        volts = input array. can be list.
        bits = number of bits to quantize too.
    ''' 
    qvolts = volts
    qvolts = n.round(qvolts * 2**(bits))
    qvolts = (qvolts/2**(bits))
    qvolts[n.where(qvolts >= (2**(bits-1))-1)] = 2**(bits-1) - 1
    qvolts[n.where(qvolts <= -1*(2**(bits-1)))] = -1*2**(bits-1)
    return qvolts
    
def plotter(inrms,outrms,log=False):
    rng = len(inrms.keys()) 
    rng1 = len(outrms.keys())
    if rng != rng1: 
        print 'Dictionaries not the same size...Exiting'
        exit()
    if log:
        for i in range(1,rng+1):
            p.semilogy(n.log2(n.array(inputrms[i])),n.array(outputrms[i])/n.array(inputrms[i]),label='%d bit quantization'%(i))
    else:
        for i in range(1,rng+1):
            p.plot(n.log2(n.array(inputrms[i])),n.array(outputrms[i])/n.array(inputrms[i]),label='%d bit quantization'%(i))
    p.axhline(1, linestyle='--', color='k')
    p.title('Power Transfer function for 1,2,3,4 bit quantization')
    p.xlabel('log2 input_rms')
    p.ylabel('rms_in/rms_out')
    p.legend()


########################################################################################
o = optparse.OptionParser()
o.add_option('--log', action='store_true', dest='log',
            help='Make plot in log space.')

opts,args = o.parse_args(sys.argv[1:])



#rms array
prange = 2**n.arange(-8,8,.01)
#dictionaries to hold input rms and out put rms for different quant bits.
inputrms = {}
outputrms = {}
for quant in range(1,5):
    inputrms[quant] = []
    outputrms[quant] = []
    for rms in prange:
        v = n.random.randn(1e4)*rms
        inputrms[quant].append(n.std(v))
        qv = quantize(v,quant)
        outputrms[quant].append(n.std(qv))
        
plotter(inputrms,outputrms, log=opts.log)
p.show()



    
    
