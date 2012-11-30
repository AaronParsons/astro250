import UVGrid
import numpy as np
import argparse

class UVGridGaussian(UVGrid.UVGrid):
    """
    @brief a subclass of UVGrid.UVGrid that implements Gaussian-weighting
    when gridding data samples onto the UV plane
    """
    
    def __init__(self, size, resolution, nearestPixels=4, wproj=True, wres=0.5):
        """
        @brief initialize the class
        
        @param size: the size of the UV grid in wavelengths (float)
        @param resolution: the resolution of the UV grid in wavelengths (float)
        @param nearestPixels: the number of nearby pixels to incorporate in weighting (int)
        @param wproj: whether to use w projection (bool)
        """
        
        # the nearest pixels to include when gridding
        self.nearestPixels = nearestPixels
        
        # the footprint size when doing gaussian gridding
        self.N_footprint = np.round(np.sqrt(self.nearestPixels))
        
        # whether to use w projection
        self.dowproj = wproj
        
        # save the w-projection resolution
        self.wres = wres
        
        # initialize the UVGrid super class
        UVGrid.UVGrid.__init__(self, size, resolution, wproj, wres)
        
        
    def gaussianGridder(self, i, j, i0, j0):
        """
        @brief return the gaussian weight of a pixel (i, j) based on its distance
        from the center pixel (i0, j0)
        
        @param i: pixel row indices (np.array or float)
        @param j: pixel column indices (np.array or float)
        @param i0: center pixel row index (float)
        @param j0: center pixel column index (float)
        """
        
        # standard deviation in pixels
        sigma = 1
        
        # this is the gaussian weight value
        w = 1./(np.sqrt(2.*np.pi)*sigma) * np.exp(- ( (i - i0)**2 + (j-j0)**2)/(2.*sigma**2))
       
        return w
        
        
    def distributePixels(self, i0, j0, samples, ws):
        """
        @brief find the nearest pixels to the center pixel (i0, j0)
        and return a list of pixels, with corresponding arrays of samples, 
        ws and i0, j0 (of correct size)
        """

        # initialize lists to return
        out_i, out_j = [], []
        out_i0, out_j0 = [], []
        out_data = []
        out_w = []
        
        # loop over each central pixel value and corresponding sample and w value
        for ix, jx, sample, w in zip(i0, j0, samples, ws):
            
            # compute the pixel values nearby
            row, col = np.indices([self.N_footprint, self.N_footprint])
            row = row - row[self.N_footprint/2, self.N_footprint/2] + ix
            col = col - col[self.N_footprint/2, self.N_footprint/2] + jx
        
            # create the lists to return
            out_i.extend(row.flatten())
            out_j.extend(col.flatten())
            out_data.extend([sample]*len(row.flatten()))
            out_i0.extend([ix]*len(row.flatten()))
            out_j0.extend([jx]*len(row.flatten()))
            out_w.extend([w]*len(row.flatten()))
            
        return (np.array(out_i), np.array(out_j)), (np.array(out_i0), np.array(out_j0)), np.array(out_data), np.array(out_w)
        
    def addSamples(self, (u, v, w), samples):
        """
        @brief add the samples with (u,v,w) coordinates to to the UV grid 
        """
        
        # phase out w component to zenith
        phase = np.exp(-2.*np.pi*1j*w)
        samples *= phase
        
        # get i0 and j0 in pixels for the (u,v) coordinates
        i0, j0 = UVGrid.UVGrid.getIndices(self, u, v)
        
        if self.dowproj:
        
            # distribute values over the nearest N pixels
            (i, j), (i0, j0), samples, w = self.distributePixels(i0, j0, samples, w)
        
            # compute the weights for these pixels
            weights = self.gaussianGridder(i, j, i0, j0)
            
            # add the weight values to the right pixels
            UVGrid.UVGrid.addWeightsToPixel(self, weights, i, j)            

            # add the weighted sample values to the right pixels
            UVGrid.UVGrid.wproj(self, w, i, j, samples*weights, wres=self.wres)
        else:
            
            # add unity weight values to the right pixels
            UVGrid.UVGrid.addWeightsToPixel(self, np.ones(len(i0)), i0, j0)            

            # add the weighted sample values to the right pixels
            UVGrid.UVGrid.addSamplesToPixel(self, samples, i0, j0)
            
            
        return
        
if __name__ == '__main__':


    # parse the input arguments
    parser = argparse.ArgumentParser(description="a UV Fourier grid to use in inteferometric observations, using gaussian gridding")
    parser.add_argument('file_name', type=str, help='the miriad UV data file name')
    parser.add_argument('--resolution', '-r', type=float, default=0.5, help="the resolution to use on the UV grid (in wavelengths)")
    parser.add_argument('--size', '-s', type=float, default=1000, help="the size of the UV grid (in wavelengths)")
    parser.add_argument('--nearest', '-n', type=int, default=4, help="how many nearby pixels to incorportate in gridding")
    parser.add_argument('--no_wproj', action='store_false', default=True, help='whether to do w projection or not')
    parser.add_argument('--wres', type=float, default=0.5, help='the resolution to bin the w array')
    
    args = parser.parse_args()

    # make the UV Interface object to read from input filename
    uvi = UVGrid.UVInterface(args.file_name)

    # make the UV Plane with a given width and resolution
    uvgrid = UVGridGaussian(args.size, args.resolution, args.nearest, wproj=args.no_wproj, wres=args.wres)

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