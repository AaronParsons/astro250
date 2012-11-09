import aipy
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

class UVPoint():
    def __init__(self,u,v,data,resolution):
        self.u = u/resolution
        self.v = v/resolution
        self.data = data

class UVGrid():
    
    def __init__(self,uvdatamat,resolution):
        x = 2*max(point.u for point in uvdatamat)
        y = 2*max(point.v for point in uvdatamat)
        self.delta = resolution
        self.uvdatamat = uvdatamat
        self.complexgrid = np.zeros([np.ceil(x/self.delta),np.ceil(y/self.delta)],dtype=uvdatamat[0].data.dtype)
        self.samplinggrid = np.zeros([np.ceil(x/self.delta),np.ceil(y/self.delta)])
    
            
    def griddata(self):
        #put data into the empty grid
        for i in range(self.uvdatamat.size):
            xcoord = np.floor((self.uvdatamat[i].u)/self.delta)
            ycoord = np.floor((self.uvdatamat[i].v)/self.delta)

            #take the average when a pixel is oversampled
            self.complexgrid[xcoord,ycoord] += self.uvdatamat[i].data
            self.complexgrid[-xcoord,-ycoord] += np.conjugate(self.uvdatamat[i].data)
            self.samplinggrid[xcoord,ycoord]+=1
            self.samplinggrid[-xcoord,-ycoord]+=1

    def weightedgriddata(self,weightingfunction):
        #put data into the empty grid
        for i in range(self.uvdatamat.size):
            centerxcoord = np.floor((self.uvdatamat[i].u)/self.delta)
            centerycoord = np.floor((self.uvdatamat[i].v)/self.delta)

            for xoffset in range(-1,2):
                for yoffset in range(-1,2):
                    currentxcoord = centerxcoord+xoffset
                    currentycoord = centerycoord+yoffset
                    #print self.uvdatamat[i].u, currentxcoord, self.uvdatamat[i].v, currentycoord
                    #weight = (1./2)*(2-abs(self.uvdatamat[i].u-currentxcoord)-abs(self.uvdatamat[i].v-currentycoord))
                    weight = weightingfunction(self.uvdatamat[i].u, self.uvdatamat[i].v, currentxcoord, currentycoord)
                    if weight<0:
                        continue
                    #take the average when a pixel is oversampled
                    self.complexgrid[currentxcoord,currentycoord] += weight*self.uvdatamat[i].data
                    self.complexgrid[-currentxcoord,-currentycoord] += weight*np.conjugate(self.uvdatamat[i].data)
                    self.samplinggrid[currentxcoord,currentycoord]+=weight
                    self.samplinggrid[-currentxcoord,-currentycoord]+=weight
                    
    def plotdirtybeam(self):
        dirtybeam = np.fft.ifftshift(np.fft.ifft2(self.samplinggrid))
        plt.imshow(abs(dirtybeam))
        plt.show()
    
    def plotuvplane(self):
        plt.imshow(abs(self.complexgrid))
        plt.show()
    
    def plotdirtyimage(self):
        #plot the image
        dirtyimage = np.fft.ifftshift(np.fft.ifft2(self.complexgrid))
        plt.imshow(abs(dirtyimage))
        plt.show()
        
    def plotdeconvolvedimage(self):
        dirtyimage = np.fft.ifftshift(np.fft.ifft2(self.complexgrid))
        dirtybeam = np.fft.ifftshift(np.fft.ifft2(self.samplinggrid))
        plt.imshow(abs(dirtyimage/dirtybeam))
        plt.show()
    