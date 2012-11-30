#! /usr/bin/env python

import pyaudio, numpy as n, time
import optparse, sys, struct, socket

o = optparse.OptionParser()
o.add_option('-i', '--host', help='Destination IP address')
o.add_option('-p', '--port', type='int', default=8888, help='Destination port')
o.add_option('-z', '--size', type='int', default=1024, help='Samples per packet')
o.add_option('-a', '--antnum', type='int', default=1, help='Antenna #')
opts,args = o.parse_args(sys.argv[1:])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.connect((opts.host,opts.port))
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100,
    input=True, frames_per_buffer=1024)

while True:
    try: d = stream.read(opts.size)
    except IOError: continue
    d = n.frombuffer(d, dtype=n.int16)
    _d = n.fft.rfft(d)[:-1].astype(n.complex64) # drop last ch
    t = int(n.round(time.time() / (opts.size / 44100.)))
    pkt = struct.pack('<II', opts.antnum, t) + _d.tostring()
    sock.sendto(pkt, (opts.host,opts.port))
    print 'Packet sent:', t

