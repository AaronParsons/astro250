import numpy as n
import threading
import socket
import Queue
import struct
import matplotlib.pyplot as plt

class Recv(threading.Thread):
    def __init__(self, port, q, **kwargs):
        self.port = port
        self.q = q
        super(Recv, self).__init__(**kwargs)
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', self.port))
        self.q.put(sock.recv(514*8))
        
class Plotter(threading.Thread):
    def __init__(self, q, **kwargs):
        self.q = q
        super(Plotter, self).__init__(**kwargs)
    def run(self):
        plt.ion()
        d = self.q.get()
        plt.plot(d)
        while True:
            d = self.q.get()
            plt.draw()
            
class Xeng(object):
    def __init__(self):
        self.queue1 = Queue.Queue()
        self.queue2 = Queue.Queue()
        self.port1 = 8888
        self.port2 = 8889
        self.plotqueue = Queue.Queue()
        self.plotter = Plotter(self.plotqueue)
    def parse_packet(self, queue):
        packet = queue.get()
        ant  = struct.unpack('<I',packet[:4])
        time = struct.unpack('<I',packet[4:8])
        data = n.frombuffer(packet[8:], dtype = n.complex64)
        return (ant, time, data)
    def xcorr(self):
        ant1, time1, data1 = self.parse_packet(self.queue1)
        ant2, time2, data2 = self.parse_packet(self.queue2)
        while True:
            if time1 == time2:
                self.plotqueue.put(data1 * data2)
                ant1, time1, data1 = self.parse_packet(self.queue1)
                ant2, time2, data2 = self.parse_packet(self.queue2)
            elif time1 > time2:
                ant2, time2, data2 = self.parse_packet(self.queue2)
            elif time1 <= time2:
                ant1, time1, data1 = self.parse_packet(self.queue1)

    def start(self):
        ant1 = Recv(self.port1, self.queue1)
        ant2 = Recv(self.port2, self.queue2)
        ant1.start()
        ant2.start()
        self.xcorr()
        self.plotter.start()
        
if __name__ == '__main__':
    A = Xeng()
    A.start()