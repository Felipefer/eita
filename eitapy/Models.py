__version__ = "0.0.2"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "Jan 2020"


"""Defines the stellar models classes and its methods

The Model class, and inherited EvTrack and Isochrone classes, are the objects 
that contain the data of the stellar models and the methods to use that data 
for different scientific tasks.


"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Model(object):
    """
    A generic stellar model.

    This class consists mostly of a stellar model in the form of a data array,
    and contains the methods to load it while ensuring the integrity of the
    data.

    It also contains methods to work on the data for generic tasks, like
    interpolation, removal and addition of columns, unit conversions, etc.

    The data is internally stored in the form of a pandas db.
    """

    def __init__(self,
                 data = None,
                 model = None,
                 columns = None):
        """

        Starting Model from from existing pd dataframe

            Parameters
            ----------
            data : pd dataframe
                the data structured as a pd dataframe
            model    : str
                name of the stellar model this data comes from


        Starting Model from from array and ordered list of column names

            Parameters
            ----------
            data : np array
                the data structured as a np array
            model    : str
                name of the stellar model this data comes from
            columns  : list of strings
                list of strings ordered as the data columns

        """

        # Assign stellar model
        self.model = model

        # Load accordingly to input
        if isinstance(data, pd.DataFrame):
            self.data = data

        elif isinstance(data, np.array):
            self.data = pd.DataFrame(data, columns = columns)

        else:
            raise ValueError("Parameter 'data' must be a numpy.array or "
                             "a pandas.DataFrame")


    def plot(self, param1, param2):
        x = self.data[param1]
        y = self.data[param2]

        plt.plot(x, y)

def load_model(filepath, model = None, columns = None, **kwargs):

    if columns is None:
        data = pd.read_csv(filepath, **kwargs)
    else:
        data = pd.read_csv(filepath, usecols=columns, **kwargs)

    md = Model(data = data, model = model)

    return md


class EvTrack(Model):
    """
    An evolutionary track of a stellar model.

    Consists of a set of evolutionary steps obtained by some stellar model for
    a single star with a given initial mass and initial composition.

    For this data structure, each line of the dataframe represent a different
    time step on the evolution of the star.

    Equivalent evolutionary points (EEPs) are also implemented to allow the
    comparison and interpolation of models that show a similar physical
    evolution, but on vastly different timescales.
    """
    pass



class Isochrone(Model):
    """
    An Isochrone of a stellar model

    Is the set of parameters obtained for stars of the same age and composition,
    but with different initial masses.

    For this data structure, each line represent a star with a different initial
    stellar mass.

    Can be obtained by interpolating a set of Evolutionary Tracks.
    """


    pass



class Model_Set(object):
    """
    A generic set of stellar models.


    """
    pass



class EvTrack_Set(Model_Set):
    pass



class Isochrone_Set(Model_Set):
    pass

