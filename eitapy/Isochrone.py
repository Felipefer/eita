__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "June 2018"

#\TODO expand this docstring
"""
Isochrone.py contains the functions used to work with isochrones
"""

import sys
sys.path.insert(0, '..')

import copy
import ev_track_columns as etcol
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from time import time
import config
import utils
import load
import os
import EvTrack

class Isochrone(object):
    # \TODO expand this docstring
    """

    """

    def __init__(self, age = None, Z = None, N = 5000, EvTrack_Set = None,
                 model='Not_Assigned', path=None, array=None, columns=None):


        if EvTrack_Set is not None:
            if array is None:
                array = EvTrack_Set.make_isochrone(age = age,
                                                   N = N,
                                                   isoc_columns=columns)
            else:
                raise Warning("In this setting, array will be produced "
                              "by the EvTrack_Set.make_isochrone")

        if model not in load.allowed_models:
            raise ValueError(("{0} is not a supported file format.\n"
                              "Supported formats are {0}."
                              "").format(load.allowed_models))


        # Load EvTrack according to the file format
        IsochroneData = None

        IsochroneData = load.LoadedIsochrone(age=age,
                                             Z=Z,
                                             model=model,
                                             path=path,
                                             array=array,
                                             columns=columns)

        # End of loading
        # Check if loading went fine
        if IsochroneData is None:
            raise utils.LoadingError("Could not load isochrone file")

        # Attributes
        self.age = age
        self.Z = Z
        self.Y = IsochroneData.Y

        self.model = model
        self.column_names = IsochroneData.column_names
        self.column_fmt = IsochroneData.column_fmt

        # Get number of columns
        self.Ncols = len(self.column_names)

        # Get number of lines
        self.Nlines = len(getattr(IsochroneData, self.column_names[0]))

        # \todo WARNING!!!
        # Here I'm going to use python's ability to reference two variables to
        # the same object. Data will be stored in self.array, and attributes
        # like self.age will point to a specific column of this array.
        #
        # This way, if you change self.array, self.name_of_the_column will also
        # change. But if you change self.name_of_the_column, only this attribute
        # will change, because you will be creating a new instance for that
        # attribute. Be careful!!!

        # Create data array:
        self.array = np.empty([self.Nlines, self.Ncols], dtype=float)
        self.array[:] = np.nan
        self.column_index = {}

        # Fill the array and point the attributes to it:
        for i in range(self.Ncols):
            column = self.column_names[i]

            self.column_index[column] = i
            self.array[:, i] = getattr(IsochroneData, column)
            setattr(self, column, self.array[:, i])
