#!/opt/local/bin/python
import pyaudio as pa, numpy as np
import matplotlib.pyplot as plt

NSAMPLES = 1024


p = pa.PyAudio()
stream = p.open(format=pa.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
d = stream.read(NSAMPLES)
d = np.frombuffer(d, dtype=np.int16)
d_spec = abs(np.fft.rfft(d))



while True:
    try:
        d = stream.read(NSAMPLES)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        continue
        #pass
    else:
        print "got data"
        d = np.frombuffer(d, dtype=np.int16)
    d_spec = abs(np.fft.rfft(d))
    
    