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
    
    output_steps = 2**args.freq_bits
    
    # define the timestep for the 2 time series
    dt_ddc = output_steps/args.clk
    dt_data = 1./args.clk
    
    # read in the data from the ddc_bram and data_bram files
    t_ddc, d_ddc = digital_utils.process_ddc_bram(args.ddc_file, timestep=dt_ddc)
    t_data, d_data = digital_utils.process_data_bram(args.data_file, timestep=dt_data)
    
    # get the power spectra of the signals
    f_ddc, p_ddc = digital_utils.power(d_ddc, dt_ddc)
    f_data, p_data = digital_utils.power(d_data, dt_data)
    
    # plot the input signal on first subplot
    pl.subplots_adjust(hspace=0.3)
    pl.subplot(211)
    pl.plot(f_data/1e6, p_data)
    
    # add the necessary info to the subplot
    pl.figtext(0.2, 0.85, 'input tone at %.3f MHz' %(args.input_freq/1e6))
    pl.xlabel('frequency (MHz)', fontsize=16)
    pl.ylabel('power', fontsize=16)
    pl.xlim(-1.5*args.input_freq/1e6, 1.5*args.input_freq/1e6)
    
    pl.subplot(212)
    
    # determine the expected down-converted frequency, as mixer frequency - input freq
    f_expected = abs(args.lof_int * args.clk / output_steps - args.input_freq)
    
    # plot the down-converted spectra 
    pl.plot(f_ddc/1e3, p_ddc)
    pl.figtext(0.2, 0.4, 'mixed tone at %.3f kHz' %(f_expected/1e3))
    pl.xlabel('frequency (kHZ)', fontsize=16)
    pl.ylabel('power', fontsize=16)
    pl.xlim(-1.5*f_expected/1e3, 1.5*f_expected/1e3)
    pl.show()
    
    return

if __name__ == '__main__':
    
    # parse the input arguments
    parser = argparse.ArgumentParser(description="test to see if input signal has been mixed properly")
    parser.add_argument('data_file', type=str, help='name of file containing true signal')
    parser.add_argument('ddc_file', type=str, help='name of file containing mixed input signal')
    parser.add_argument('--lof_int', type=int, default=1, help='integer corresponding to the local oscillator freq')
    parser.add_argument('--input_freq', type=float, default=10e6, help='freq of input tone in Hz')
    parser.add_argument('--clk', type=float, default=200e6, help='clock frequency in Hz')
    parser.add_argument('--freq_bits', type=float, default = 10, help='num of bits in the frequency period is 2**freq_bits')
    
    args = parser.parse_args()
    
    test_down_conversion(args)
    
    