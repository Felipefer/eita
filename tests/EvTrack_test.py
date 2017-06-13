import sys
sys.path.insert(0, '../eitapy')

import load
import EvTrack
from time import time
from matplotlib import pyplot as plt

__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
_parsec_tests_tracks_path = "./test_tracks_PARSEC"

"""
Tests if EvTracks methods are working correctly
"""

def test_EvTrack_plot():
    path = _parsec_tests_tracks_path
    mass = 0.950
    Z = 0.014

    file_format = 'PARSEC'

    print "Parameters used for the test:"
    print "mass: {0} | Z: {1} | file_format: {2}\n".format(mass, Z, file_format)

    print "Initializing EvTrack"
    t0 = time()
    track = EvTrack.EvTrack(mass=mass, Z=Z,
                            path=path, file_format=file_format)
    print "Initializing took {0} seconds".format(time() - t0)

    print "Ploting EvTrack data"
    t0 = time()
    track.plot('log_Teff', 'log_L')
    print "Plotting took {0} seconds".format(time()-t0)

    plt.gca().invert_xaxis()
    plt.show()

if __name__ == "__main__":
    print "Running EvTrack.plot test"
    test_EvTrack_plot()