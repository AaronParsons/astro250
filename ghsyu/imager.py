import aipy
import numpy as n
import matplotlib.pyplot as plt

class ReadMiriad(object):
    def __init__(self, target = 'sim.uv'):   
        self.uv.rewind()
        idx = list(self.freqs).index(freq)
        for (uvw, t, bl), data, flags in self.uv.all(raw = True):
            if not n.all(uvw == 0): 
                data = data[idx]
        n.linspace(self.uv['sfreq'], self.uv['sdf']*self.uv['nchan']+self.uv['sfreq'], self.uv['nchan'], endpoint = False)

class UVGrid(object):
    def __init__(self, resolution, max_bl, uv, freqs):
        self.resolution = resolution
        self.uv = uv
        self.max_bl = max_bl
        self.freqs = freqs
        nx = ny = self.freqs[-1]*self.max_bl/resolution
        self.grid = n.zeros((nx, ny),dtype = n.complex)
        
    def nearest_idx(self, uvw, freq):
        u = n.round(uvw[0]*freq/self.resolution)
        v = n.round(uvw[1]*freq/self.resolution)
        return (u,v)
    
    def populate_grid(self, uvw, freq):
            u, v = self.nearest_idx(uvw, freq)
            self.grid[u,v]   += data
            self.grid[-u,-v] += n.conjugate(data)
    
    def find_dimg(self):
        self.dimg = n.fft.ifft2(self.grid)
        
    def show(self):
        plt.imshow(n.abs(self.grid))
        plt.show()
        plt.imshow(n.abs(n.fft.fftshift(self.dimg)))
        plt.show()
    
if __name__ =='__main__':
    uv = aipy.miriad.UV('sim.py')
    
    A = UVGrid(.5, uv)
    A.populate_grid(A.freqs[0])
    A.find_dimg()
    A.show()