__version__ = "0.0.2"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "Jan 2020"

import pandas as pd

"""Defines the Star and StellarPopulation classes and their methods

...
...

"""



class Star(object):

    def __init__(self, id = None, obs = None):
        """
        Each object of this instance represent a single star, and contains
        its observational parameters (position, distance, magnitude,
        abundances, atmospheric parameters, etc), and the methods to
        estimate different properties from these parameters.

        Parameters
        ----------
        id : str
            identificator of the star
        obs : dict, pd.DataFrame
            if a dictionary, keys must be names of observational parameters,
            and values the value of the observation. If a pd.DataFrame,
            each column must be a different observational parameter
        """

        self.id = id

        if obs is not None:
            if isinstance(obs, dict):
                self.obs = pd.DataFrame(params)

    def



class StellarPopulation(object):
    pass