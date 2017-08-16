import sys
sys.path.insert(0, '../eitapy')

import load
import EvTrack
import ev_track_columns as etcol
from time import time
from matplotlib import pyplot as plt
import numpy as np
import copy

__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
_parsec_tests_tracks_path = "./test_tracks_PARSEC"

"""
Tests if EvTracks methods are working correctly
"""

# Test EvTrack_MassSet init

# Initialize from files
def test_init_EvTrack_MassSet_from_files():
    Z = 0.017
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    print "Loading Evolutionary Tracks from files."
    t0 = time()
    Set = EvTrack.EvTrack_MassSet(Z = Z, M = M, model = model, path = path)
    print "Loading took {0} seconds.".format(time()-t0)

    plt.plot(Set.array[0, :, 3], Set.array[0, :, 2], 'b-', label = M[0])
    plt.plot(Set.array[1, :, 3], Set.array[1, :, 2], 'r-', label = M[1])
    plt.plot(Set.array[2, :, 3], Set.array[2, :, 2], 'g-', label = M[2])

    plt.gca().invert_xaxis()
    plt.legend()

    plt.show()

    print dir(Set)
    print Set.columns
    print Set.array

if __name__ == "__main__":
    run = raw_input("Run test_init_EvTrack_MassSet_from_files() (y, N): ")

    if run in ('Y', 'y'):
        test_init_EvTrack_MassSet_from_files()


# Initialize from a list of EvTracks
def test_init_EvTrack_MassSet_from_EvTrack_list():
    Z = 0.017
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    track0 = EvTrack.EvTrack(mass=M[0], Z=Z,
                             path=path, model=model)
    track1 = EvTrack.EvTrack(mass=M[1], Z=Z,
                             path=path, model=model)
    track2 = EvTrack.EvTrack(mass=M[2], Z=Z,
                             path=path, model=model)

    tracks = [track0, track1, track2]

    print "Loading Evolutionary Tracks from a list of EvTracks."
    t0 = time()
    Set = EvTrack.EvTrack_MassSet(EvTrack_list = tracks)
    print "Loading took {0} seconds.".format(time()-t0)

    plt.plot(Set.array[0, :, 3], Set.array[0, :, 2], 'b-', label=M[0])
    plt.plot(Set.array[1, :, 3], Set.array[1, :, 2], 'r-', label=M[1])
    plt.plot(Set.array[2, :, 3], Set.array[2, :, 2], 'g-', label=M[2])

    plt.gca().invert_xaxis()
    plt.legend()

    plt.show()

    print dir(Set)
    print Set.columns
    print Set.array

if __name__ == "__main__":
     run = raw_input(("Run test_init_EvTrack_MassSet_from_EvTrack_list() "
                      "(y, N): "))

     if run in ('Y', 'y'):
        test_init_EvTrack_MassSet_from_EvTrack_list()


# Initialize from an array
def test_init_EvTrack_MassSet_from_array():
    Z = 0.017
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model, path=path)

    array = Set.array
    columns = Set.columns

    print "Loading Evolutionary Tracks from an array."
    t0 = time()
    Set2 = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model,
                                   array=array, columns=columns)
    print "Loading took {0} seconds.".format(time()-t0)


    plt.plot(Set2.array[0, :, 3], Set2.array[0, :, 2], 'b-', label=M[0])
    plt.plot(Set2.array[1, :, 3], Set2.array[1, :, 2], 'r-', label=M[1])
    plt.plot(Set2.array[2, :, 3], Set2.array[2, :, 2], 'g-', label=M[2])

    plt.gca().invert_xaxis()
    plt.legend()

    plt.show()

    print dir(Set2)
    print Set2.columns
    print Set2.array

if __name__ == "__main__":
    run = raw_input(("Run test_init_EvTrack_MassSet_from_array() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_init_EvTrack_MassSet_from_array()


def test_EvTrack_MassSet_interp_mass():
    Z = 0.017
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model, path=path)

    M_new = [0.950, 0.975, 1.000, 1.025, 1.050]

    print "Interpolating new masses"
    t0 = time()
    Set.interp_mass(M_new)
    print "Interpolation took {0} seconds.".format(time()-t0)

    fmt = ['r-', 'b-', 'g-', 'm-', 'c-']
    for m in range(len(Set.M)):
        plt.plot(Set.array[m, :, 3], Set.array[m, :, 2], fmt[m],
                 label = M_new[m])

    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_MassSet_interp_mass() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_interp_mass()


def test_EvTrack_MassSet_getitem():
    Z = 0.017
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model, path=path)

    track0 = EvTrack.EvTrack(mass=M[0], Z=Z,
                             path=path, model=model)

    track1 = Set[0]

    track0.plot('log_Teff', 'log_L', ls = '-', c = 'red', zorder = 0,
                label = "Loaded individually")
    track1.plot('log_Teff', 'log_L', ls = '--', c = 'blue', zorder = 1,
                label = "get item by index")

    print "dir(Set): {}".format(dir(Set))
    print "Set.array: {}".format(Set.array)
    print "dir(track1): {}".format(dir(track1))
    print "track1.array: {}".format(track1.array)

    plt.legend()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_MassSet_getitem() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_getitem()

def test_EvTrack_MassSet_iter():
    Z = 0.017
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model, path=path)

    i = 0
    c = ['red', 'blue', 'green']

    # Tests the Set.__iter__ method:
    for track in Set:
        track.plot('log_Teff', 'log_L', c = c[i], label = track.M)
        i += 1

    plt.gca().invert_xaxis()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_MassSet_iter() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_iter()


def test_EvTrack_MassSet_plot():
    Z = 0.017
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model, path=path)

    Set.plot('log_Teff', 'log_L', c = 'red')

    plt.gca().invert_xaxis()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_MassSet_plot() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_plot()


def test_EvTrack_MassSet_plot_with_interp():
    Z = 0.017
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model, path=path)

    M_plot = [0.95, 0.96, 0.97, 0.98, 0.99, 1, 1.01, 1.02, 1.03, 1.04, 1.05]
    Set.plot('log_Teff', 'log_L', M = M_plot, c='red')

    plt.gca().invert_xaxis()
    plt.show()


if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_MassSet_plot_with_interp() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_plot_with_interp()