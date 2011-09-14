# guidelines
# should take beam size and wavelength as arguments
# should predict noise levels for observations of given bandwidth, time,
# number of antennae, etc.

class Telescope:
    def __init__(self):
        self.beamSize = 0
        self.numAnt = 1

class ATA(Telescope):
    def __init__(self):

        Telescope.__init__()

class CARMA(Telescope):
    def __init__(self):

        Telescope.__init__()


def noise(bandwidth, intTime, wavelength):
    '''
    Purpose
    -------

    Inputs
    ------
    bandwidth: flt
        Bandwidth in Hz
    intTime: flt
        Integration time in seconds
    beamSize:

    wavelength: 

    numAnt: int
        Number of antennae. 

    Notes
    -----

    '''

    numSamp = bandwidth * intTime

    return 0


