import sys
sys.path.insert(0, '../eitapy')

import load
import EvTrack
import ev_track_columns as etcol
from time import time
from matplotlib import pyplot as plt
import numpy as np
import copy
import getpass
import socket

__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
_parsec_tests_tracks_path = "./test_tracks_PARSEC"

"""
Checks if EvTracks methods are working correctly
"""

# Initialize from a list of EvTracks
def test_init_EvTrack_ZSet_from_EvTrack_MassSet_list():
    Z = [0.01, 0.014, 0.017]
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set0 = EvTrack.EvTrack_MassSet(Z = Z[0], M = M,
                                   model = model, path = path)
    Set1 = EvTrack.EvTrack_MassSet(Z=Z[1], M=M,
                                   model=model, path=path)
    Set2 = EvTrack.EvTrack_MassSet(Z=Z[2], M=M,
                                   model=model, path=path)

    Sets = [Set0, Set1, Set2]

    print "Loading Evolutionary Tracks from a list of EvTracks."
    t0 = time()
    Set = EvTrack.EvTrack_ZSet(EvTrack_MassSet_list = Sets)
    print "Loading took {0} seconds.".format(time()-t0)

    for i in range(Set.array.shape[1]):
        plt.plot(Set.array[0, i, :, 3], Set.array[0, i, :, 2], 'b-')
        plt.plot(Set.array[1, i, :, 3], Set.array[1, i, :, 2], 'r-')
        plt.plot(Set.array[2, i, :, 3], Set.array[2, i, :, 2], 'g-')

    plt.gca().invert_xaxis()
    plt.show()

    print dir(Set)

if __name__ == "__main__":
    run = raw_input("Run test_init_EvTrack_ZSet_from_EvTrack_MassSet_list (y, N): ")

    if run in ('Y', 'y'):
        test_init_EvTrack_ZSet_from_EvTrack_MassSet_list()

def test_init_EvTrack_ZSet_from_files():
    Z = [0.01, 0.014, 0.017]
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    t0 = time()
    Set = EvTrack.EvTrack_ZSet(Z = Z, M = M, model = model, path = path)
    print "Loading took {0} seconds.".format(time()-t0)

    for i in range(Set.array.shape[1]):
        plt.plot(Set.array[0, i, :, 3], Set.array[0, i, :, 2], 'b-')
        plt.plot(Set.array[1, i, :, 3], Set.array[1, i, :, 2], 'r-')
        plt.plot(Set.array[2, i, :, 3], Set.array[2, i, :, 2], 'g-')

    plt.gca().invert_xaxis()
    plt.show()

    print dir(Set)

if __name__ == "__main__":
    run = raw_input("Run test_init_EvTrack_ZSet_from_files (y, N): ")

    if run in ('Y', 'y'):
        test_init_EvTrack_ZSet_from_files()


def test_init_EvTrack_ZSet_from_array():
    Z = [0.01, 0.014, 0.017]
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    # Use load from file to get the data
    Set_ref = EvTrack.EvTrack_ZSet(Z = Z, M = M, model = model, path = path)

    columns = Set_ref.columns
    array = Set_ref.array

    # Load from array
    t0 = time()
    Set = EvTrack.EvTrack_ZSet(Z = Z,
                               M = M,
                               model = model,
                               columns = columns,
                               array = array)
    print "Loading took {0} seconds.".format(time()-t0)

    for i in range(Set.array.shape[1]):
        plt.plot(Set.array[0, i, :, 3], Set.array[0, i, :, 2], 'b-')
        plt.plot(Set.array[1, i, :, 3], Set.array[1, i, :, 2], 'r-')
        plt.plot(Set.array[2, i, :, 3], Set.array[2, i, :, 2], 'g-')

    plt.gca().invert_xaxis()
    plt.show()

    print dir(Set)

if __name__ == "__main__":
    run = raw_input("Run test_init_EvTrack_ZSet_from_array (y, N): ")

    if run in ('Y', 'y'):
        test_init_EvTrack_ZSet_from_array()


def test_EvTrack_ZSet_getitem():
    Z = [0.01, 0.014, 0.017]
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    ZSet = EvTrack.EvTrack_ZSet(Z=Z, M=M, model=model, path=path)

    MSet = EvTrack.EvTrack_MassSet(M=M, Z=Z[0],
                                   path=path, model=model)

    ZSet0 = ZSet[0]

    MSet.plot('log_Teff', 'log_L', ls = '-', c = 'red', zorder = 0,
                label = "Loaded individually")
    ZSet0.plot('log_Teff', 'log_L', ls = '--', c = 'blue', zorder = 1,
                label = "get item by index")

    print "dir(ZSet): {}".format(dir(ZSet))
    print "ZSet.array: {}".format(ZSet.array)
    print "ZSet.array.shape: {}\n".format(ZSet.array.shape)

    print "dir(ZSet[0]): {}".format(dir(ZSet0))
    print "ZSet[0].array: {}".format(ZSet0.array)
    print "ZSet[0].array: {}\n".format(ZSet0.array.shape)

    print "dir(MSet loaded individually): {}".format(dir(MSet))
    print "MSet.array: {}".format(MSet.array)
    print "MSet.array.shape: {}\n".format(MSet.array.shape)

    plt.gca().invert_xaxis()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_ZSet_getitem() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_ZSet_getitem()


