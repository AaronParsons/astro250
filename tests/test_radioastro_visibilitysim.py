import unittest
import sys

sys.path.append('..')

from radioastro import visibilitySim
from math import pi
from scipy import zeros
import AstroConstants as AC


class TestVisibilitySim(unittest.TestCase):
    '''
    '''

    def testHorizonPhase(self):

        separation = 1 * AC.meter
        wavelength = 2 * separation
        angSep = separation / AC.radEarth
        phase = visibilitySim.twoAntennae([-angSep / 2., 0], \
                [angSep / 2., 0], [pi, 0], AC.c / wavelength)

        self.assertAlmostEqual(abs(phase + 1), 0, 1)

    def testHorizonPhaseManyAntennae(self):

        separation = 1 * AC.meter
        wavelength = 2 * separation
        angSep = separation / AC.radEarth

        numFreq = 10
        frequency = zeros(numFreq)
        frequency[:] = AC.c / wavelength

        antennaeCoords = array([
            [0, 0, 0],
            [0, 1, 0],
            [1, 0, 0],
            [1, 1, 0]])
        numAntennae = antennaeCoords.shape[0]

        sourceCoords = array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]])
        numSources = sourceCoords.shape[0]

        for i in xrange(numAntennae):
            pass


if __name__ == '__main__':
    unittest.main()

        
