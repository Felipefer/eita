__version__ = "0.0.2"
__author__ = "Felipe de Almeida Fernandes"
__email__ = "felipefer42@gmail.com"
__date__ = "Jan 2020"

"""Defines the stellar models classes and its methods

The Model class, and inherited EvTrack and Isochrone classes, are the objects 
that contain the data of the stellar models and the methods to use that data 
for different scientific tasks.


"""

import pandas as pd
import numpy as np


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
                 data=None,
                 model=None,
                 file=None,
                 columns=None):
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

        Starting Model from file

            Parameters
            ----------
            file     : str
                location of the file containing the data to be loaded.
            model    : str
                name of the stellar model this data comes from
            columns  : list of strings or list of numbers
                list of columns to be used, can be the names or their index

        """

        # Guess input type based on the inputs provided
        input_type = self.get_input_type(data=data, model=model,
                                         file=file, columns=columns)

        # Assign stellar model
        self.model = model

        # Load accordingly to input
        if input_type == 'load_from_file':
            self.load_from_file(file=file, columns=columns)

        elif input_type == 'load_from_dataframe':
            self.load_from_dataframe(dataframe=data)

        elif input_type == 'load_from_array':
            self.load_from_array(array=data, columns=columns)

    def get_input_type(self,
                       data,
                       model,
                       file,
                       columns,
                       delimiter=','):

        """
        Checks if input parameters are given correctly and identify how the
        data is being loaded.

        Raises errors or warnings if inputs are incorrectly given

        Parameters
        ----------
        *all self.__init__ accepted parameters

        Returns
        -------
        str
            a string representing the load method to be followed.
            Can be: 'load_from_db', 'load_from_file'

        """

        # Raise a warning if the stellar model is not indicated
        if model is None:
            raise Warning(("Parameter 'model' was not given when initializing "
                           "the class Model. Some methods are model dependent "
                           "and will not work."))

        # Raise error if neither file nor data are given
        if file is None and data is None:
            raise ValueError(("Impossible to initiallize Model. No data "
                              "or file given."))

        # Raise a warning if user mistakenly provide both a file and a data
        if file is not None and data is not None:
            raise Warning(("Since a 'file' is given, 'data' will be "
                           "ignored."))

        # Condition to return load_from_file
        if file is not None:
            if isinstance(file, str):
                return 'load_from_file'
            else:
                raise ValueError("Parameter 'file' must be a string")

        if data is not None:

            # Condition to return load_from_dataframe
            if isinstance(data, pd.DataFrame):
                return 'load_from_dataframe'

            # Condition to return load_from_array
            elif isinstance(data, np.array):

                if columns is None:
                    raise ValueError(("When loading from array, a list of "
                                      "column names must be provided."))

                return 'load_from_array'

            else:
                raise ValueError("Parameter 'data' must be a numpy.array or "
                                 "a pandas.DataFrame")

    def load_from_dataframe(self, dataframe):

        self.data = dataframe
        self.columns = dataframe.columns

    def load_from_file(self, file, columns):


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

