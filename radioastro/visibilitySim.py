# Create some software for simulating a visibility. 
# That is, given two antennas (with x,y,z positions in equatorial coordinates) 
# and a source (with x,y,z also in equatorial coordinates), 
# compute the phase that you would measure as a function of frequency.

# AstroConstants must be in path
from AstroConstants import c, radEarth
from math import sqrt, pi

from scipy import array


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
        is hour angle, the second is declination. Should be in decimal format.
    antennaTwoCoords: 1d array
        Same format as antennaOneCoords, but for the second antenna.
    sourceCoords: 1d array
        Same format as antennaOneCoords, but for the source.

    Notes
    -----
    Works for test cases of zenith and horizon


    Tests
    -----
    For a source on the horizon, and a wavelength that is twice the separation of
    the dishes, the phase should be pi. 
    >>> from AstroConstants import meter, radEarth, c
    >>> separation = 1 * meter
    >>> wavelength = 2 * separation
    >>> angSep = separation / radEarth
    >>> print visibilitySim.twoAntennae([-angSep / 2., 0], [angSep / 2., 0], [pi, 0], c / wavelength)
    -3.14159265359


    '''

    # TODO: eventually want input in ra instead of ha?
    # TODO: eventaully want input in sexigesimal rather than decimal format?

    # allow lists as inputs, but convert to arrays
    # for simplicity, assume now that if one is a list, all are
    if type(antennaOneCoords).__name__ == 'list':
        antennaOneCoords = array(antennaOneCoords)
        antennaTwoCoords = array(antennaTwoCoords)
        sourceCoords = array(sourceCoords)

    # need to calculate the time delay
    baselineCoordVector = antennaOneCoords - antennaTwoCoords
    sourceUnitVector = sourceCoords / sqrt(sum(sourceCoords**2))

    # we have position in equatorial coordinates
    # this translates in to a physical distance along the surface of the Earth
    # for instance, a separation of pi radians in equatorial position
    # is a distance of pi * radEarth
    # this encodes the distance (in centimeters) and the direction

    # we want the shortest path, so interested in range -pi to pi
    # given array design, this is surely unnecessary
    if sqrt(sum(baselineCoordVector**2)) > pi:
        baselineCoordVector -= 2 * pi
    baselineVector = baselineCoordVector * radEarth

    
    # time delay given by dot product of baseline vector and
    # the unit vector in direction of signal
    timeDelay = sum(baselineVector * sourceUnitVector) / c
    phase = 2 * pi * timeDelay * frequency

    return phase

