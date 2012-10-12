"""
Script to continuously accept BRAM binary information
over a UDP connection and plot them up.

TODO:
I'm worried that we're dropping packets while building the plot
&etc, so it may make sense to have two threads - one to continuously
pull in data and put it in an object, and one to read from that object
and plot and update the graph.

"""

import matplotlib.pyplot as plt
import numpy as np
import struct, socket
from scipy.ndimage.filters import gaussian_filter1d

class udp_interface_rx():
    
    def __init__(self, port=12345):
        # set up the UDC connection
        self.port = port
        self.max_recv_bytes = 8192*4
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind( ('0.0.0.0', port) )
        self.sock = sock
        
        self.bram = None # the most recent binary bram data received
        self.data = np.array([0,0]) # all of the data 
        self.max_plot_len = 100 # number of datapoints to show in plot
        self.max_data_len = int(1e4) # number of datapoints to keep track of


    def unpack_bram(self, bram_str=None, ddc=True):
        '''
        returns a numpy array of binary data in bram file
    
        ddc=False: array is the full signal
        ddc=True: array[::2] is mixed with cos(theta), and array[1::2] is mixed with sin(theta)
        '''
        if bram_str == None:
            bram_str = self.bram
        if not ddc:
            n_samps = len(bram_str)/4
            data = np.array(struct.unpack('>%di' %n_samps, bram_str))
        else:
            n_samps = len(bram_str)/2
            data = np.array(struct.unpack('>%dh' %n_samps, bram_str))
        return data
    
    def get_data(self):
        self.bram = self.sock.recv(self.max_recv_bytes)
        self.data = np.concatenate( (self.data, self.unpack_bram()) )[ -self.max_data_len: ]
        

    def spectrum(self, timeseries, tstep=5e-9*1024, ltrim=2, htrim='Nyquist', smoothness=0):
        '''
        produce the fft power spectrum of a timeseries consistently sampled
        tstep seconds apart.

        options:
          ltrim: number of points to trim from the lower end of the spectrum
          htrim: ditto for high end, or 'Nyquist'
          smoothness: the sigma of a gaussian kernel with which to smooth the power spectrum
        '''
        if htrim == 'Nyquist':
            htrim = len(timeseries)/2
        freq = np.fft.fftfreq(len(timeseries), tstep)[ ltrim:htrim ]
        fts  = np.fft.fft(timeseries)
        powr = abs(fts[ ltrim:htrim ])**2
        if smoothness:
            smth_powr = gaussian_filter1d( powr, smoothness )
            return freq, smth_powr
        else:
            return freq, powr

    def continuous_plot(self):
        # first collect enough data to fill buffer
        while len(self.data) < self.max_data_len:
            self.get_data()

        # now make a continuously-running plot of timeseries and the fft of data
        plt.ion()
        fig = plt.figure()
        
        time_ax = plt.subplot(2,1,1)
        to_plot = self.data[-self.max_plot_len*2:]
        line1, = time_ax.plot(to_plot[::2], c='b')
        line2, = time_ax.plot(to_plot[1::2], c='r')
        time_ax.set_xlabel('sample number')
        time_ax.set_ylabel('signal')

        fft_ax = plt.subplot(2,1,2)
        freq,powr = self.spectrum( self.data[1::2] + (0+1j)*self.data[::2] )
        line3, = fft_ax.plot( freq, powr, c='k')
        fft_ax.set_xlabel('Hz')
        fft_ax.set_ylabel('power')
        
        while True:
            self.get_data()
            to_plot = self.data[ -self.max_plot_len*2:] # truncate dual array to len points for each mixed signal
            line1.set_ydata( to_plot[::2] )
            line2.set_ydata( to_plot[1::2] )
            
            freq,powr = self.spectrum( self.data[1::2] + (0+1j)*self.data[::2] )
            line3.set_ydata( powr )
            
            plt.draw()
        

if __name__ == '__main__':
    interface = udp_interface_rx()
    interface.continuous_plot()
