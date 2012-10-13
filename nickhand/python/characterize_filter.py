# 
#  characterize_filter.py
#  <Radio: Digital Lab #2>
#  characterize the filter shape that has been convolved with input noise signal
#
#  Created by Nick Hand on 2012-10-11.
# 
import mpfit
import argparse, digital_utils
import pylab as pl
import numpy as np

def fitFilter(x, y, model='gaussian', bandpass=100):
    """
    @brief fit the filter function specified by y, using the function
    specified by fitfunc
    
    @param x: the x array to use
    @param y: the y array to use
    @param model: the model function to use (either 'gaussian' or 'sinc')
    @param bandpass: bandpass of input frequency array (in MHz)
    
    @return x,y corresponding to best fit model
    """
    
    def modelFunction(x, p, func=model):
        
        # params:
        #### p[0] = A
        #### p[1] = B

        A, B = p[0], p[1]
        
        if func == 'gaussian':
            return A*np.exp(-B*x**2)
        elif func == 'sinc':
            return A*np.sin(B*x) / (B*x)

    def fittingFunction(p, fjac=None, x=None, y=None, err=None, func=model):

        # parameter values are passed in 'p'
        # if fjac == None, then partial derivatives should not be computed.
        # It will always be None if MPFIT is called with default flag.

        m = modelFunction(x, p, func=model)

        status = 0
        return ([status, (y-m)/err])
        
    # measure the amplitude
    p0 = [4, 1/bandpass]
    fa = {'x': x, 'y': y, 'err': y*0.1}

    m = mpfit.mpfit(fittingFunction, p0, functkw=fa)
    A, B = m.params[0], m.params[1]
    
    return x, modelFunction(x, m.params, func=model)

if __name__ == '__main__':
    
    # parse the input arguments
    parser = argparse.ArgumentParser(description="charactize digital filter for input signal")
    parser.add_argument('signal_file', type=str, help='name of file containing true input signal')
    parser.add_argument('convolved_file', type=str, help='name of file containing convolved signal')
    parser.add_argument('--dt', type=float, default=5e-9, help='timestep of data file')
    parser.add_argument('--keepDC', action='store_false', help='do not remove DC bias from input signal')
    parser.add_argument('--smoothing', type=int, default=0, help='kernel of gaussian smoothing function to apply to power spectra')
    parser.add_argument('--fitGaussian', action='store_true', help='whether to fit a gaussian to filter shape')
    parser.add_argument('--fitSinc', action='store_true', help='whether to fit a sinc to filter shape')
    
    args = parser.parse_args()
    
    # proces the data from the convolved and true input signal files
    t_conv, d_conv = digital_utils.process_data_bram(args.convolved_file, timestep=args.dt)
    t_true, d_true = digital_utils.process_data_bram(args.signal_file, timestep=args.dt)
    
    # get the power spectra
    f_conv, p_conv = digital_utils.power(d_conv, args.dt, smoothing=args.smoothing, keepDC=args.keepDC)
    f_true, p_true = digital_utils.power(d_true, args.dt, smoothing=args.smoothing, keepDC=args.keepDC)
    
    # restrict the filter to positive frequencies
    filt = p_conv/p_true
    inds = np.where(f_true > 0)[0]
    filt = filt[inds]
    f_true = f_true[inds]/1e6 # now in MHz
    
    # plot the filter
    pl.plot(f_true, filt, c='k', label='recovered filter')
    
    # fit the filter to a gaussian and sinc and plot
    if args.fitGaussian:
        t, f_fitted = fitFilter(f_true, filt, model='gaussian', bandpass=np.amax(f_true))
        pl.plot(t, f_fitted, c='b', label='best fit gaussian')
    if args.fitSinc:
        t, f_fitted = fitFilter(f_true, filt, model='sinc', bandpass=np.amax(f_true))
        pl.plot(t, f_fitted, c='r', label='best fit sinc')
    
    # label and show
    pl.legend(loc='upper right', prop={'size':16})
    pl.xlabel("frequency (MHz)", fontsize=16)
    pl.ylabel("amplitude", fontsize=16)
    pl.show()
