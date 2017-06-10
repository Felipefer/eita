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
Tests if evolutionary tracks files are being correctly loaded
"""

def test_load_of_PARSEC_track():
    path = _parsec_tests_tracks_path
    mass = 0.950
    Z    = 0.014
    
    file_format = 'PARSEC'
    
    print "Parameters used for the test:"
    print "mass: {0} | Z: {1} | file_format: {2}\n".format(mass, Z, file_format)

    print "Setting up and loading ev_track"
    ev_track = load.LoadedEvolutionaryTrack(mass = mass,
                                            Z = Z,
                                            path = path,
                                            file_format = file_format)
    
    return ev_track

if __name__ == "__main__":
    print "Running test to load Parsec track"
    
    t0 = time()
    ev_track = test_load_of_PARSEC_track()
    print "Loading took {0} seconds".format(time()-t0)
    
    print dir(ev_track)
    
    plt.plot(ev_track.log_Teff, ev_track.log_L)
    plt.gca().invert_xaxis()
    plt.show()

################################################################################
# Test initialization of EvTrack class

def test_init_EvTrack():
    path = _parsec_tests_tracks_path
    mass = 0.950
    Z = 0.014
    
    file_format = 'PARSEC'
    
    print "Parameters used for the test:"
    print "mass: {0} | Z: {1} | file_format: {2}\n".format(mass, Z, file_format)
    
    print "Initializing EvTrack"
    t0 = time()
    track = EvTrack.EvTrack(mass = mass, Z = Z,
                            path = path, file_format = file_format)
    print "Initializing took {0} seconds".format(time()-t0)

    return track
    

if __name__ == "__main__":
    print "Running test to initialize EvTrack (PARSEC)"
    
    t0 = time()
    track = test_init_EvTrack()
    print "Loading took {0} seconds".format(time() - t0)
    
    print dir(track)
    plt.plot(track.log_Teff, track.log_L)
    plt.gca().invert_xaxis()
    plt.show()
    
    
################################################################################
# Test EvTrack.simplify_array

def test_EvTrack_simplify_array():
    path = _parsec_tests_tracks_path
    mass = 0.950
    Z = 0.014
    
    file_format = 'PARSEC'
    
    print "Parameters used for the test:"
    print "mass: {0} | Z: {1} | file_format: {2}\n".format(mass, Z, file_format)
    
    print "Initializing EvTrack"
    t0 = time()
    track = EvTrack.EvTrack(mass = mass, Z = Z,
                            path = path, file_format = file_format)
    print "Initializing took {0} seconds".format(time() - t0)
    
    print "Getting simplified array"
    t0 = time()
    array = track.simplify_array(["age", "mass", "log_L", "log_Teff",
                                  "log_R", "phase"])
    print "Simplifying the array took {0} seconds".format(time()-t0)
    
    return array

if __name__ == "__main__":
    
    print "Running EvTrack.simplify_array test"

    array = test_EvTrack_simplify_array()
    
    plt.plot(array[:,3], array[:,2])
    plt.gca().invert_xaxis()
    plt.show()

