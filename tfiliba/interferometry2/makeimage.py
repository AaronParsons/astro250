import aipy
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal


#def griddata(data, x, y, delta):
#    grid = np.zeros([x/delta,y/delta])
#    for in data:
#        grid[] = data



uv = aipy.miriad.UV('sim.uv')
#print uv['nchan']
#print uv['sfreq']
#print uv['sdf']

freq = np.zeros([uv['nchan']])
#for i in range(uv['nchan']):
#    freq[i] = uv['sfreq'] + i*uv['sdf']

u = []
v = []
uvdata = []
#grid = np.zeros([x/delta,y/delta])
for (uvw,t,bl),data,flags in uv.all(raw=True):
    #uvw*uv['sfreq'] #change coordiate to wavelengths
    #print uvw
    u.append(uvw[0]*uv['sfreq'])
    v.append(uvw[1]*uv['sfreq'])
    uvdata.append(data[0])
    #print uvw[0],uvw[1]
    #for freq in range(uv['nchan']):   
    #    print uvw, t, bl, uv['pol'], data

umat = np.array(u)
vmat = np.array(v)
uvdatamat = np.array(uvdata)
#plt.plot(umat,vmat,'r+')
#plt.show()

#grid the data
#determine the size of the grid
x = umat.max()-umat.min()
y = vmat.max()-vmat.min()
#determine the resolution of the grid
delta = 1
#generate an empty grid
complexgrid = np.zeros([np.ceil(x/delta),np.ceil(y/delta)],dtype=uvdatamat.dtype)
numpoints = np.zeros([np.ceil(x/delta),np.ceil(y/delta)])

#put data into the empty grid
for i in range(uvdatamat.size):
    xcoord = np.floor((umat[i])/delta)
    ycoord = np.floor((vmat[i])/delta)
    if numpoints[xcoord,ycoord] == 0:
        complexgrid[xcoord,ycoord] = uvdatamat[i]
        complexgrid[-xcoord,-ycoord] = np.conjugate(uvdatamat[i])
    #take the average when a pixel is oversampled
    else:
        (complexgrid[xcoord,ycoord]*numpoints[xcoord,ycoord]+uvdatamat[i])/(numpoints[xcoord,ycoord]+1)
        (complexgrid[-xcoord,-ycoord]*numpoints[-xcoord,-ycoord]+np.conjugate(uvdatamat[i]))/(numpoints[-xcoord,-ycoord]+1)
    numpoints[xcoord,ycoord]+=1
    numpoints[-xcoord,-ycoord]+=1

#plot the uv plane
#plt.imshow(abs(complexgrid))

#plot the image
imagegrid = np.fft.ifftshift(np.fft.ifft2(complexgrid))
plt.imshow(abs(imagegrid))
plt.show()
        
        

        
    
    
