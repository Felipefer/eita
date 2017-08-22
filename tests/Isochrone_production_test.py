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

# !!!! This test only works if the files are already download and in the right
# assigned path.

Z = 0.014
M = np.concatenate((np.arange( 0.80,  2.35, 0.05),
                    np.arange( 2.40,  6.60, 0.20),
                    np.arange( 7.00, 13.00, 1.00),
                    np.arange(14.00, 20.00, 2.00),
                    np.arange(20.00, 32.00, 4.00),
                    np.arange(30.00, 70.00, 5.00),
                    np.array((70, 80, 90, 95, 100, 120, 150))))

model = "PARSEC"
path = "/home/felipe/Evolutionary_Tracks/Original"

print "Loading Evolutionary Tracks from files."
t0 = time()
Set = EvTrack.EvTrack_MassSet(Z=Z, M=M, model=model, path=path)
print "Loading took {0} seconds.".format(time() - t0)

print Set.age_beg_phase
for i in range(Set.age_beg_phase.shape[1]):

    plt.plot(Set.age_beg_phase[:, i],
             Set.M)

plt.plot(np.array((0, 100)), np.array((1e9, 1e9)), '--k')
plt.show()

isochrone_masses = Set.get_isochrone_masses(t = 1e9)
print isochrone_masses