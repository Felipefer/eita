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

default_interp_phase = {}
#\TODO review this value. Used this only for testing
default_interp_phase['PARSEC'] = np.linspace(0, 10, 0.01)

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

    def interp_age(self, age, columns = None, **kargs):
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

class EvTrack_MassSet(object):
    #\TODO expand this docstring
    """

    """

    def __init__(self, EvTrack_list = None, Z = None, M = None, phase = None,
                 model = None, path = None, array = None, columns = None):
        """
        Initializes the EvTrack_MassSet. There are three possible ways to load
        EvTrack_MassSet. 1) By giving a list of EvTrack objects of same
        composition and different masses. 2) By loading data from a file,
        specified by Z, M list, model and path. 3) By explicitly providing the
        whole data Z, M list, model, array, columns

        :param EvTrack_list: list of EvTrack objects.
        :param Z: float. Metal fraction composition.
        :param M: list of floats. List of masses contained in the set
        :param phase: list of floats. The phases for which data is (or will be)
                      available. If not provided, the default procedure is:
                      1) Try to use the phases from the first provided EvTrack
                      in the EvTrack_list. 2) Try to obtain phases from the
                      array, provided it is one of the columns. 3) Try to use
                      the default phases for the given model.
        :param model: string. Specifies the model from which the data comes from
        :param array: np.array. Used only when explicitly providing the data.
                      The shape of the array must be (number_of_masses,
                      number_of_phases, number_of_columns)
        :param columns: list of strings or etcol.Ev_track_column objects.
                        used when explicitly providing the data to describe the
                        array or when the user desires to simplify the original
                        data to contain only the wanted columns.
        """

        ########################################################################
        # Perform some tests to check if all necessary data is provided

        # Check the method used to load the data
        self.EvTrack_list_is_provided = False
        self.array_is_provided = False
        self.load_info_is_provided = False

        # This will update the above booleans
        self._check_if_all_needed_info_is_given(EvTrack_list=EvTrack_list,
                                                Z=Z, M=M, phase=phase,
                                                model=model, path=path,
                                                array=array, columns=columns)

        if not any([self.EvTrack_list_is_provided,
                    self.array_is_provided,
                    self.load_info_is_provided]):

            raise ValueError("Not enought information was provided to load the"
                             "evolutionary set from any of the three possible"
                             "methods (from EvTracks list, explicitly from "
                             "data array, or load from files. Check the "
                             "documentation to see how to load data from any of"
                             " these methods.")

        # Deal with the model parameter
        if model is not None:
            if model not in load.allowed_models:
                raise ValueError(("{0} is not a supported model.\n"
                                  "Supported models are {1}."
                                  "").format(model, load.allowed_models))
            else:
                self.model = model
        else:
            self.model = "Not_Assigned"
        ########################################################################

        # Initialize EvTrack set according to the method chosen by the user's
        # parameters entries.

        # Set attributes depending on initialization kind (all but array)

        self.phase = None # Will be set by self._prepare_phase_parameter

        if self.EvTrack_list_is_provided:

            # Get reference EvTrack
            refEvTrack = EvTrack_list[0]

            # self.Z is given by the reference object
            self.Z = refEvTrack.Z
            self.Y = refEvTrack.Y

            # self.M is a list containing the initial mass of each track
            self.M = []
            for evtrack_obj in EvTrack_list:
                self.M.append(evtrack_obj.M)

            # self.model is given by the reference object
            self.model = refEvTrack.model

            # if columns is None, get it from reference object
            if columns is None:
                self.columns = refEvTrack.column_names
            else:
                self.columns = columns

            # phase is given by entry parameter, or taken from reference, or
            # taken from default value for model.
            self._prepare_phase_parameter(refEvTrack=refEvTrack,
                                          phase=phase, array=array,
                                          columns=columns) # Sets self.phase


        elif self.load_info_is_provided:

            # Get reference EvTrack
            refEvTrack = EvTrack(mass=M[0], Z=Z, path=path, model=model)

            # self.Z is given by entry parameter
            self.Z = Z
            self.Y = utils.abundanceY(Z)

            # self.M is given by entry parameter
            self.M = M

            # self.model is given by entry parameter
            self.model = model

            # phase is given by entry parameter, or taken from reference, or
            # taken from default value for model.
            self._prepare_phase_parameter(refEvTrack=refEvTrack,
                                          phase=phase, array=array,
                                          columns=columns)  # Sets self.phase

            # if columns is None, get it from reference object
            if columns is None:
                self.columns = refEvTrack.column_names
            else:
                self.columns = columns


        elif self.array_is_provided:
            # self.Z is given by entry parameter
            self.Z = Z
            self.Y = utils.abundanceY(Z)

            # self.M is given by entry parameter
            self.M = M

            # self.model is given by entry parameter
            self.model = model

            # phase is given by entry parameter, or taken from reference, or
            # taken from default value for model.
            self._prepare_phase_parameter(refEvTrack=None,
                                          phase=phase, array=array,
                                          columns=columns)  # Sets self.phase

        # Set up the array
        if self.array_is_provided:
            self.array = array

        # for the "EvTrack_list" and "load from file" cases:
        else:
            # Generate an empty array
            self.array = np.empty((len(self.M),
                                   len(self.phase),
                                   len(self.columns)))
            self.array[:] = np.nan

            # Now, fill the array
            for i in range(len(self.M)):

                # Get EvTrack for this step
                if self.EvTrack_list_is_provided:
                    EvTrack_obj = EvTrack_list[i]
                elif self.load_info_is_provided:
                    EvTrack_obj = EvTrack(mass=M[i], Z=Z,
                                          path=path, model=model)

                # Interpolate phases
                EvTrack_obj.interp_phase(phase = self.phase,
                                         return_EvTrack = False)

                # Simplify the array
                EvTrack_obj.simplify_array(columns=self.columns,
                                           return_EvTrack=False)

                self.array[i, :, :] = EvTrack_obj.array

    def _prepare_phase_parameter(self, refEvTrack = None, phase = None,
                                 array = None, columns = None):
        """
        Used internally to set which values will be used for phase if it is not
        provided by the user.
        """

        if phase is not None:
            if utils.isiterable(phase):
                self.phase = phase
            else:
                raise ValueError("Phase parameter must be iterable.")

        else:
            if self.EvTrack_list_is_provided:
                # Try to get the phases from the first object in the list
                try:
                    self.phase = refEvTrack.phase

                except:
                    try:
                        # Try to get default model phases
                        self.phase = default_interp_phase[self.model]

                    except:
                        raise ValueError("Could not assign phase attribute.")

            elif self.array_is_provided:
                # Try to get the phases from the first object in the array
                try:
                    self.phase = array[0, :, columns == 'phase']

                except:
                    try:
                        # Try to get default model phases
                        self.phase = default_interp_phase[self.model]

                    except:
                        raise ValueError("Could not assign phase attribute.")

            elif self.load_info_is_provided:
                try:
                    self.phase = refEvTrack.phase
                except:
                    try:
                        # Try to get default model phases
                        self.phase = default_interp_phase[self.model]

                    except:
                        raise ValueError("Could not assign phase attribute.")

    def _check_if_all_needed_info_is_given(self, EvTrack_list = None,
                                           Z = None, M = None, phase = None,
                                           model = None, path = None,
                                           array = None, columns = None):

        """
        Used internally to check if the user provided all the necessary data to
        initialize the array from any of the given methods.
        """

        EvTrack_list_is_provided = False
        array_is_provided = False
        load_info_is_provided = False

        # Check if EvTrack_list is provided and if it is a list
        if EvTrack_list is not None:
            if utils.isiterable(EvTrack_list):
                EvTrack_list_is_provided = True
            else:
                raise ValueError("if provided, EvTrack_list must be a list of"
                                 "EvTrack objects")

        # If EvTrack_list is provided, check if unecessary data was
        # also given by the user:
        if EvTrack_list_is_provided:
            param_dict = {'Z': Z, 'M': M, 'model': model, 'path': path,
                          'array': array}
            for param in param_dict.keys():
                if param_dict[param] is not None:
                    raise ValueError(("When providing EvTrack_list, it is not "
                                      "necessary to also provide the parameter "
                                      "{0}, which may cause conflicts during "
                                      "evaluation.").format(param))

        # Check if array is provided, meaning data will be given explicitly
        if array is not None:
            array_is_provided = True

        # If array is provided, check if the other necessary information is also
        # provided.
        if array_is_provided:
            param_dict = {'Z': Z, 'M': M, 'model': model, 'columns': columns}

            for param in param_dict.keys():
                if param_dict[param] is None:
                    raise ValueError(("When explicitly providing the data, "
                                      "parameter {0} must be assigned"
                                      ".").format(param))

        # Check if array's shape agrees with the other given information
        if array_is_provided:
            if array.shape[0] != len(M):
                raise ValueError(("The number of provided masses in list M "
                                  "({0}) does not agree with the size of the "
                                  "dimension 0 of the given array ({1})"
                                  ".").format(len(M), array.shape[0]))

            if array.shape[2] != len(columns):
                raise ValueError(("The number of provided columns "
                                  "({0}) does not agree with the size of the "
                                  "dimension 2 of the given array ({1})"
                                  ".").format(len(columns), array.shape[2]))

        # If neither array, nor EvTrack objects are provided, check if all the
        # information to load from a file is provided
        if not any([EvTrack_list_is_provided, array_is_provided]):
            param_dict = {'Z': Z, 'M': M, 'model': model, 'path': path}

            for param in param_dict.keys():
                if param_dict[param] is None:
                    raise ValueError(("When loading data from files, "
                                      "parameter {0} must be assigned"
                                      ".").format(param))

            # If it gets here
            load_info_is_provided = True

        self.EvTrack_list_is_provided = EvTrack_list_is_provided
        self.array_is_provided = array_is_provided
        self.load_info_is_provided = load_info_is_provided

        ########################################################################

