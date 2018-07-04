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

# !!!! This test only works if the files are already download and in the right
# assigned path.

def test_EvTrack_MassSet_make_isochrone_without_adding_HB():
Z = 0.014
M = np.concatenate((np.arange( 0.80,  2.35, 0.05),
                    np.arange( 2.40,  6.60, 0.20),
                    np.arange( 7.00, 13.00, 1.00),
                    np.arange(14.00, 20.00, 2.00),
                    np.arange(20.00, 32.00, 4.00),
                    np.arange(30.00, 70.00, 5.00),
                    np.array((70, 80, 90, 95, 100, 120, 150))))

model = "PARSEC"

path = None
if socket.gethostname() == 'Bravos':
    if getpass.getuser() == 'felipe':
        path = '/home/felipe/Documents'
else:
    path = "/home/felipe/Evolutionary_Tracks/Original"

print "Loading Evolutionary Tracks from files."
t0 = time()
Set = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model, path=path)
print "Loading took {0} seconds.".format(time() - t0)

isoc_columns = ['age', 'mass', 'log_L', 'log_Teff', 'phase']
print "Starting make_isochrone method"
t0 = time()
isochrone = Set.make_isochrone(age = 1e9,
                               N = 1000,
                               isoc_columns = isoc_columns,
                               verbose=True)
print "Total time to build the isochrone was {}".format(time()-t0)
print isochrone

plt.plot(isochrone[:, 3], isochrone[:, 2])
plt.gca().invert_xaxis()
plt.show()

if __name__ == "__main__":
    run = raw_input(("test_EvTrack_MassSet_make_isochrone_without_HB() "
                     "(y, N): "))

    if run in ('Y', 'y'):
        test_EvTrack_MassSet_make_isochrone_without_adding_HB()
