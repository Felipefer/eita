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
from scipy.interpolate import interp1d
from time import time

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
                 param_list = [],
                 pred_list = [],
                 obs_list = []):
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
        self.obs_list = obs_list
        self.param_list = param_list
        self.pred_list = pred_list

        self.columns = self.obs_list + self.param_list + self.pred_list

        # Load accordingly to input
        if isinstance(data, pd.DataFrame):
            self.data = data

        elif isinstance(data, np.array):
            self.data = pd.DataFrame(data, columns = self.columns)

        else:
            raise ValueError("Parameter 'data' must be a numpy.array or "
                             "a pandas.DataFrame")


    def plot(self, param1, param2):
        x = self.data[param1]
        y = self.data[param2]

        plt.plot(x, y)

    def __add__(self, other_model):
        self.data = pd.concat([self.data, other_model.data])
        return self

    def interp_mass(self, tcol = 'logAge', Zcol = 'MH', mcol = 'Mini',
                    Ninterp = 2000, v = True):

        # if verbose
        if v:
            print 'Starting interpolation of {} models'.format(self.model)
            old_shape = self.data.shape
            t0 = time()

        # Create the empty dataframe
        columns = list(self.data.columns)
        new_data = pd.DataFrame(columns=columns, dtype = float)

        # Get list of t_i
        t_list = list(set(self.data.loc[:,tcol]))
        t_list.sort()

        # Loop over each t_i
        for ti in t_list:
            # Get list of Z_ij
            cond_i = self.data.loc[:,tcol].values == ti

            Z_list = list(set(self.data.loc[cond_i,Zcol]))
            Z_list.sort()

            # Loop over each Z_j
            for Zj in Z_list:
                cond_j = self.data.loc[:,Zcol].values == Zj
                cond_ij = cond_i & cond_j

                data_ij = self.data.loc[cond_ij,:].values
                m_ij = self.data.loc[cond_ij, mcol].values

                interp_fun = interp1d(m_ij, data_ij, axis = 0)

                m_interp = np.linspace(m_ij.min(), m_ij.max(), Ninterp)

                data_interp = pd.DataFrame(interp_fun(m_interp),
                                           columns=columns)

                new_data = pd.concat((new_data, data_interp))


        # Update self.data
        self.data = new_data

        if v:
            new_shape = self.data.shape
            tf = time()
            print ("Interpolating changed the shape of the models from {0} to "
                   "{1}, and took {2} seconds.").format(old_shape,
                                                        new_shape,
                                                        tf-t0)




def load_model(filepath, model = None, columns = None, **kwargs):

    if columns is None:
        data = pd.read_csv(filepath, **kwargs)
    else:
        data = pd.read_csv(filepath, usecols=columns, **kwargs)

    md = Model(data = data, model = model)

    return md


def load_multiple_models(filelist, model = None, columns = None, **kwargs):

    # Load first model
    print 'loading model {}'.format(filelist[0])
    md = load_model(filepath=filelist[0],
                    model=model,
                    columns=columns,
                    **kwargs)

    # Load remaining models
    for i in range(1, len(filelist)):
        print 'loading model {}'.format(filelist[i])
        md = md + load_model(filepath=filelist[i],
                             model = model,
                             columns = columns,
                             **kwargs)

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







class Model_Set(object):
    """
    A generic set of stellar models.


    """
    pass



class EvTrack_Set(Model_Set):
    pass



class Isochrone_Set(Model_Set):
    pass

