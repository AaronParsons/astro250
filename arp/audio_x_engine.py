#! /usr/bin/env python

import numpy as n, pylab as p
import optparse, sys, struct, socket, threading

def dB(d): return 10 * n.log10(n.abs(d)**2).clip(0,n.Inf)

def unpack(d):
    antnum,timestamp = struct.unpack('<II', d[:8])
    d = n.frombuffer(d[8:], dtype=n.complex64)
    return antnum, timestamp, d

o = optparse.OptionParser()
#o.add_option('-i', '--host', help='Destination IP address')
o.add_option('-p', '--port', type='int', default=8888, help='Destination port')
o.add_option('-z', '--size', type='int', default=8192, help='Max packet size.')
opts,args = o.parse_args(sys.argv[1:])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('',opts.port))
    
p.ion()
d = sock.recv(opts.size)
ant,t,d = unpack(d)
plt = {}
plt[0], = p.plot(dB(d), 'k')
plt[1], = p.plot(dB(d), 'b')
plt['c'], = p.plot(dB(d), 'r')
plt['d'], = p.plot(dB(d), 'g')
p.ylim(20,200)
#p.draw()
#
#while True:
#    try: d = stream.read(SIZE)
#    except IOError: continue
#    d = n.frombuffer(d, dtype=n.int16)
#    _d = 10*n.log10(n.abs(n.fft.rfft(w*d))**2)
#    plt.set_ydata(_d)
#    p.draw()

class RXThread(threading.Thread):
    def __init__(self, sock, size, maxsize=40):
        threading.Thread.__init__(self)
        self.pkts = []
        self.sock = sock
        self.size = size
        self.maxsize = maxsize
        self.go = False
    def run(self):
        self.go = True
        while self.go:
            d = sock.recv(self.size)
            self.pkts.insert(0, d)
            self.pkts = self.pkts[:self.maxsize]
    def quit(self):
        self.go = False
    def getall(self):
        pkts = self.pkts
        self.pkts = []
        return pkts
    
rx = RXThread(sock, opts.size)
rx.start()

import aipy as a
w = a.dsp.gen_window(d.size, window='blackman-harris')

try:
    while True:
        pairs = {}
        if len(rx.pkts) < 20: continue
        pkts = rx.getall()
        print len(pkts)
        gotpair = False
        for pkt in pkts:
            ant,t,d = unpack(pkt)
            print ant, t
            pairs[t] = pairs.get(t,[]) + [(ant,d)]
            if len(pairs[t]) == 2:
                gotpair = True
                break
        if gotpair:
            (a1,d1),(a2,d2) = pairs[t]
            if a1 > a2: a1,d1,a2,d2 = a2,d2,a1,d1
            corr = d1 * n.conj(d2)
            plt['c'].set_ydata(dB(corr))
            #plt['c'].set_ydata(100*n.angle(corr))
            plt['d'].set_ydata(dB(n.fft.ifft(w*corr)))
            #plt[a1].set_ydata(dB(d1))
            #plt[a2].set_ydata(dB(d2))
        else:
            plt[ant].set_ydata(dB(d))
        #d = sock.recv(opts.size)
        #pairs = {}
        #try: d = rx.pkts.pop()
        #except(IndexError): continue
        #ant,t,d = unpack(d)
        #print ant, t, d.size
        p.draw()
        #print 'Got one', d.size
except:
    rx.quit()
    rx.join()

