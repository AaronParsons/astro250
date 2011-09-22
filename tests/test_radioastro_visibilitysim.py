import unittest
import sys

sys.path.append('..')

from radioastro import visibilitySim
from math import pi
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

if __name__ == '__main__':
    unittest.main()

        
