#!/opt/local/bin/python
import pyaudio as pa, numpy as np
import matplotlib.pyplot as plt

NSAMPLES = 1024


p = pa.PyAudio()
stream = p.open(format=pa.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
d = stream.read(NSAMPLES)
d = np.frombuffer(d, dtype=np.int16)
d_spec = abs(np.fft.rfft(d))

plt.ion()
audio_fig = plt.figure()
time_plot = audio_fig.add_subplot(121)
spec_plot = audio_fig.add_subplot(122)
#spec_plot.set_yscale('log')

timeline, = time_plot.plot(d)
specline, = spec_plot.plot(d_spec)


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
    
    timeline.set_ydata(d)
    #print d
    specline.set_ydata(d_spec)
    plt.draw()