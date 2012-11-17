import aipy
import numpy as np
import matplotlib.pyplot as plt
import argparse

class UVInterface(object):
    """
    @brief a class to act as an interface for MIRIAD files which store data samples
    at a given (u,v,w) baseline coordinate
    """
    
    def __init__(self, uvFile):
        """
        @brief initialize the class
        @param uvFile: the file name storing the UV data (str)
        """
        
        # initialize the miriad uv class
        self.uv = aipy.miriad.UV(uvFile)
        
        # create an array of the frequency channels we are using (in GHz)
        self.freqs = np.linspace(self.uv['sfreq'], self.uv['sfreq']+self.uv['nchan']*self.uv['sdf'], 
                                self.uv['nchan'], endpoint=False) # in GHz
        
    
    def reset(self):
        """
        @brief reset the miriad UV file to the beginning
        """
        
        self.uv.rewind()
        
        return
          
    def getBaselineLength(self, uvw):
        """
        @brief compute the baseline length given a (u,v,w) coordinate
        """
        u, v, w = uvw
        
        return np.sqrt((u**2 + v**2 + w**2))
        
    def getMaxBaseline(self):
        """
        @brief get the maximum baseline length in the input UV data file
        """
        
        # reset the input data file
        self.reset()
        
        # loop over all samples in the input file
        maxBaseline = 0
        for (uvw, t, bl), data, flags in self.uv.all(raw=True):
            u, v, w = uvw
            l = max((u**2 + v**2 + w**2) * self.freqs)
            if l > maxBaseline: maxBaseline = l
        
        # the maximum baseline in units of wavelengths
        self.maxBaseline =  np.sqrt(maxBaseline) 
        
        return self.maxBaseline
        
    def readSamples(self):
        """
        @brief read the samples from the input file
        @return (u, v, w): u, v, w are arrays of the coordinates
        @return samples: an array of the data samples corresponding to each coordinate
        """
        # reset the input data file
        self.reset()
        
        us, vs, ws  = [], [], []
        samples = []
        for ((u,v,w), t, bl), data, flags in self.uv.all(raw=True):
        
            # don't return samples that have zero baseline length
            if self.getBaselineLength((u,v,w)) == 0:
                continue
                
            # (u,v,w) are in nanoseconds initially, multipy by freqs in GHz to get wavelengths
            u = u*self.freqs
            v = v*self.freqs
            w = w*self.freqs
        
            # store the results we are returning
            samples.extend(data)
            us.extend(u)
            vs.extend(v)
            ws.extend(w)
        
        return (np.array(us), np.array(vs), np.array(ws)), np.array(samples)
        
