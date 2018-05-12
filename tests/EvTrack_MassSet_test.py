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


def test_EvTrack_MassSet_array_age_beg_phase():
    Z = 0.017
    M = [0.950, 1.000, 1.050]

    model = "PARSEC"
    path = _parsec_tests_tracks_path

    Set = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model, path=path)

    print Set.age_beg_phase
    for i in range(Set.age_beg_phase.shape[1]):
        plt.plot(Set.age_beg_phase[:,i],
                 Set.M)

    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_MassSet_array_age_beg_phase() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_array_age_beg_phase()


def get_tracks_path():
    if socket.gethostname() == 'Bravos':
        if getpass.getuser() == 'felipe':
            path = '/home/felipe/Documents'
    elif socket.gethostname() == 'Valyria':
        if getpass.getuser() == 'felipe':
            path = '/home/felipe/Evolutionary_Tracks/Original'
    elif socket.gethostname() == 'winterfell':
        if getpass.getuser() == 'felipe':
            path = '/home/felipe/Evolutionary_Tracks/Original'

    return path


def load_default_EvTrack_MassSet():
    Z = 0.017
    M = [0.950, 1.000, 1.050]
    phase = EvTrack.default_interp_phase['PARSEC']
    model = "PARSEC"
    path = get_tracks_path()

    Set = EvTrack.EvTrack_MassSet(Z=Z,
                                  M=M,
                                  model=model,
                                  phase=phase,
                                  path=path)

    return Set


def test_EvTrack_MassSet_include_HB():
    path = get_tracks_path()

    print "Loading Ev_track Set"
    Set = load_default_EvTrack_MassSet()

    print "Ev_track Set loaded"
    Set.plot('log_Teff', 'log_L', c='red', label = 'Original')

    print "Running include_HB method"
    Set.include_HB(path = path)
    print "include_HB completed"

    Set.plot('log_Teff', 'log_L', c='blue', linestyle='--', label = 'HB added')

    plt.gca().invert_xaxis()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_MassSet_include_HB? "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_include_HB()


def test_EvTrack_MassSet_get_phase_completeness():
    path = get_tracks_path()

    print "Loading Ev_track Set"
    Set = load_default_EvTrack_MassSet()
    Set_completeness = Set.get_phase_completeness(plot = True,
                                                  color = 'blue',
                                                  zorder = 1,
                                                  alpha = 0.5,
                                                  markersize = 10,
                                                  label = "Without HB")

    print "Including HB"
    Set_with_HB = copy.deepcopy(Set)
    Set_with_HB.include_HB(path=path)
    Set_with_HB_completeness = Set_with_HB.get_phase_completeness(plot = True,
                                                            color = 'red',
                                                            zorder = 0,
                                                            markersize = 20,
                                                            label = "With HB")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_MassSet_get_phase_completeness? "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_get_phase_completeness()


def test_EvTrack_MassSet_load_large_Set():
    Z = 0.017
    phase = EvTrack.default_interp_phase['PARSEC']
    model = "PARSEC"
    path = get_tracks_path()
    M = EvTrack.utils.get_PARSEC_masses(Z = Z, path = path)

    # Loading Evolutionary tracks
    print "Loading Evolutionary Tracks"
    Set = EvTrack.EvTrack_MassSet(Z=Z,
                                  M=M,
                                  model=model,
                                  phase=phase,
                                  path=path)

    print "plotting Evolutionary Tracks"
    Set.plot("log_Teff", "log_L", color = 'blue', zorder = 1)

    # Include HB
    print "Including HB"
    Set_with_HB = copy.deepcopy(Set)
    Set_with_HB.include_HB(path = path)

    print "plotting Evolutionary Tracks with HB"
    Set_with_HB.plot("log_Teff", "log_L", color='red', zorder=0)
    plt.gca().invert_xaxis()
    plt.show()

    # Plot completeness
    Set.get_phase_completeness(plot = True,
                               color = 'blue',
                               zorder = 1,
                               markersize = 10)
    Set_with_HB.get_phase_completeness(plot = True,
                               color = 'red',
                               zorder = 0,
                               markersize = 20)
    plt.show()


if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_MassSet_load_large_Set? "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_load_large_Set()


