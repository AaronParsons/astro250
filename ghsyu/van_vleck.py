import struct
import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as p
import numpy as n

def plot_bram(target = 'data_bram', output = 'output.png'):
    with open(target,'r') as f:
        data = f.read()
    grouped = zip(*[iter(data)]*4)
    C_int   = (''.join(i) for i in grouped)
    ints    = [struct.unpack('>i', i)[0] for i in C_int]
    t = n.linspace(0, len(ints)/200, len(ints), False)
    p.plot(t, ints)
    p.xlabel(r't ($\mathrm{\mu}$s)')
    p.show()
    #p.savefig(output)

if __name__ == '__main__':
    plot_bram()