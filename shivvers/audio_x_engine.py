import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
from time import time
import struct, socket



class udp_interface_rx():
    '''
    an interface to the UDP connection, designed to be run parallel
    to the plotting class with the multiprocessing module.
    '''
    def __init__(self, pipe_out, port=12345):
        # set up the UDP connection
        self.port = port
        self.max_recv_bytes = 1028*10 # receive up to 10 packets
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind( ('0.0.0.0', port) )
        self.sock = sock
        self.data = None # the most recent data received
        self.pipe = pipe_out # the end of the pipe into which we feed data
        self.count = 0

    def get_data(self):
        # get a UDP packet and stash it
        s = self.sock.recv(self.max_recv_bytes)
        self.data = np.array(struct.unpack('>{}i'.format(1028), s))
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



class correlator():
    '''
    the correlator plots the correlation.
    '''

    def __init__(self, pipe_in):
        self.pipe = pipe_in # the output end of a multiprocessor pipe
        self.N_packs = 10 # number of most-recent packets to keep around

        self.ant1 = 11 # the antenna ids to plot
        self.ant2 = 11
        self.tstamps1 = [] # list of timestamps of most recent data from each of the telescopes
        self.tstamps2 = []
        self.data1 = [] # lists of data arrays corresponding to timestamps
        self.data2 = []

    def get_data(self):
        while self.pipe.poll():
            # pull data from pipe until it is empty; added bonus: doesn't hang if already empty!
            d = self.pipe.recv()
            if d[0] == self.ant1:
                self.tstamps1.append(d[1])
                self.data1.append(d[2:])
            if d[0] == self.ant2:
                self.tstamps2.append(d[1])
                self.data2.append(d[2:])
        # keep data lists managable by trimming them to most recent N samples
        #  if there's a time delay beyond that, increase N_packs above
        for lll in [self.tstamps1, self.tstamps2, self.data1, self.data2]:
            lll = lll[-self.N_packs:]
    
    def get_a_pair(self):
        '''
        find and return the most recent set of samples
        that match timestamps.
        '''
        self.get_data()
        for i,pack in enumerate(self.data1[::-1]):
            # going backwards, so use -(i+1) as the index
            ts1 = self.tstamps1[-(i+1)]
            if ts1 not in self.tstamps2:
                continue
            else:
                i2 = self.tstamps2.index(ts1)
                pack1 = pack
                pack2 = self.data2[i2]
                return pack1, pack2
        # if we can't find a co-aligned packet, return None
        return None
                

    def plot_forever(self):
        ''' main function '''
        # first, wait until we have some data
        while len(self.data1) < 5 or len(self.data2) < 5:
            self.get_data()

        # now, plot it!
        flag = True  # used to track first plot instantiation
        while True:
            if flag:
                flag = False
                # build the plot for the first time
                plt.ion()
                fig = plt.figure()
                ax1 = plt.subplot(1,1,1)
                # get the two aligned signals
                while True:
                    try:
                        pack1, pack2 = self.get_a_pair()
                        break
                    except:
                        print 'could not align packages! trying again!'
                
                # build the frequency array, assuming packages are of format:
                #   pack[:len/2] = real(rfft), pack[len/2:] = imag(rfft)
                n = len(pack1)/2-1
                freq = np.fft.fftfreq(2*n, 1./44100)[:n]
                # plot the real and imaginary parts of the visibility
                #  as a function of frequency for the most recent
                #  time-aligned packets
                fft1 = pack1[:len(pack1)/2] + 1j*pack1[len(pack1)/2:]
                fft2 = pack2[:len(pack2)/2] + 1j*pack2[len(pack2)/2:]
                vis = (fft1*fft2)[:-1]
                line1, = ax1.semilogy( freq, abs(np.real(vis)), c='b', label='real')
                line2, = ax1.semilogy( freq, abs(np.imag(vis)), c='g', label='imag')
                
                ax1.set_xlabel('Hz')
                ax1.set_ylabel('visibility')
                plt.legend(loc=1)
                plt.ax1is( [0, 25000, 1e0, 1e10] )
            else:
                # from here on out, only update the lines
                while True:
                    try:
                        pack1, pack2 = self.get_a_pair()
                        break
                    except:
                        print 'could not align packages! trying again!'
                fft1 = pack1[:len(pack1)/2] + 1j*pack1[len(pack1)/2:]
                fft2 = pack2[:len(pack2)/2] + 1j*pack2[len(pack2)/2:]
                vis = (fft1*fft2)[:-1]
                line1.set_ydata( abs(np.real(vis)) )
                line2.set_ydata( abs(np.imag(vis)) )
                
                # update the figure
                plt.draw()


if __name__ == '__main__':
    pipe_recv, pipe_send = mp.Pipe(False) # a 1-way pipe between processes
    listener = udp_interface_rx(pipe_send)
    correler  = correlator(pipe_recv)
    p1 = mp.Process(target=listener.listen_forever)
    p2 = mp.Process(target=correler.plot_forever)
    p1.start()
    p2.start()
    p2.join() # watch the output to make sure packets are coming through properly
