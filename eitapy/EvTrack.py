__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "June 2017"

#\TODO expand this docstring
"""
EvTrack.py contains the functions used to work with evolutionary tracks
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import utils
import load

class EvTrack(object):
    #\TODO expand this docstring
    """
    
    """
    
    def __init__(self, mass, Z, path, file_format = 'PARSEC'):
        
        # Check if given file_format is supported in this version of eitapy
        if file_format not in load.allowed_file_formats:
            raise ValueError(("{0} is not a supported file format.\n"
                              "Supported formats are {0}."
                              "").format(load.allowed_file_formats))
        
        # Load EvTrack according to the file format
        EvTrackData = None
        
        if file_format == 'PARSEC':
            EvTrackData = load.LoadedEvolutionaryTrack(mass, Z,
                                                       path, file_format)
        
        # End of loading
        # Check if loading went fine
        if EvTrackData == None:
            raise utils.Loading("Could not load evolutionary track file")
        
        # Attributes
        self.mass = mass
        self.Z    = Z
        self.Y    = EvTrackData.Y
        
        # Here I change the name from file_format to file_origin because, at
        # this point, loading should have standardized everything, so the format
        # is no longer a 'special case'
        self.file_origin  = file_format
        self.column_names = EvTrackData.column_names

        # Get number of columns
        self.Ncols  = len(self.column_names)
        
        # Get number of lines
        self.Nlines = len(getattr(EvTrackData, self.column_names[0]))

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
        self.array = np.empty([self.Nlines, self.Ncols], dtype = float)
        self.array[:] = np.nan
        self.column_index = {}
        
        # Fill the array and point the attributes to it:
        for i in range(self.Ncols):
            
            column = self.column_names[i]
            
            self.column_index[column] = i
            self.array[:,i] = getattr(EvTrackData, column)
            setattr(self, column, self.array[:,i])
    
    
    def simplify_array(self, columns):
        """
        Return a new data array containing only data from the chosen columns
        
        :param columns: string or list of strings
        :return: data array
        """
        
        # Obtain column indexes
        index = []
        for column in columns:
            index.append(self.column_index[column])
            
        array = self.array[:, index]
        
        return array

    def plot(self, column_name1, column_name2, **kargs):
        """
        Uses matplotlib.pyplot.plot to plot self.column_name1 as x and
        self.column_name2 as y

        :param column_name1: string that must be in self.column_names
        :param column_name2: string that must be in self.column_names
        """

        # First test if column_name1(2) is in the self.column_names list
        if any((column_name1 not in self.column_names,
                column_name2 not in self.column_names)):

            raise ValueError(("Only column names in self.column_names are "
                              "accepted"))

        x = getattr(self, column_name1)
        y = getattr(self, column_name2)

        plt.plot(x, y, **kargs)

    def _update_colname_attributes(self):
        """
        used internally when self.array is reassigned
        """
        for i in range(self.Ncols):
            column = self.column_names[i]
            self.column_index[column] = i
            setattr(self, column, self.array[:, i])

    def interp_phase(self, N = 10000, phase = None, **kargs):
        """
        Interpolates the evolutionary track producing :param N points evenly
        distributed according to evolutionary phase OR interpolate the data
        for the given :param phase numbers.

        :param N: integer like.
        :param phase: list like.

        also accepted any keyword argument for the function interp1d from the
        scipy.interpolate module
        """

        # First test if the evolutionary track has the phase attribute that
        # is needed for the interpolation
        if not hasattr(self, 'phase'):
            raise AttributeError(("Object does not contain the phase attribute,"
                                  " therefore, it can't be interpolated."))

        # Define values to interpolate
        if phase is None:
            # Remove possible nan values from self.phase
            phase_tmp = self.phase[~np.isnan(self.phase)]
            phase = np.linspace(phase_tmp.min(), phase_tmp.max(), N)

        # Create the interpolation function
        interp_function = interp1d(x = self.phase,
                                   y = self.array,
                                   axis = 0,
                                   **kargs)
        '''
        \TODO also consider a way to let the user choose if he/she wants to
        update the array or create a new object with the new data
        '''
        # Update array
        self.array = interp_function(phase)

        # Update attributes
        self._update_colname_attributes()