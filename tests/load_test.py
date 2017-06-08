import sys
sys.path.insert(0, '../eitapy')

import load

__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
_parsec_tests_tracks_path = "./test_tracks_PARSEC"

"""
Tests if evolutionary tracks files are being correctly loaded
"""


def test_load_of_PARSEC_track():
    path = _parsec_tests_tracks_path
    mass = 0.950
    Z    = 0.014
    
    file_format = 'PARSEC'
    
    print "Parameters used for the test:"
    print "mass: {0} | Z: {1} | file_format: {2}\n".format(mass, Z, file_format)

    print "Setting up ev_track"
    ev_track = load.LoadedEvolutionaryTrack(mass = mass,
                                            Z = Z,
                                            file_format = file_format)
     
    print "Loading ev_track data from path = " + path
    ev_track.load(path)

    # Force raise of the warning "Already loaded"
    #print "Trying to load again to force Warning"
    #ev_track.load(path)
    
    print "returning "
    return ev_track

if __name__ == "__main__":
    print "Running test to load Parsec track"
    ev_track = test_load_of_PARSEC_track()
    print dir(ev_track)
    
    from matplotlib import pyplot as plt
    plt.plot(ev_track.log_Teff, ev_track.log_L)
    plt.gca().invert_xaxis()
    plt.show()