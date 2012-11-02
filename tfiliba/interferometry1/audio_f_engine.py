#!/opt/local/bin/python
import pyaudio as pa, numpy as np
import matplotlib.pyplot as plt
import socket
import time

NSAMPLES = 1024

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
antno = 34


p = pa.PyAudio()
stream = p.open(format=pa.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
d = stream.read(NSAMPLES)
d = np.frombuffer(d, dtype=np.int16)
d_spec = abs(np.fft.rfft(d))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


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
    d_spec128 = np.fft.rfft(d)
    d_spec64=np.array(d_spec128[0:512],dtype=np.complex64)
    #convert to complex64
    d_spec64.tostring()
    
    #generate header
    time.time
    header = np.array([antno, time.time()],dtype=np.uint32)
    
    #print header.tostring()+d_spec64.tostring()
    #print d_spec
    sock.sendto(header.tostring()+d_spec64.tostring(), (UDP_IP, UDP_PORT))
    
    