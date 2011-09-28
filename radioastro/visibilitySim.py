# Create some software for simulating a visibility. 
# That is, given two antennas (with x,y,z positions in equatorial coordinates) 
# and a source (with x,y,z also in equatorial coordinates), 
# compute the phase that you would measure as a function of frequency.

# AstroConstants must be in path
from AstroConstants import c, radEarth
from math import sqrt, pi

from scipy import array, exp, zeros


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
    For a source on the horizon, and a wavelength that is twice 
    the separation of the dishes, the phase should be pi. 
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
    phase = exp(-2 * pi * timeDelay * frequency * 1j)

    return phase

def manyAntennae(antennaeCoords, sourceCoords, frequency):
    '''
    Purpose
    -------
    Generalize visibility simulation to allow for many antenna. 


    Inputs
    ------
    antennaCoords: 2d array
        Should have dimensions of ([# of antennae] x 3), where
        [# of antennae] can be any value
    sourceCoords: 2d array
        Should have dimensions of ([# of sources] x 3), where
        [# of sources] can be any value
        One source is fine, as long as the input is a 2d array
        of shape [1 x 3]
    frequency: 1d array
        Array of frequencies. These frequencies are assumed to be the
        same for all sources.


    Notes
    -----
    This is going to be seriously memory limited
    for 10 antennae, 1000 sources, and 1000 frequency channels, this
    is creating an array with 10**8 elements. Perhaps this
    approach is not viable?
    '''

    # will have N * (N - 1) / 2 delays, where N is [# of antennae]
    # if M is number of sources, each with a delay, there are then
    # M * N * (N - 1) / 2 total delays to be recorded
    # Delay is a function of frequency, so each frequency channel has
    # its own delay

    # the phases can be stored in a 4D array 
    #
    # for a single source and a single frequency, the phases at 
    # each element will be stored in a 2d array, arranged as follows:
    #           ant_1    ant_2    ....  ....    ant_n
    # ant_1 [[      0     x_12    ....  ....     x_1n  ]
    # ant_2  [  x_12*        0    ....  ....     x_2n  ]
    #     .  [                                         ]
    #     .  [                                         ]
    # ant_n  [  x_1n*    x_2n*    ....  ....        0  ]]

    # NOTE: for N antennae, N^2 - (N * (N + 1) / 2) values are
    #       unneeded, as there are N zeroes, and (N * (N - 1) / 2) 
    #       complex conjugates

    # for each source and frequency, there will be an array ordered
    # in this way, leading to a total of 4d
    
    
    # want first dimension to be coordinates 
    # for antennaeCoords and sourceCoords
    numDimensions = 3
    assert antennaeCoords.shape[1] == numDimensions, \
            'Antennae coordinates should have dimensions ([# of antennae] x 3)'
    assert sourceCoords.shape[1] == numDimensions, \
            'Source coordinates should have dimensions ([# of sources] x 3)'

    # if this passes, assume the second dimension is # of antenna, # of sources
    # NOTE: for the case of 3 antennae, this test is useless

    numAntennae = antennaeCoords.shape[0]
    numSources = sourceCoords.shape[0]
    numChannels = len(frequency)

    phases = zeros([numSources, numAntennae, numAntennae, numChannels], 
            dtype = 'complex')
    
    # will be able to cut down on this by at least that factor of redundant
    # and zero value indices
    for i in xrange(numSources):
        for j in xrange(numAntennae):
            for k in xrange(numAntennae):
                phases[i, j, k, :] = twoAntennae(
                        antennaeCoords[j, :],
                        antennaeCoords[k, :],
                        sourceCoords[i, :],
                        frequency)

    return phases



