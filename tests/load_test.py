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
_parsec_tests_isocs_path = "./test_isocs_PARSEC"

"""
Tests if evolutionary tracks files are being correctly loaded
"""

def test_load_of_PARSEC_track():
    path = _parsec_tests_tracks_path
    mass = 0.950
    Z    = 0.014
    
    model = 'PARSEC'
    
    print "Parameters used for the test:"
    print "mass: {0} | Z: {1} | model: {2}\n".format(mass, Z, model)

    print "Setting up and loading ev_track"
    ev_track = load.LoadedEvolutionaryTrack(mass = mass,
                                            Z = Z,
                                            path = path,
                                            model = model)
    
    return ev_track

if __name__ == "__main__":
    run = raw_input(("Run test to load Parsec track? "
                     "(y, N): "))

    if run in ('Y', 'y'):
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
    
    model = 'PARSEC'
    
    print "Parameters used for the test:"
    print "mass: {0} | Z: {1} | model: {2}\n".format(mass, Z, model)
    
    print "Initializing EvTrack"
    t0 = time()
    track = EvTrack.EvTrack(mass = mass, Z = Z,
                            path = path, model = model)
    print "Initializing took {0} seconds".format(time()-t0)

    return track
    

if __name__ == "__main__":
    run = raw_input(("Run test to initialize EvTrack (PARSEC)? "
                     "(y, N): "))

    if run in ('Y', 'y'):
        t0 = time()
        track = test_init_EvTrack()
        print "Loading took {0} seconds".format(time() - t0)

        print dir(track)
        plt.plot(track.log_Teff, track.log_L)
        plt.gca().invert_xaxis()
        plt.show()

################################################################################
# Test initialization of an Isochrone

def load_of_PARSEC_Isochrone():
    path = _parsec_tests_isocs_path
    age = 1e9
    Z = 0.0152

    model = 'PARSEC_ISOC_1_2'

    print "Parameters used for the test:"
    print "age: {0} | Z: {1} | model: {2}\n".format(age, Z, model)

    print "Setting up and loading ev_track"
    isoc = load.LoadedIsochrone(age=age,
                                Z=Z,
                                path=path,
                                model=model)

    return isoc


if __name__ == "__main__":
    run = raw_input(("Run test to load Isochrone? "
                     "(y, N): "))

    if run in ('Y', 'y'):
        t0 = time()
        isoc = load_of_PARSEC_Isochrone()
        print "Loading took {0} seconds".format(time() - t0)

        print dir(isoc)

        plt.plot(isoc.log_Teff, isoc.log_L)
        plt.gca().invert_xaxis()
        plt.show()


def test_init_Isochrone():
    path = _parsec_tests_isocs_path
    age = 1e9
    Z = 0.0152

    model = 'PARSEC_ISOC_1_2'

    print "Parameters used for the test:"
    print "age: {0} | Z: {1} | model: {2}\n".format(age, Z, model)

    print "Initializing EvTrack"
    t0 = time()
    track = EvTrack.Isochrone(age=age, Z=Z,
                            path=path, model=model)
    print "Initializing took {0} seconds".format(time() - t0)

    return track


if __name__ == "__main__":
    run = raw_input(("Run test to initialize Isochrone (PARSEC_ISOC_1_2)? "
                     "(y, N): "))

    if run in ('Y', 'y'):
        t0 = time()
        track = test_init_Isochrone()
        print "Loading took {0} seconds".format(time() - t0)

        print dir(track)
        plt.plot(track.log_Teff, track.log_L)
        plt.gca().invert_xaxis()
        plt.show()