def test_EvTrack_ZSet_iter():
    Z = [0.01, 0.014, 0.017]
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    ZSet = EvTrack.EvTrack_ZSet(Z=Z, M=M, model=model, path=path)

    i = 0
    c = ['red', 'blue', 'green']

    # Tests the Set.__iter__ method:
    for track_set in ZSet:
        track_set.plot('log_Teff', 'log_L', c = c[i], label = track_set.Z)
        i += 1

    plt.gca().invert_xaxis()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_ZSet_iter() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_ZSet_iter()


def test_EvTrack_ZSet_interp_Z():
    Z = [0.01, 0.014, 0.017]
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_ZSet(Z=Z, M=M, model=model, path=path)

    Z_new = [0.01, 0.0125, 0.014, 0.0155, 0.017]

    print "Interpolating new masses"
    t0 = time()
    Set.interp_Z(Z_new)
    print "Interpolation took {0} seconds.".format(time()-t0)

    fmt = ['k-', 'r-', 'k-', 'g-', 'k-']
    zorder = [0, 1, 0, 1, 0]

    for z in range(len(Set.Z)):
        for m in range(len(Set.M)):
            plt.plot(Set.array[z, m, :, 3], Set.array[z, m, :, 2], fmt[z],
                     zorder = zorder[z])

    plt.gca().invert_xaxis()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_ZSet_interp_Z() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_ZSet_interp_Z()


def test_EvTrack_ZSet_interp_mass_and_phase():
    Z = [0.01, 0.014, 0.017]
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_ZSet(Z=Z, M=M, model=model, path=path)

    M_new = [0.950, 0.975, 1.000, 1.025, 1.050]

    print "Interpolating new masses"
    t0 = time()
    Set.interp_mass_and_phase(M_new)
    print "Interpolation took {0} seconds.".format(time()-t0)

    fmt = ['r-', 'g-', 'b-']

    for z in range(len(Set.Z)):
        for m in range(len(Set.M)):
            plt.plot(Set.array[z, m, :, 3], Set.array[z, m, :, 2], fmt[z])

    plt.gca().invert_xaxis()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_ZSet_interp_mass_and_phase() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_ZSet_interp_mass_and_phase()


def test_EvTrack_ZSet_interp():
    Z = [0.01, 0.014, 0.017]
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_ZSet(Z=Z, M=M, model=model, path=path)

    Z_new = [0.01, 0.0125, 0.014, 0.0155, 0.017]
    M_new = [0.950, 0.975, 1.000, 1.025, 1.050]

    print "Interpolating only Z"
    t0 = time()
    Set.interp(Z=Z_new)
    print "Interpolation took {0} seconds.".format(time()-t0)

    fmt = ['k-', 'r-', 'k-', 'g-', 'k-']

    for z in range(len(Set.Z)):
        for m in range(len(Set.M)):
            plt.plot(Set.array[z, m, :, 3], Set.array[z, m, :, 2], fmt[z])

    plt.gca().invert_xaxis()
    plt.show()

    # Reload
    Set = EvTrack.EvTrack_ZSet(Z=Z, M=M, model=model, path=path)

    print "Interpolating Z and M"
    t0 = time()
    Set.interp(Z=Z_new, M=M_new)
    print "Interpolation took {0} seconds.".format(time()-t0)

    fmt = ['k-', 'r-', 'k-', 'g-', 'k-']

    for z in range(len(Set.Z)):
        for m in range(len(Set.M)):
            plt.plot(Set.array[z, m, :, 3], Set.array[z, m, :, 2], fmt[z])

    plt.gca().invert_xaxis()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_ZSet_interp() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_ZSet_interp()


def test_EvTrack_ZSet_plot():
    Z = [0.01, 0.014, 0.017]
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    # Plot whole Set
    Set = EvTrack.EvTrack_ZSet(Z=Z, M=M, model=model, path=path)
    Set.plot('log_Teff', 'log_L', color = "#666666", alpha = 0.5)

    # Plot with interpolation
    Z_new = [0.012, 0.0152]
    M_new = [0.950, 0.975, 1.000, 1.025, 1.050]
    Set.plot('log_Teff', 'log_L', Z = Z_new, M = M_new,
             Zcolor = ['#FF0000', '#00FF00'])

    plt.gca().invert_xaxis()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_ZSet_plot() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_ZSet_plot()