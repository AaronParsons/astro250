#!/opt/local/bin/python

import socket
import numpy as np
import matplotlib.pyplot as plt

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

NCHANNELS = 512

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

plt.ion()
audio_fig = plt.figure()
spec_plot = audio_fig.add_subplot(111)

data, addr = sock.recvfrom(4104) # buffer size is 1024 bytes
#print "received message:", data
header = np.frombuffer(data[0:8],dtype=np.uint32)
d_spec = np.frombuffer(data[8:4104],dtype=np.complex64)
#d_spec = np.zeros(NCHANNELS)
specline, = spec_plot.plot(abs(d_spec))

while True:
    data, addr = sock.recvfrom(4104) # buffer size is 1024 bytes
    #print "received message:", data
    header = np.frombuffer(data[0:8],dtype=np.uint32)
    d_spec = np.frombuffer(data[8:4104],dtype=np.complex64)
    specline.set_ydata(abs(d_spec))
    plt.draw()