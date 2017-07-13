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
################################################################################
# Test EvTrack.simplify_array


def _initialize_track_for_test(mass=0.950, Z=0.014,
                              path=_parsec_tests_tracks_path,
                              model='PARSEC'):


    print "Parameters used for the test:"
    print "mass: {0} | Z: {1} | model: {2}\n".format(mass, Z, model)

    print "Initializing EvTrack"
    t0 = time()
    track = EvTrack.EvTrack(mass=mass, Z=Z,
                            path=path, model=model)
    print "Initializing took {0} seconds".format(time() - t0)

    return track


def test_EvTrack_return_simplified_array():
    """
    Tests the Method EvTrack.return_simplified_array
    """

    track = _initialize_track_for_test()

    print "Getting simplified array"
    t0 = time()
    array = track.return_simplified_array(["age", "mass", "log_L", "log_Teff",
                                           "log_R", "phase"])
    print "Simplifying the array took {0} seconds".format(time()-t0)

    return array

if __name__ == "__main__":
    run = raw_input("Run EvTrack.return_simplified_array test? (y/N): ")

    if run in ('Y', 'y'):
        print "Running EvTrack.simplify_array test"

        array = test_EvTrack_return_simplified_array()

        plt.plot(array[:,3], array[:,2])
        plt.gca().invert_xaxis()
        plt.show()

def test_create_EvTrack_from_array():
    """
    Tests the Method LoadedEvolutionaryTrack._load_from_array
    """
    mass = 0.950
    Z = 0.014
    model = "PARSEC"
    path = _parsec_tests_tracks_path

    track = _initialize_track_for_test(mass=mass,
                                       Z=Z,
                                       path=path,
                                       model=model)

    print "Getting simplified array"
    t0 = time()
    columns = ["age", "mass", "log_L", "log_Teff", "log_R", "phase"]

    array = track.return_simplified_array(columns)
    print "Simplifying the array took {0} seconds\n".format(time() - t0)

    track_from_array = EvTrack.EvTrack(mass=mass, Z=Z, model="PARSEC",
                                       array = array, columns = columns)

    print "print: {0}".format(track_from_array)
    print "dir: {0}".format(dir(track_from_array))
    print "array: {0}".format(track_from_array.array)
    print "column_names: {0}".format(track_from_array.column_names)

    plt.plot(track_from_array.array[:, 3],
             track_from_array.array[:, 2])
    plt.gca().invert_xaxis()
    plt.show()

if __name__ == "__main__":
    run = raw_input("Run create_EvTrack_from_array test? (y/N): ")

    if run in ('Y', 'y'):
        print "Running LoadedEvolutionaryTrack._load_from_array test"
        test_create_EvTrack_from_array()


def test_EvTrack_plot():
    track = _initialize_track_for_test()

    print "Ploting EvTrack data"
    t0 = time()
    track.plot('log_Teff', 'log_L')
    print "Plotting took {0} seconds".format(time()-t0)

    plt.gca().invert_xaxis()
    plt.show()

if __name__ == "__main__":
    run = raw_input("Run EvTrack.plot test? (y/N): ")

    if run in ('Y', 'y'):
        print "Running EvTrack.plot test"
        test_EvTrack_plot()


def test_EvTrack_interpolate_phase(N = 10000):
    track = _initialize_track_for_test()

    print ("Interpolating EvTrack by phase - creating new EvTrack - "
           "(N = {0})").format(N)
    t0 = time()
    new_track = track.interp_phase(N = N)
    print ("Interpolating  - creating new EvTrack - "
           "took {0} seconds").format(time() - t0)

    print "\nold track shape: {0}".format(track.array.shape)
    print "new track shape: {0}".format(new_track.array.shape)

    print ("Interpolating EvTrack by phase - updating old EvTrack - "
           "(N = {0})").format(N)
    t0 = time()
    track.interp_phase(N=N, return_EvTrack = False)
    print ("Interpolating  - updating old EvTrack - "
           "took {0} seconds").format(time() - t0)

    print "\nupdated track shape: {0}".format(track.array.shape)

    return track

if __name__ == "__main__":
    run = raw_input("Run EvTrack.interp_phase test? (y/N): ")

    if run in ('Y', 'y'):
        print "Running EvTrack.interp_phase test"
        track = test_EvTrack_interpolate_phase(N=1000)
        print track.array.shape
        print len(track.log_Teff)
        track.plot('log_Teff', 'log_L', color = 'blue', zorder = 2)

        track = test_EvTrack_interpolate_phase(N=10000)
        track.plot('log_Teff', 'log_L', color = 'red', zorder = 1)

        track = test_EvTrack_interpolate_phase(N=100000)
        track.plot('log_Teff', 'log_L', color='black', zorder=0)

        plt.gca().invert_xaxis()
        plt.show()

