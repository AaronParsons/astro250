import aipy
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from uvgrid import *

def weightingfunction(sampleu,samplev,pixelu,pixelv):
    return (1./2)*(2-abs(sampleu-pixelu)-abs(samplev-pixelv))


uv = aipy.miriad.UV('sim.uv')

#wavelengths per pixel
resolution=1

uvdata = []
#grid = np.zeros([x/delta,y/delta])
for (uvw,t,bl),data,flags in uv.all(raw=True):
    for i in range(uv['nchan']):
        u = uvw[0]*(uv['sfreq']+i*uv['sdf'])
        v = uvw[1]*(uv['sfreq']+i*uv['sdf'])
        uvdata.append(UVPoint(u,v,data[i],resolution))

uvdatamat = np.array(uvdata)
mygrid = UVGrid(uvdatamat, resolution)
#mygrid.griddata()
mygrid.weightedgriddata(weightingfunction)
#mygrid.plotuvplane()
mygrid.plotdirtyimage()



        
        

        
    
    
