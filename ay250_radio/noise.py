# guidelines
# should take beam size and wavelength as arguments
# should predict noise levels for observations of given bandwidth, time,
# number of antennae, etc.


import math

# constants in cgs
kb = 1.38e-16
jansky = 1.0e-23

class Telescope:
    '''

    numAnt: int
        Number of antennae. 
    '''
    def __init__(self):
        self.setBasic()
        self.setDependent()

    def setBasic(self):
        self.beamSize = 0
        self.sysTemp = 100  # K

        # dish properties: number of antenna, area of each dish, 
        # and the aperture efficiency 
        self.numAnt = 1
        self.areaDish = 1
        self.effAper = 1
        
    def setDependent(self):

        self.effArea = self.numAnt * self.areaDish * self.effAper

class ATA(Telescope):
    def __init__(self):

        Telescope.__init__()

class CARMA(Telescope):
    def __init__(self):

        Telescope.__init__()


def noise(telescope, bandwidth, intTime, wavelength):
    '''
    Purpose
    -------
    This provides the expected noise level in Jansky of a telescope,
    given the observing parameters and properties of the telescope. 

    Inputs
    ------
    telescope: class
        Specifications for a given telescope (beam size, number of antennae)
    bandwidth: float
        Bandwidth in Hz
    intTime: float
        Integration time in seconds

    wavelength: 

    Returns
    -------
    fluxDensityRMS: float
        The rms in the flux density, in units of Janskys 


    Notes
    -----
    Maybe supposed to develop more of the variables used here?

    Should incorporate in Telescope class.

    '''

    numSamp = bandwidth * intTime
    gain = (telescope.effArea / (2 * kb) ) * jansky

    # comment here
    rmsTemp = telescope.sysTemp / math.sqrt(numSamp)
    rmsFluxDensity = rmsTemp / gain

    return rmsFluxDensity


