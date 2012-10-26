import matplotlib.pyplot as plt
import pyaudio as pa
import numpy as n
import time

NSAMPLES = 1024

plt.ion()
def read_samp(stream):
    d = stream.read(NSAMPLES)
    d = n.frombuffer(d, dtype = n.int16)
    return n.abs(n.fft.fft(d))

p = pa.PyAudio()
stream = p.open(format=pa.paInt16, channels=1,
                rate = 44100, input=True, frames_per_buffer=1024)
out = plt.semilogy(read_samp(stream))

while True:
    out[0].set_ydata(read_samp(stream))
    plt.draw()