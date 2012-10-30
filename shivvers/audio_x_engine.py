import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
from time import time
import struct, socket



class udp_interface_rx():
    '''
    an interface to the UDP connection, designed to be run parallel
    to the plotting class with multiprocessing.
    '''
    def __init__(self, pipe_out, port=12345):
        # set up the UDP connection
        self.port = port
        self.max_recv_bytes = 1024+8 # receive at most one packet at a time
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind( ('0.0.0.0', port) )
        self.sock = sock
        self.data = None # the most recent binary bram data received
        self.pipe = pipe_out # the end of the pipe into which we feed data
        self.count = 0

    def get_data(self):
        # get a UDP packet and stash it
        self.data = np.frombuffer(self.sock.recv(self.max_recv_bytes), dtype='int16')
        self.count += 1

    def listen_forever(self):
        ''' main function '''
        t_start = t_prev = time()
        while True:
            self.get_data()
            self.pipe.send(self.data)
            t_now = time()
            if t_now-t_prev > 1.:
                print 'running for {} seconds'.format( int(t_now-t_start) )
                print '  received {} packets'.format(self.count)
                t_prev = t_now



class analyzer():
    ''' the other half, this one continuously plots the data in the pipe '''
    
    def __init__(self, pipe_in):
        self.pipe = pipe_in # the output end of a multiprocessor pipe
        self.num_spec = int(1e3) #number of points to analyze for the fft window
        self.data = np.array( [] ) #initialize data array
    
    def get_data(self):
        while self.pipe.poll():
            # pull data from pipe
            d = self.pipe.recv()[2:] #for now throw away timestamp and ID
            self.data = np.concatenate( (self.data, d) )
        # keep data list managable by trimming it
        self.data = self.data[-self.num_spec:]
        
    def spectrum(self, timeseries, tstep=1./44100 ):
        '''
        produce the fft power spectrum of a timeseries consistently sampled
        tstep seconds apart.
        '''
        Nyquist = len(timeseries)/2+1
        freq = np.fft.fftfreq(len(timeseries), tstep)[ :Nyquist-1 ]
        fts  = np.fft.rfft(timeseries)[:-1] #quick hack to throw away confounding point
        powr = abs(fts)**2
        return freq, powr
        
    def get_data_forever(self):
        while True:
            # pull data from pipe
            d = self.pipe.recv()[2:] #for now throw away timestamp and ID
            self.data = np.concatenate( (self.data, d) )
            # keep data list managable by trimming it
            self.data = self.data[-self.num_spec:]

    def plot_forever(self):
        ''' main function '''
        # first, pull data until we have enough to plot
        while len(self.data) < self.num_spec:
            self.get_data()
        
        # now, plot it!
        flag = True  # used to track first plot instantiation
        while True:
            if flag:
                flag = False
                plt.ion()
                fig = plt.figure()
                fft_ax = plt.subplot(1,1,1)
                freq,powr = self.spectrum( self.data )
                line, = fft_ax.semilogy( freq, powr, c='k')

                fft_ax.set_xlabel('Hz')
                fft_ax.set_ylabel('power')
                plt.axis( [0, 1e4, 1e0, 1e12] )
            else:
                self.get_data()
                freq,powr = self.spectrum( self.data )
                line.set_ydata( powr )
                # update the figure
                plt.draw()


if __name__ == '__main__':
    pipe_recv, pipe_send = mp.Pipe(False) # a 1-way pipe between processes
    listener = udp_interface_rx(pipe_send)
    plotter  = analyzer(pipe_recv)
    p1 = mp.Process(target=listener.listen_forever)
    p2 = mp.Process(target=plotter.plot_forever)
    p1.start()
    p2.start()
    p1.join()