def test_EvTrack_interpolate_phase_times():
    track = _initialize_track_for_test()
    N_cols_interpolated = track.array.shape[1]

    # Number of points to interpolate
    N = [100, 1000, 10000, 100000, 200000, 1000000, 2000000]

    # Perform linear interpolations
    t_linear = []

    for i in range(len(N)):
        new_track = copy.deepcopy(track)
        t0 = time()
        new_track.interp_phase(N = N[i], kind = 'linear')
        tf = time()

        t_linear.append(tf-t0)

    t_linear = np.array(t_linear) * 1e3 # converting to miliseconds
    # Plot results
    plt.plot(np.log10(N), np.log10(t_linear), 'ro')
    plt.gca().set_xlabel("log N")
    plt.gca().set_ylabel("log time (miliseconds)")
    plt.show()

if __name__ == '__main__':
    run = raw_input("Run EvTrack.interp_phase times test? (y/N): ")

    if run in ('Y', 'y'):
        print "Running EvTrack.interp_phase times test"
        test_EvTrack_interpolate_phase_times()


def test_EvTrack_simplify_array():
    track = _initialize_track_for_test()

    new_columns = ["age", "mass", "log_L", "log_Teff", "log_R", "phase"]

    print "\nTesting simplification creating a new EvTrack"

    print "Simplifying EvTrack"
    t0 = time()
    new_track = track.simplify_array(columns = new_columns,
                                     return_EvTrack = True)
    print ("Simplifying EvTrack creating a new EvTrack "
           "took {0} seconds").format(time()-t0)

    print 'Old track array shape is {0}'.format(track.array.shape)
    print 'Old track dir(): {0}'.format(dir(track))
    print 'Old track self.column_index: {0}'.format(track.column_index)
    print 'Old track self.column_fmt: {0}'.format(track.column_fmt)
    print 'Old track self.column_names: {0}'.format(track.column_names)

    print '\nNew track array shape is {0}'.format(new_track.array.shape)
    print 'New track dir(): {0}'.format(dir(new_track))
    print 'New track self.column_index: {0}'.format(new_track.column_index)
    print 'New track self.column_fmt: {0}'.format(new_track.column_fmt)
    print 'New track self.column_names: {0}'.format(new_track.column_names)

    track.plot('log_Teff', 'log_L', color = 'blue',
               linestyle = '--', zorder = 1)
    new_track.plot('log_Teff', 'log_L', color = 'red',
                   linestyle = '-', zorder = 0)

    plt.gca().invert_xaxis()
    plt.show()

    print "\nTesting simplification updating an old EvTrack"
    print "Simplifying EvTrack"
    t0 = time()
    track.simplify_array(columns=new_columns,
                         return_EvTrack = False)
    print ("Simplifying EvTrack updating an old EvTrack "
           "took {0} seconds").format(time() - t0)

    print track.array.shape
    print dir(track)

    return new_track

if __name__ == '__main__':
    run = raw_input("Run EvTrack.simplify_array test? (y/N): ")

    if run in ('Y', 'y'):
        print "Running EvTrack.simplify_array test"
        test_EvTrack_simplify_array()


def test_EvTrack_save():
    track = _initialize_track_for_test()

    # Default save
    print '\nSaving using default values'
    t0 = time()
    track.save()
    print 'Saving {0} shape array took {1} seconds'.format(track.array.shape,
                                                           time()-t0)

    # Simplified save in different folder
    new_columns = ["age", "mass", "log_L", "log_Teff", "log_R", "phase"]

    print '\nSaving in user defined folder and using less columns'
    t0 = time()
    track.save(filename = "simplified_track_save_test.dat",
               folder   = "./",
               columns  = new_columns)
    print 'Saving ({0}, {1}) array took {2} seconds'.format(track.Nlines,
                                                            len(new_columns),
                                                            time() - t0)

if __name__ == '__main__':
    run = raw_input("Run EvTrack.save test? (y/N): ")

    if run in ('Y', 'y'):
        test_EvTrack_save()


def test_EvTrack_interpolate_age():
    track = _initialize_track_for_test()

    track.plot('log_Teff', 'log_L', color='red',
               linestyle='-', zorder=0)

    # Interpolate track to obtain data for an age, all columns
    print "\nInterpolating track to obtain data for the given age."
    t0 = time()
    age_data0 = track.interpolate_age(age = 1e9)
    print "Interpolating the track took {0} seconds.\n".format(time()-t0)

    plt.plot(age_data0[3], age_data0[2], 'bo', label = '1e9')

    # Print interpolated column names and values
    print track.column_names
    print age_data0

    # Interpolate some more ages and also plot them
    ages = [2e9, 3e9, 4e9, 5e9, 6e9]
    fmts = ['go', 'ro', 'ko', 'co', 'yo']

    for fmt, age in zip(fmts, ages):
        age_data = track.interpolate_age(age = age)
        plt.plot(age_data[3], age_data[2], fmt, label="{:.1e}".format(age))

    plt.legend()
    plt.gca().invert_xaxis()
    plt.show()

if __name__ == '__main__':
    run = raw_input("Run EvTrack.interpolate_age test? (y/N): ")

    if run in ('Y', 'y'):
        test_EvTrack_interpolate_age()