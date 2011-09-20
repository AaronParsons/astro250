# Create some software for simulating a visibility. 
# That is, given two antennas (with x,y,z positions in equatorial coordinates) 
# and a source (with x,y,z also in equatorial coordinates), 
# compute the phase that you would measure as a function of frequency.

# AstroConstants must be in path
from AstroConstants import c, radEarth
from math import sqrt


def twoAntennae(antennaOneCoords, antennaTwoCoords, sourceCoords, frequency):
    '''
    Purpose
    -------
    We want to simulate a visibility. As a starting point, we will do this
    for the simplest case where there are only two antennae. Given
    the positions of the antennae and source (all in equatorial
    coordinates), as well as the frequency, this will return the phase.

    Inputs
    ------
    antennaOneCoords: 1d array
        Two element array with the coordinates of the first antenna. 
        The units should be radians. The first element
        is ra, the second is dec. Should be in decimal format.
    antennaTwoCoords: 1d array
        Same format as antennaOneCoords, but for the second antenna.
    sourceCoords: 1d array
        Same format as antennaOneCoords, but for the source.


    '''

    # need to calculate the time delay
    baselineVector = antennaOneCoords - antennaTwoCoords
    sourceUnitVector = sourceCoords / sqrt(sum(sourceCoords**2))

    # we have position in equatorial coordinates
    # this translates in to a physical distance along the surface of the Earth


    # time delay given by dot product of baseline vector and
    # the unit vector in direction of signal
    timeDelay = baselineVector * sourceUnitVector / c

