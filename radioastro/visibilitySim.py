# Create some software for simulating a visibility. 
# That is, given two antennas (with x,y,z positions in equatorial coordinates) 
# and a source (with x,y,z also in equatorial coordinates), 
# compute the phase that you would measure as a function of frequency.

# AstroConstants must be in path
from AstroConstants import c


def twoAntennae(antennaOneCoords, antennaTwoCoords, sourceCoords, frequency):
    '''
    Purpose
    -------
    We want to simulate a visibility. As a starting point, we will do this
    for the simplest case where there are only two antennae. Given
    the positions of the antennae and source (all in equatorial
    coordinates), as well as the frequency, this will return the phase.



    '''

    # need to calculate the time delay

    # how to calculate baseline and unit vector for source
    baselineVector = [0., 0.]
    sourceUnitVector = [0., 0.]


    # time delay given by dot product of baseline vector and
    # the unit vector in direction of signal
    timeDelay = baselineVector * sourceUnitVector / c