def test_EvTrack_MassSet_compare_interpolation_times(plot_steps = False):
    Z = 0.017
    phase = EvTrack.default_interp_phase['PARSEC']
    model = "PARSEC"
    path = get_tracks_path()
    M = EvTrack.utils.get_PARSEC_masses(Z = Z, path = path)

    M_interp = [np.linspace(0.7, 2.0, 100),
                np.linspace(0.7, 2.0, 500),
                np.linspace(0.7, 2.0, 1000),
                np.linspace(0.7, 2.0, 5000)]

    N_masses = [100, 500, 1000, 5000]

    # Loading Evolutionary tracks
    print "Loading Evolutionary Tracks"
    Set = EvTrack.EvTrack_MassSet(Z=Z,
                                  M=M,
                                  model=model,
                                  phase=phase,
                                  path=path)

    #Set_with_HB = copy.deepcopy(Set)
    #Set_with_HB.include_HB(path=path)

    # Calculating interpolation times for the Set without HB
    interp_time_without_HB = []

    print "Calculating interpolation times without HB"
    for Mlist in M_interp:
        print "interpolating {N} masses".format(N = len(Mlist))

        # Make a copy of the Set
        Set_interp = copy.deepcopy(Set)

        # Interpolate
        t0 = time()
        Set_interp.interp_mass(Mlist)
        tf = time()

        # Save time
        interp_time_without_HB.append(tf-t0)

        if plot_steps:
            Set_interp.plot('log_Teff', 'log_L')
            plt.gca().invert_xaxis()
            plt.show()

    # Calculating interpolation times for the Set with HB previously added
    interp_time_with_HB_previously = []

    print "Calculating interpolation times for previously added HB"
    for Mlist in M_interp:
        print "interpolating {N} masses".format(N = len(Mlist))

        # Make a copy of the Set
        Set_interp = copy.deepcopy(Set)

        # Interpolate
        Set_interp.include_HB(path = path)
        t0 = time()
        Set_interp.interp_mass(Mlist)
        tf = time()

        # Save time
        interp_time_with_HB_previously.append(tf-t0)

        if plot_steps:
            Set_interp.plot('log_Teff', 'log_L')
            plt.gca().invert_xaxis()
            plt.show()

    print interp_time_with_HB_previously

    # Calculating interpolation times for the Set with HB
    interp_time_with_HB_before = []

    print "Calculating interpolation times adding HB before interpolation"
    for Mlist in M_interp:
        print "interpolating {N} masses".format(N = len(Mlist))

        # Make a copy of the Set
        Set_interp = copy.deepcopy(Set)

        # Interpolate
        t0 = time()
        Set_interp.include_HB(path = path)
        Set_interp.interp_mass(Mlist)
        tf = time()

        # Save time
        interp_time_with_HB_before.append(tf-t0)

        if plot_steps:
            Set_interp.plot('log_Teff', 'log_L')
            plt.gca().invert_xaxis()
            plt.show()

    print interp_time_with_HB_before

    # Calculating interpolation times for the Set with HB after
    interp_time_with_HB_after = []

    print "Calculating interpolation times adding HB after interpolation"
    for Mlist in M_interp:
        print "interpolating {N} masses".format(N = len(Mlist))

        # Make a copy of the Set
        Set_interp = copy.deepcopy(Set)

        # Interpolate
        t0 = time()
        Set_interp.interp_mass(Mlist)
        Set_interp.include_HB(path=path)
        tf = time()

        # Save time
        interp_time_with_HB_after.append(tf-t0)

        if plot_steps:
            Set_interp.plot('log_Teff', 'log_L')
            plt.gca().invert_xaxis()
            plt.show()

    print interp_time_with_HB_after

    # Plot results
    plt.plot(N_masses, interp_time_without_HB, color = 'red',
             label = "without HB")
    plt.plot(N_masses, interp_time_with_HB_previously, color = 'green',
             label = "with HB previously")
    plt.plot(N_masses, interp_time_with_HB_before, color = 'blue',
             label = "with HB before")
    plt.plot(N_masses, interp_time_with_HB_after, color = 'black',
             label = "with HB after")

    plt.legend()
    plt.show()

if __name__ == "__main__":
    run = raw_input(("Run test_EvTrack_compare_interpolation_times? "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_compare_interpolation_times()

#\todo write test_EvTrack_MassSet_interp_phase