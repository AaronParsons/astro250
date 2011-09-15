#log# Automatic Logger file. *** THIS MUST BE THE FIRST LINE ***
#log# DO NOT CHANGE THIS LINE OR THE TWO BELOW
#log# opts = Struct({'__allownew': True, 'logfile': 'ipython_log.py', 'pylab': 1})
#log# args = []
#log# It is safe to make manual edits below here.
#log#-----------------------------------------------------------------------
import noise
t = noise.Telescope()
reload(noise)
t = noise.Telescope()
noise.noise(t, 1e7, 1e5)
noise.noise(t, 1e7, 1e5, 0)
reload(noise)
t = noise.Telescope()
noise.noise(t, 1e7, 1e5, 0)
reload(noise)
t = noise.Telescope()
noise.noise(t, 1e7, 1e5, 0)
