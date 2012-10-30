

import matplotlib.pyplot as plt
import numpy as np
import struct, socket
from scipy.ndimage.filters import gaussian_filter1d
import multiprocessing as mp
import pyaudio as pa
import numexpr as ne


class audio_in():
    '''
    an interface to the UDP connection, designed to be run parallel
    to the plotting class with multiprocessing.
    '''
    def __init__(self):
        self.chunk = 1024
        self.FORMAT = pa.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pa.PyAudio()
        self.plot_num = 1000

    def spectrum(self, timeseries, tstep=1./44100 ):
        '''
        produce the fft power spectrum of a timeseries consistently sampled
        tstep seconds apart.

        options:
          ltrim: number of points to trim from the lower end of the spectrum
          htrim: ditto for high end, or 'Nyquist'
          smoothness: the sigma of a gaussian kernel with which to smooth the power spectrum
        '''
        Nyquist = len(timeseries)/2+1
        freq = np.fft.fftfreq(len(timeseries), tstep)[ :Nyquist-1 ]
        fts  = np.fft.rfft(timeseries)[:-1] #quick hack to throw away confounding point
        powr = abs(fts)**2
        return freq, powr

    def listen_forever(self):
        ''' main function '''
        data = np.array([])
        flag = True
        while True:
            stream = self.p.open(format = self.FORMAT,
                                    channels = self.CHANNELS,
                                        rate = self.RATE,
                                       input = True,
                           frames_per_buffer = self.chunk)
            d = np.frombuffer(stream.read(self.chunk), dtype='int16')
            stream.close()
            data = np.concatenate( (data, d) )

            if len(data) >= self.plot_num:
                data = data[-self.plot_num:]
                if flag:
                    flag = False
                    plt.ion()
                    fig = plt.figure()
                    fft_ax = plt.subplot(1,1,1)
                    freq,powr = self.spectrum( data )
                    line, = fft_ax.semilogy( freq, powr, c='k')
                    
                    fft_ax.set_xlabel('Hz')
                    fft_ax.set_ylabel('power')
                    plt.axis( [0, 1e4, 1e0, 1e12] )
                else:
                    freq,powr = self.spectrum( data )
                    line.set_ydata( powr )
                    # update the figure
                    plt.draw()