class EvTrack_setM(object):
    #\TODO expand this docstring
    """

    """

    def __init__(self, Z = None, M = None, phase = None,
                 model = None, array = None, columns = None):

        # Check if given model is supported in this version of eitapy
        if model is None:
            model = 'Not_Assigned'

        elif model not in load.allowed_models:
            raise ValueError(("{0} is not a supported file format.\n"
                              "Supported formats are {1}."
                              "").format(model, load.allowed_models))

        # Assign empty list as default value for M
        if M is None:
            self.M = []
        else:
            self.M = M

        self.phase = phase
        self.columns = columns
        self.Z = Z

        # If Z is provided, calculate Y
        if self.Z is not None:
            self.Y = utils.abundanceY(Z)

        self.model = model

        # Initialize self.array
        self.array = array

        # if array is None, initialize array using the shape described by len of
        # M, phase and columns
        if self.array is None:
            if self.phase is not None:
                if self.columns is not None:
                    self._initialize_array()


    def _initialize_array(self):
        """
        Initialize the data array with the shape defined by the number of masses
        in the set, number of phases in each EvTrack and the number of columns
        in each EvTrack

        Assigns self.array or raises an error telling what went wrong
        """

        if self.array is not None:
            raise ValueError("self.array is already initialized")

        else:

            if self.phase is not None:

                if self.columns is not None:
                    # array shape sizes
                    d1 = len(self.M)
                    d2 = len(self.phase)
                    d3 = len(self.columns)

                    self.array = np.empty((d1, d2, d3))
                    self.array[:] = np.nan

                else:
                    raise ValueError(("Can't initialize array if self.columns"
                                      "is None"))

            else:
                raise ValueError("Can't initialize array if self.phase is None")

    def add_track(self, evtrack):
        """
        add new evtrack to the data in the EvTrack_setM
        """

        # Attribute the EvTrack metallicity to the set if none has been assigned
        if self.Z is None:
            self.Z = evtrack.Z
            self.Y = utils.abundanceY(self.Z)

        # Attribute the EvTrack stage if the set stages are not assigned yet
        if self.phase is None:
            self.phase = evtrack.phase

        # Check if Set and EvTrack metallicities are the same
        if self.Z != evtrack.Z:
            raise ValueError(("EvTrack metallicity does not correspond to the"
                              "metallicity of the set and can not be addad."))

        # Find the index of the mass to be added in self.mass
        new_mass_id = get_new_mass_index(mass_list = self.M,
                                         new_mass = evtrack.M)




def get_new_mass_index(mass_list, new_mass):
    """
    returns the index the newly added "new_mass" has in the ordered mass_list
    """

    # Make a copy of the mass_list so it doesn't get eddited by this function
    new_mass_list = copy.deepcopy(mass_list)

    # Add the new_mass to the list
    new_mass_list.append(new_mass)

    # Sort the list
    new_mass_list.sort()

    # Get the index of the new_mass in the updated list
    index = new_mass_list.index(new_mass)

    return index
