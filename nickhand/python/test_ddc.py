# 
#  test_ddc.py
#  <Radio: Digital Lab #2>
#  test to see if input signal has been digitally down converted
#  
#  Created by Nick Hand on 2012-10-11.
# 
import digital_utils, argparse
import pylab as pl

def test_down_conversion(args):
    """
    @brief test to see if input signal of known frequency has been down converted
    after mixing with known frequency
    """
    
    # define the timestep for the 2 time series
    dt_mixed = args.output_steps/args.clock_freq
    dt_true = 1./args.clock_freq
    
    # read in the data for mixed and input signals
    t_mixed, d_mixed = digital_utils.read_bram(args.mixed_file, timestep=dt_mixed, mixed=True)
    t_true, d_true = digital_utils.read_bram(args.input_file, timestep=dt_true, mixed=False)
    
    # get the power spectra of the signals
    f_mixed, p_mixed = digital_utils.power(d_mixed, dt_mixed)
    f_true, p_true = digital_utils.power(d_true, dt_true)
    
   
    # plot the input signal on first subplot
    pl.subplots_adjust(hspace=0.3)
    pl.subplot(211)
    pl.plot(f_true/1e6, p_true)
    
    # add the necessary info to the subplot
    pl.figtext(0.2, 0.85, 'input tone at %.3f MHz' %(args.input_freq/1e6))
    pl.xlabel('frequency (MHz)', fontsize=16)
    pl.ylabel('power', fontsize=16)
    pl.xlim(-1.5*args.input_freq/1e6, 1.5*args.input_freq/1e6)
    
    pl.subplot(212)
    
    # determine the expected down-converted frequency, as mixer frequency - input freq
    f_expected = abs(args.mixed_int * args.clock_freq / args.output_steps - args.input_freq)
    
    # plot the down-converted spectra 
    pl.plot(f_mixed/1e3, p_mixed)
    pl.figtext(0.2, 0.4, 'mixed tone at %.3f kHz' %(f_expected/1e3))
    pl.xlabel('frequency (kHZ)', fontsize=16)
    pl.ylabel('power', fontsize=16)
    pl.xlim(-1.5*f_expected/1e3, 1.5*f_expected/1e3)
    pl.show()
    
    return

if __name__ == '__main__':
    
    # parse the input arguments
    parser = argparse.ArgumentParser(description="test to see if input signal has been mixed properly")
    parser.add_argument('input_file', type=str, help='name of file containing true signal')
    parser.add_argument('mixed_file', type=str, help='name of file containing mixed input signal')
    parser.add_argument('--mixed_int', type=int, default=1, help='integer that corresponds to mixer frequency')
    parser.add_argument('--input_freq', type=float, default=10e6, help='freq of input tone in Hz')
    parser.add_argument('--clock_freq', type=float, default=200e6, help='clock frequency in Hz')
    parser.add_argument('--output_steps', type=float, default = 1024., help='clock steps per data output')
    
    args = parser.parse_args()
    
    test_down_conversion(args)
    
    