class UVGrid(object):
    """
    @brief an object that implements a grid in UV Fourier space, to be used
    in interferometric observations
    """
    
    def __init__(self, size, resolution, wproj=True, wres=0.5):
        """
        @brief initialize the class
        
        @param size: the size of the UV grid in wavelengths (float)
        @param resolution: the resolution of the UV grid in wavelengths (float)
        @param wproj: whether to use w projection (bool)
        @param wres: the resolution to bin the w array (float)
        """
        
        dim             = int(size/resolution)
        self.shape      = (dim, dim) # save the shape of the UV grid we are using
        self.size       = size       # save the size of the plane in wavelengths
        self.resolution = resolution # resolution of the plane in wavelengths
        
        # initialize the UV grid and corresponding weights array
        self.uvplane = np.zeros(self.shape, dtype='complex64')
        self.weights = np.zeros(self.shape)
        
        # save whether we are doing w-projection or not
        self.dowproj = wproj
        
        # save the w-projection resolution
        self.wres = wres
        
        # compute the l and m sky values corresponding to the UV plane
        self.l, self.m = self.compute_lm()
    

    def compute_lm(self):
        """
        @brief compute the l and m sky values corresponding to the UV plane
        """
        
        # the dimension of the UV plane
        dim = self.shape[0]
        
        # make an indices array corresponding to the UV plane shape
        l, m = np.indices(self.shape)
        
        # make sure that the 2nd half of a given axis stores negative values
        l = np.where(l > dim/2, dim-l, -l)
        m = np.where(m > dim/2, m-dim, m)
        
        # convert pixel indices to l, m by dividing by the size of UV plane in wavelengths
        l, m = 1.*l/self.size, 1.*m/self.size
        
        # mask out where l**2 + m**2 > 1 since l, m are the sine of angles 
        mask = np.where(l**2 + m**2 >= 1, 1, 0)
        l = np.ma.array(l, mask=mask)
        m = np.ma.array(m, mask=mask)
        
        return l, m
        
    def showUV(self):
        """
        @brief plot and show the UV plane
        """
        # the dimension and resolution of the UV plane
        dim = self.shape[0] 
        res = self.resolution
        
        # plot and show the shifted UV plane (so center lies at Nx/2, Ny/2)
        plt.imshow(np.fft.fftshift(abs(self.uvplane)), extent=[-dim/2*res, dim/2*res, -dim/2*res, dim/2*res])
        plt.xlabel(r"$u$", fontsize=16)
        plt.ylabel(r"$v$", fontsize=16)
        plt.show()
        
        return
        
    def getIndices(self, u, v):
        """
        @brief get the pixel indices of the coordinates (u,v) in the 
        gridded UV plane by rounding to nearest pixel value
        
        @param u: u coordinates (float or np.array)
        @param v: v coordinates (float or np.array)
        """
        
        # i corresponds to row number, which is equal to v
        i = np.round(v/self.resolution)
        
        # j corresponds to column number, which is equal to u
        j = np.round(u/self.resolution)
        
        return (i.astype('int'), j.astype('int'))
        
    def addWeightsToPixel(self, weight, i, j):
        """
        @brief add the weight values at pixels (i,j) to the weight array
        
        @param weight: the weight values (float or np.array)
        @param i: pixel row values (float or np.array)
        @param j: pixel column values (float or np.array)
        """

        try:
            # add the weights to the pixels (i,j)
            self.weights[i, j] += weight
            
            # also add the weight to (-i, -j) since sky is real-valued
            self.weights[-1*i, -1*j] += weight
            
        except:
            raise ValueError("u/v coordinates larger than width of uv plane")
        
        return 
        
    def addSamplesToPixel(self, samples, i, j):
        """
        @brief add the sample values at pixels (i,j) to the weight array
        
        @param weight: the sample values (float or np.array)
        @param i: pixel row values (float or np.array)
        @param j: pixel column values (float or np.array)
        """
        
        try:

             # add the samples to pixels (i, j)
             self.uvplane[i, j] += samples  
             
             # add the conjugate of the samples to (-i, -j) since the sky is real-valued
             self.uvplane[-1*i, -1*j] += samples.conjugate()

        except:
            raise ValueError("u/v coordinates larger than width of uv plane")

        return
        
    def wproj(self, w, pixi, pixj, samples, wres=0.5):
        """
        @brief perform a w-projection in order to project all UV samples
        to the w=0 plane
        
        @param w: the w coordinate values (np.array)
        @param pixi: the row pixel values corresponding to w (np.array)
        @param pixj: the column pixel values corresponding to w (np.array)
        @param samples: the sample values corresponding to w (np.array)
        @param wres: the resolution in w to bin the w array by (float)
        """
        
        # sort all input arrays by w
        order = np.argsort(w)
        w = w[order]
        samples = samples[order]
        pixi = pixi[order]
        pixj = pixj[order]
        
        # loop over all w values and bin them
        locut = 0
        while True:
            
            # make a new uv plane for convolution purposes
            uvplane = np.zeros(self.shape, dtype='complex64')
           
            # get indices of all w values less than w[locut] + wres
            hicut = np.where(w <= w[locut]+wres)[0][-1]
            
            # make sure locut is not hicut, else continue on
            if hicut == locut:
                locut += 1
                continue
            
            # get the average w value in this bin
            avgw = np.average(w[locut:hicut])
            
            # store the samples for the samples that are in this w bin
            uvplane[pixi[locut:hicut], pixj[locut:hicut]] += samples[locut:hicut]  
            uvplane[-1*pixi[locut:hicut], -1*pixj[locut:hicut]] += samples.conjugate()[locut:hicut]
            
            # get the inverse w projection kernel
            invker = self.invWKernel(avgw)
            
            # convolve with the inverse kernel, add to the uv plane
            self.uvplane += np.fft.ifft2(np.fft.fft2(uvplane) * invker)
            
            # the loop breaking condition
            if hicut == len(w)-1: break
            locut = hicut
            
        return
      
    def invWKernel(self, w):
        """
        @brief the inverse w-projection kernel
        """
        return np.exp(-2.*np.pi*1j*w*(np.sqrt(1. - self.l**2 - self.m**2) - 1.)).filled(0.)
              
    def addSamples(self, (u, v, w), samples):
        """
        @brief add the samples with (u,v,w) coordinates to to the UV grid 
        """
        
        # phase out w component to zenith
        phase = np.exp(-2.*np.pi*1j*w)
        samples *= phase
        
        # get the nearest pixel indices on the grid for each (u,v)
        i, j = self.getIndices(u, v)
        
        # add unity weights to the given pixels
        self.addWeightsToPixel(np.ones(len(i)), i, j)
        
        # do w-projection, if specified
        if self.dowproj:
              
            # do w-projection and add samples
            self.wproj(w, i, j, samples, wres=self.wres)
        else: 
            # add the samples
            self.addSamplesToPixel(samples, i, j)
        
        return 
        
    def uvToSky(self, show=False):
        """
        @brief perform an inverse FFT of the UV plane and show the image
        """
        
        # do the inverse FFT
        ifft = np.fft.ifft2(self.uvplane)
        ifft = np.fft.fftshift(ifft)
        
        # show, if specified
        if show:
            
            dim = self.shape[0]
            plt.imshow(abs(ifft), extent=[-dim/2, dim/2, -dim/2, dim/2 ])
            plt.show()
            
        return ifft
        
        
if __name__ == '__main__':
    
    
    # parse the input arguments
    parser = argparse.ArgumentParser(description="a UV Fourier grid to use in inteferometric observations")
    parser.add_argument('file_name', type=str, help='the miriad UV data file name')
    parser.add_argument('--resolution', '-r', type=float, default=0.5, help="the resolution to use on the UV grid (in wavelengths)")
    parser.add_argument('--size', '-s', type=float, default=1000, help="the size of the UV grid (in wavelengths)")
    parser.add_argument('--no_wproj', action='store_false', default=True, help='whether to do w projection or not')
    parser.add_argument('--wres', type=float, default=0.5, help='the resolution to bin the w array')
    
    args = parser.parse_args()
    
    # make the UV Interface object to read from input filename
    uvi = UVInterface(args.file_name)
    
    # make the UV Plane with a given width and resolution
    uvgrid = UVGrid(args.size, args.resolution, wproj=args.no_wproj, wres=args.wres)
    
    # read the samples
    print "reading samples..."
    (u, v, w), data = uvi.readSamples()

    # add the samples 
    print "adding samples to UV grid..." 
    uvgrid.addSamples( (u, v, w), data)
    
    # show the uv plane
    uvgrid.showUV()
    
    # show the sky image from the UV plane
    print "taking inverse FFT..."
    ifft = uvgrid.uvToSky(show=True)
    
