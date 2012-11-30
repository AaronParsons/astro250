"""
Script to continuously accept BRAM binary information
over a UDP connection and plot them up.

TODO:
- test with live data stream

"""

import matplotlib.pyplot as plt
import numpy as np
import struct, socket
from scipy.ndimage.filters import gaussian_filter1d
import multiprocessing as mp

class udp_interface_rx():
    '''
    an interface to the UDP connection, designed to be run parallel
    to the plotting class with multiprocessing.
    '''
    def __init__(self, pipe_out, port=12345):
        # set up the UDP connection
        self.port = port
        self.max_recv_bytes = 8192*4 * 2 #set to twice the maximum that could be sent, to be safe
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind( ('0.0.0.0', port) )
        self.sock = sock
        
        self.bram = None # the most recent binary bram data received
        self.pipe = pipe_out # the end of the pipe into which we feed data


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
        # get a UDP packet and stash it
        self.bram = self.sock.recv(self.max_recv_bytes)

        
    def listen_forever(self):
        ''' main function '''
        while True:
            self.get_data()
            data = self.unpack_bram()
            self.pipe.send(data)
            #print 'sent', data[:4], '...'
        

class bram_analyzer():
    ''' the other half, this one continuously plots the data in the pipe '''
    
    def __init__(self, pipe_in):
        self.pipe = pipe_in # the output end of a multiprocessor pipe
        self.num_plot = 100 #number of points to plot in the timeseries window
        self.num_spec = int(2**13) #number of points to analyze for the fft window
        self.data = np.array( [0] ) #initialize data array
    
    def get_data(self):
        # pull data from pipe
        self.data = np.concatenate( (self.data, self.pipe.recv()) )
        # keep data list managable by trimming it
        self.data = self.data[-self.num_spec:]
        
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
        '''
        the main function, this should build and continuously update
        a live plot of the data being fed into the pipe
        '''
        # first collect enough data from the pipe to fill buffer
        while len(self.data) < self.num_spec:
            self.get_data()

        # now make a continuously-running plot of timeseries and the fft of data
        plt.ion()
        fig = plt.figure()
        
        time_ax = plt.subplot(2,1,1)
        to_plot = self.data[-self.num_plot*2:]
        line1, = time_ax.plot(to_plot[::2], c='b')
        line2, = time_ax.plot(to_plot[1::2], c='r')
        time_ax.set_xlabel('sample number')
        time_ax.set_ylabel('signal')

        fft_ax = plt.subplot(2,1,2)
        freq,powr = self.spectrum( self.data[1::2] + (0+1j)*self.data[::2] )
        line3, = fft_ax.semilogy( freq, powr, c='k')
        fft_ax.set_xlabel('Hz')
        fft_ax.set_ylabel('power')
        
        while True:
            # get new data
            self.get_data()
            to_plot = self.data[ -self.num_plot*2: ] # plot truncated signal arrays
            line1.set_ydata( to_plot[::2] )
            line2.set_ydata( to_plot[1::2] )
            # re-create and plot the FFT
            freq,powr = self.spectrum( self.data[1::2] + (0+1j)*self.data[::2] )
            line3.set_ydata( powr )
            # update the figure
            plt.draw()
        

if __name__ == '__main__':
    pipe_recv, pipe_send = mp.Pipe(False) # a 1-way pipe between processes
    listener = udp_interface_rx(pipe_send)
    plotter  = bram_analyzer(pipe_recv)
    p1 = mp.Process(target=listener.listen_forever)
    p2 = mp.Process(target=plotter.continuous_plot)
    p1.start()
    p2.start()

    
