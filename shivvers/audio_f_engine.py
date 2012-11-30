'''
Real-time sender of audio data.
'''


import numpy as np
import socket, struct
import pyaudio as pa
from time import time

class audio_in_and_out():
    '''
    an interface to the UDP connection, this program pulls
    audio data from the mic and sends it to the UDP socket.
    
    packet format:
     4 bytes: antenna ID (uint)
     4 bytes: timestamp (uint)
     rest: FFT(data)
    
    '''
    def __init__(self, port=12345, host='127.0.0.1'):
        # set up the UDP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect( (host, port) )
        self.sock = sock
        
        # set up the audio input
        self.chunk = 1024
        self.FORMAT = pa.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pa.PyAudio()
        self.count = 0
        
        # define ID for later correlations
        self.ID = 11

    def listen_forever(self):
        ''' main function '''
        t_start = t_prev = time()
        while True:
            stream = self.p.open(format = self.FORMAT,
                                    channels = self.CHANNELS,
                                        rate = self.RATE,
                                       input = True,
                           frames_per_buffer = self.chunk)
            d = np.frombuffer(stream.read(self.chunk), dtype='int16')
            stream.close()
            time_int = int(time()%100 * 100) # send timestamp in 1/100's of a second
            d_fft = np.fft.rfft(d)
            to_send = np.hstack( (self.ID, time_int, np.real(d_fft), np.imag(d_fft)) )
            # build the byte string to send:
            s = struct.pack('>{}i'.format(1028), *to_send)
            self.sock.send(s)
            self.count +=1

            t_now = time()
            if t_now-t_prev > 1.:
                print 'running for {} seconds'.format( int(t_now-t_start) )
                print '  sent {} packets'.format(self.count)
                t_prev = t_now

if __name__ == '__main__':
    listener = audio_in_and_out()
    listener.listen_forever()
    
