__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "June 2017"

#\TODO expand this docstring
"""
EvTrack.py contains the functions used to work with evolutionary tracks
"""

import copy
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

import config
import utils
import load

class EvTrack(object):
    #\TODO expand this docstring
    """
    
    """
    
    def __init__(self, mass, Z, model = 'Not_Assigned', path = None,
                 array = None, columns = None):

        # Check if given model is supported in this version of eitapy
        if model not in load.allowed_models:
            raise ValueError(("{0} is not a supported file format.\n"
                              "Supported formats are {0}."
                              "").format(load.allowed_models))
        
        # Load EvTrack according to the file format
        EvTrackData = None
        
        if model == 'PARSEC':
            EvTrackData = load.LoadedEvolutionaryTrack(mass = mass,
                                                       Z = Z,
                                                       model = model,
                                                       path = path,
                                                       array = array,
                                                       columns = columns)
        
        # End of loading
        # Check if loading went fine
        if EvTrackData is None:
            raise utils.Loading("Could not load evolutionary track file")
        
        # Attributes
        self.mass = mass
        self.M    = mass
        self.Z    = Z
        self.Y    = EvTrackData.Y
        
        self.model        = model
        self.column_names = EvTrackData.column_names
        self.column_fmt   = EvTrackData.column_fmt

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
            self.array[:, i] = getattr(EvTrackData, column)
            setattr(self, column, self.array[:, i])
    
    
    def return_simplified_array(self, columns):
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

    def simplify_array(self, columns, return_EvTrack = True):
        """
        Simplify the data array for it to contain only the chosen columns

        :param columns: string or list of strings
        :param return_EvTrack: if true, returns a new EvTrack object. If false,
                               updates the data in this object.
        """

        # Use recursivity if the user desires to return a new EvTrack object
        # with the simplified array
        if return_EvTrack:
            new_track = copy.deepcopy(self)
            new_track.simplify_array(columns, return_EvTrack = False)

            return new_track

        else:
            # Obtain column indexes
            index = []
            for column in columns:
                index.append(self.column_index[column])

            # Update self.array
            self.array = self.array[:, index]

            # Update attributes
            self._update_colname_attributes(column_names = columns)

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

    def _update_colname_attributes(self, column_names = None):
        """
        used internally when self.array is reassigned
        """

        # Assign all columns if None is assigned
        if column_names is None:
            column_names = self.column_names

        # Delete attributes that are no longer used and update self.column_fmt
        # \TODO this can be written better

        for i in range(len(self.column_names)):
            if self.column_names[i] not in column_names:
                delattr(self, self.column_names[i])

        # Update number of columns
        self.Ncols = len(column_names)

        # Reassing remaining columns for the new data in the array
        self.column_index = {}
        new_column_fmt    = {}

        for i in range(self.Ncols):
            column = column_names[i]
            self.column_index[column] = i
            setattr(self, column, self.array[:, i])

            # Also update self.column_fmt
            new_column_fmt[column] = self.column_fmt[column]

        self.column_fmt = new_column_fmt

        # Update column names
        self.column_names = column_names

    def interp_phase(self, N = 10000, phase = None, return_EvTrack = True,
                     **kargs):
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

        # If a new EvTrack is to be created, copy, evaluate and return it
        if return_EvTrack:
            new_track = copy.deepcopy(self)
            new_track.interp_phase(N = N, phase = phase, return_EvTrack=False,
                                   **kargs)

            return new_track

        # Otherwise, only evaluate
        else:
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

            # Update array
            self.array = interp_function(phase)

            # Update self.Nlines
            self.Nlines = len(phase)

            # Update attributes
            self._update_colname_attributes()

    def interpolate_age(self, age, columns = None, **kargs):
        """
        returns interpolated data array for a given age

        :param age (years): desired interpolated age, float.
        :param     columns: list of strings with column names to be
                            interpolated.
        :param     **kargs: parameters passed to interp1d function.
        :returns array containing data for the wanted columns and given age.
        """

        # Deal with default values
        if columns is None:
            columns = self.column_names

        # Check if "age" attribute is present and try to run with "log_age" if
        # it is not.
        if not hasattr(self, 'age'):
            try:
                pass
                # \todo complete here once interpolate_log_age is done and try it
            except:
                raise AttributeError(("Track does not have age attribute to "
                                     "interpolate"))

        # Get simplified array to interpolate
        array = self.return_simplified_array(columns)

        array_interp_function = interp1d(self.age, array, axis = 0, **kargs)
        age_array_line = array_interp_function(age)

        return age_array_line
    

    def default_save_filename(self):
        """
        returns the default filename used by method "save" to create a .dat file
        """

        filename0 = "EvTrack_{0}".format(self.model)
        filename1 = "_M{:07.3f}_Z{:07.5f}_Y{:07.5f}.dat".format(self.M,
                                                             self.Z,
                                                             self.Y)

        filename = filename0+filename1
        return filename

    def save(self, filename = None, folder = None, columns = None,
             delimiter = ',', verbose = False, **kargs):
        """
        Saves the EvTrack data array to a file.
        
        :param  filename: name of the file to be created.
        :param    folder: directory where file will be stored.
        :param   columns: list of strings with the name of the columns to be
                          saved.
        :param delimiter: string used as column separator
        :param   **kargs: arguments passed to the np.savetxt function
        """

        # Deal with default values
        if folder is None:
            folder = config.default_evtrack_save_folder

        if filename is None:
            filename = self.default_save_filename()

        if columns is None:
            columns = self.column_names

        # Prepare fmt for np.savetxt
        fmt = []

        for col in columns:
            fmt.append(self.column_fmt[col])

        # Prepare header
        header = "#" + ("{0} ".format(delimiter)).join(columns) + "\n"

        if verbose:
            print "\nSaving to file {0},".format(filename)
            print "in the folder {0},".format(folder)
            print "using the formats {0}.".format(self.column_fmt)

        # Get the array
        array = self.return_simplified_array(columns)

        # Get full_path
        full_path = folder + '/' + filename

        # Save file
        with open(full_path, 'w') as f:
            f.write(("#File data originally "
                     "comes from {0} set\n").format(self.model))
            f.write(header)
            np.savetxt(fname     = f,
                       X         = array,
                       fmt       = fmt,
                       delimiter = delimiter,
                       **kargs)