__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "June 2017"

#\TODO expand this docstring
"""
EvTrack.py contains the functions used to work with evolutionary tracks
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

default_interp_phase = {}
#\TODO review this value. Used this only for testing
default_interp_phase['PARSEC'] = np.concatenate((np.linspace(1+1e-8,1+1e-7,10),
                                                 np.linspace(1+1e-7,1+1e-6,10),
                                                 np.linspace(1+1e-6,1+1e-5,10),
                                                 np.linspace(1+1e-5,1+1e-4,10),
                                                 np.linspace(1+1e-4,1+1e-3,10),
                                                 np.linspace(1+1e-3,1+1e-2,10),
                                                 np.arange(1.01, 16, 0.01)))

class EvTrack(object):
    #\TODO expand this docstring
    """
    
    """
    
    def __init__(self, mass, Z, model = 'Not_Assigned', path = None,
                 array = None, columns = None, HB=False):

        # Check if given model is supported in this version of eitapy
        if model not in load.allowed_models:
            raise ValueError(("{0} is not a supported file format.\n"
                              "Supported formats are {0}."
                              "").format(load.allowed_models))
        
        # Load EvTrack according to the file format
        EvTrackData = None

        # Todo: Review this. By design, all model dependent characteristics
        # Todo: should be dealt with in the load.py
        if model == 'PARSEC':
            EvTrackData = load.LoadedEvolutionaryTrack(mass = mass,
                                                       Z = Z,
                                                       model = model,
                                                       path = path,
                                                       array = array,
                                                       columns = columns,
                                                       HB = HB)
        
        # End of loading
        # Check if loading went fine
        if EvTrackData is None:
            raise utils.LoadingError("Could not load evolutionary track file")
        
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
        
        if HB is True:
            self.hasHB = True
            self.onlyHB = True
        else:
            self.hasHB = False
            self.onlyHB = False
    
    def return_simplified_array(self, columns):
        """
        Return a new data array containing only data from the chosen columns
        
        :param columns: string or list of strings
        :return: data array
        """
        etcol_type = etcol.Ev_track_column
        if all(isinstance(obj, etcol_type) for obj in columns):
            columns = utils.etcolobjs2colnames(columns)

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

        # \todo write test to convert columns from etcol to strings if
        # necessary
        etcol_type = etcol.Ev_track_column
        if all(isinstance(obj, etcol_type) for obj in columns):
            columns = utils.etcolobjs2colnames(columns)

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
                                       bounds_error = False,
                                       fill_value = np.nan,
                                       **kargs)

            # Update array
            self.array = interp_function(phase)

            # Update self.Nlines
            self.Nlines = len(phase)

            # Update attributes
            self._update_colname_attributes()
            self._update_HB_attributes()

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

        array_interp_function = interp1d(self.age,
                                         array,
                                         axis = 0,
                                         bounds_error=False,
                                         fill_value=np.nan,
                                         **kargs)
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

    def rgb_mass_loss(self, eta = 0.477):
        
        # Reimers Formula according to McDonald & Zijlstra (2015).
        #
        # Mdot = (4e-13 * eta_R) * (LR)/(M) [M_sun/yr]
        #
        # [L] = [L_sun], [R] = [R_sun], [M] = [M_sun]
        # eta_R = 0.477 +- 0.070 (McDonald & Zijlstra, 2015)

        R_sun_cm = 6.957e10  # [cm]
        
        # Select only RGB phase and convert R, L, M to the correct units
        if self.model == "PARSEC":
            
            RGB_phase_init = 8
            RGB_phase_end  = 11
            
            RGB = ((self.phase >= RGB_phase_init) &
                   (self.phase <= RGB_phase_end))
            
            try:
                R = (10**self.log_R[RGB])/R_sun_cm # [R_sun]
            except AttributeError:
                raise AttributeError(("Attribute log_R is not present and the "
                                      "mass loss during RGB phase cannot be "
                                      "estimated"))
            
            try:
                L = 10**self.log_L[RGB]
            except:
                raise AttributeError(("Attribute log_L is not present and the "
                                      "mass loss during RGB phase cannot be "
                                      "estimated"))
            
            try:
                M = copy.deepcopy(self.mass[RGB])
            except AttributeError:
                raise AttributeError(("Attribute mass is not present and the "
                                      "mass loss during RGB phase cannot be "
                                      "estimated"))
            
            try:
                t = copy.deepcopy(self.age[RGB])
            except AttributeError:
                raise AttributeError(("Attribute age is not present and the "
                                      "mass loss during RGB phase cannot be "
                                      "estimated"))
            
        else:
            raise AttributeError(("The method RGB_mass_loss does not support "
                                  "the {0} model").format(self.model))

        # If RGB is not present in the evolutionary track, mass loss is not
        # calculated and the final RGB mass is returned as None
        if len(M) == 0:
            return None

        # Otherwise, calculate mass loss during RGB and return final mass
        mdot    = np.empty(len(M))
        mdot[:] = np.nan
        
        for i in range(len(M)-1):
            Dt = t[i+1]-t[i]
            DM = (4e-13 * eta) * (L[i]*R[i])/(M[i]) * Dt
            M[i+1] = M[i] - DM
        
            mdot[i] = DM/Dt

        if hasattr(self, 'mdot'):
            self.mdot[RGB] = mdot
        
        self.mass[RGB] = M

        RGB_final_mass = M[-1]
        return RGB_final_mass

    def __add__(self, evtrack):
        """
        Adds data from two EvTracks of same initial mass and composition. This
        is used mostly when data from two different evolutionary phases are
        stored in different files.
        """

        # Perform a few tests to see if this addition is possible ##############
        if self.M != evtrack.M:
            raise ValueError(("You can only concatenate data from evolutionary "
                              "tracks of the same initial mass"))

        if self.Z != evtrack.Z:
            raise ValueError(("You can only concatenate data from evolutionary "
                              "tracks of the same initial composition"))

        if self.column_names != evtrack.column_names:
            raise ValueError(("The columns of the data you are trying to"
                              "concatenate, does not match."))
        ########################################################################

        # Remove nan values from evtrack data
        evtrack.array = evtrack.array[~np.isnan(evtrack.phase), :]
        evtrack.phase = evtrack.phase[~np.isnan(evtrack.phase)]

        # Remove from self the phase interval that contains both self and
        # evtrack data
        print "set(self.phase: {}".format(set(np.floor(self.phase)))
        print "set(evtrack.phase: {}".format(set(np.floor(evtrack.phase)))
        
        remove_common_phases_from_self = ((self.phase < evtrack.phase.min()) |
                                          (self.phase > evtrack.phase.max()))

        phase0 = copy.deepcopy(self.phase)[remove_common_phases_from_self]
        array0 = copy.deepcopy(self.array)[remove_common_phases_from_self]

        print "array0.shape: {}".format(array0.shape)
        
        # Concatenate both data
        phase = np.concatenate((phase0, evtrack.phase))
        array = np.concatenate((array0, evtrack.array))

        # Order the data
        argsort = phase.argsort()
        array = array[argsort, :]

        # create new object and update data
        evtrack_combined = copy.deepcopy(self)
        evtrack_combined.array = array
        evtrack_combined._update_colname_attributes()
        evtrack_combined._update_HB_attributes()
        
        return evtrack_combined
    
    def _update_HB_attributes(self):
        """
        
        :return:
        """
        
        try:
            phase = self.phase[~np.isnan(self.phase)]
        except AttributeError:
            raise AttributeError(("Could not access self.phase to update "
                                  "self.hasHB and self.onlyHB."))
        
        model_RGB_tip = None
        if self.model == "PARSEC":
            model_RGB_tip_phase = 11
        else:
            model_RGB_tip_phase = None
        
        if model_RGB_tip_phase is None:
            raise AttributeError(("Model {} is not supported by the "
                                  "_update_HB_attributes "
                                  "method.").format(self.model))

        if np.floor(phase.max()) <= model_RGB_tip_phase:
            self.hasHB = False
        else:
            self.hasHB = True
        
        if phase.min() >= (model_RGB_tip_phase+1):
            self.onlyHB = True
        else:
            self.onlyHB = False

class EvTrack_MassSet(object):
    #\TODO expand this docstring
    """

    """

    def __init__(self, EvTrack_list = None, Z = None, M = None, phase = None,
                 model = None, path = None, array = None, columns = None,
                 HB = False):
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

        self.kind = "MassSet"
        ########################################################################
        # Perform some tests to check if all necessary data is provided

        # Prepare Mass parameter for the case M is a single value
        M = utils.array1d(M) if (M is not None) else None

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

            # self.columns is given by entry parameter
            self.columns = columns

            # phase is given by entry parameter, or taken from reference, or
            # taken from default value for model.
            self._prepare_phase_parameter(refEvTrack=None,
                                          phase=phase, array=array,
                                          columns=columns)  # Sets self.phase

        # Fix for the case of the Set containing only one mass
        if not utils.isiterable(self.M):
            self.M = [self.M]

        # Set up the array
        if self.array_is_provided:
            if len(self.M) == 1:
                if array.ndim == 2:
                    self.array = np.empty((1, array.shape[0], array.shape[1]))
                    self.array[0, :, :] = array
                elif array.ndim == 3:
                    self.array = array
                else:
                    raise AttributeError("Array has wrong number of dimensions.")
            else:
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


        # Set an integer list describing the phases present in the set
        self.phases = np.array(list(set(np.around(self.phase))), dtype=int)

        # Set the array containing the age of the beginning of each phase for
        # each mass
        self._set_array_age_beginning_phase()
        self._interp_mass_function = None

    def simplify_array(self, columns, return_object = True):
        """
        Simplify the data array for it to contain only the chosen columns

        :param columns: string or list of strings
        :param return_object: if true, returns a new EvTrack_MassSet object.
                              If false, updates the data in this object.
        """

        # Use recursivity if the user desires to return a new EvTrack_MassSet
        # object with the simplified array
        if return_object:
            new_set = copy.deepcopy(self)
            new_set.simplify_array(columns, return_object=False)

            return new_set

        else:
            # Update self.columns
            etcol_type = etcol.Ev_track_column
            if all(isinstance(obj, etcol_type) for obj in columns):
                columns = utils.etcolobjs2colnames(columns)

            # Create new self.array
            new_array = np.empty((len(self.M),
                                  len(self.phase),
                                  len(columns)))
            new_array[:] = np.nan

            # Update self.array with simplified data
            for i in range(len(self)):
                track_temp = self[i]
                track_temp.simplify_array(columns = columns,
                                          return_EvTrack= False)

                new_array[i, :, :] = track_temp.array

            self.array = new_array
            self.columns = columns
            
    def __len__(self):
        return len(self.M)

    def __getitem__(self, i):
        """
        self.__getitem__ returns the EvTrack object which has mass self.M[i]
        """

        # Had to do it to fix problems when len(self.M) == 1: ##################
        if len(self.array.shape) == 2:
            array = self.array

        else:
            array = self.array[i, :, :]

        if not utils.isiterable(self.M):
            self.M = [self.M]
        ########################################################################

        evtrack_i = EvTrack(mass = self.M[i],
                            Z = self.Z,
                            model = self.model,
                            array = array,
                            columns = self.columns)

        return evtrack_i

    def __iter__(self):
        """
        Iterates the set returning one EvTrack at a time
        """

        for i in range(len(self.M)):
            # Create EvTrack object from array data
            evtrack_i = EvTrack(mass=self.M[i],
                                Z=self.Z,
                                model=self.model,
                                array=self.array[i, :, :],
                                columns=self.columns)

            yield evtrack_i

    def get_interp_mass_function(self, record_interp_function = True,
                                 **kargs):
        """
        Returns the interp1d function for the Set as a function of mass.
        """
        
        if self._interp_mass_function is not None:
            return self._interp_mass_function
        
        else:
            interp_function = interp1d(x = self.M,
                                       y = self.array,
                                       axis = 0,
                                       bounds_error=False,
                                       fill_value=np.nan,
                                       **kargs)
            
            if record_interp_function:
                self._interp_mass_function = interp_function
            
            return interp_function

    def interp_phase(self, phase, new_object = False,
                    record_interp_function = True, **kargs):

        if new_object:
            new_set = copy.deepcopy(self)
            new_set.interp_phase(phase=phase, new_object = False, **kargs)

            return new_set

        else:
            # Considering that the __init__ already deals with a interpolation
            # of phases, this was the simplest way to implementing this method
            # without having to write too much code.
            self = EvTrack_MassSet(Z = self.Z, M = self.M,
                                   model = self.model, array = self.array,
                                   columns = self.columns, phase = phase)

    def interp_mass(self, M, new_object = False,
                    record_interp_function = True, **kargs):
        """
        Interpolates the evolutionary track set for the given list of masses M

        :param M: list of masses to interpolate

        also accepts any keyword argument for the function interp1d from the
        scipy.interpolate module
        """

        # This controls if an interpolation is actually necessary
        interpolate = True

        # If a new EvTrack Set is to be created, copy, evaluate and return it
        if new_object:
            new_set = copy.deepcopy(self)
            new_set.interp_mass(M=M, new_object = False, **kargs)

            return new_set

        # Otherwise, only evaluate
        else:
            # First check if there is enough data to interpolate from.
            # And also check if data needs to be modified at all.
            if len(self.M) == 1:
                M = utils.array1d(M)
                if list(M) == list(self.M):
                    # Nothing needs to be modified
                    interpolate = False
                else:
                    raise ValueError("This Set does not contain enough data "
                                     "to interpolate for this mass.")

            if interpolate:
                # If values asked for interpolation are already present
                # in the data, use them:
                if np.in1d(M, self.M).all():

                    # Even in this case, record the interpolate function if required
                    if record_interp_function:
                        self.interp_mass_function = interp1d(x=self.M,
                                                             y=self.array,
                                                             axis=0,
                                                             bounds_error=False,
                                                             fill_value=np.nan,
                                                             **kargs)

                    self.array = self.array[np.in1d(self.M, M), :, :]
                    self.M = M

                else:
                    # If interpolation function is recorded, use it.
                    if self._interp_mass_function is not None:
                        self.array = self._interp_mass_function(M)
                        self.M = M

                    else:
                        # Create the interpolation function
                        interp_function = interp1d(x=self.M,
                                                   y=self.array,
                                                   axis=0,
                                                   bounds_error=False,
                                                   fill_value=np.nan,
                                                   **kargs)

                        self.array = interp_function(M)
                        self.M = M

                        if record_interp_function:
                            self._interp_mass_function = interp_function

    def interp(self, M, phase = None, new_object = False,
                    record_interp_function = True, **kargs):
        """
        Interpolates the evolutionary track set for the given list of masses M

        :param phase: list of phases to interpolate
        :param M: list of masses to interpolate

        also accepts any keyword argument for the function interp1d from the
        scipy.interpolate module
        """

        # If a new EvTrack Set is to be created, copy, evaluate and return it
        if new_object:
            new_set = copy.deepcopy(self)
            new_set.interp(M=M, phase=phase, new_object=False, **kargs)

            return new_set

        # Otherwise, only evaluate
        else:
            if phase is None:
                phase = self.phase

            # If interpolation function is recorded, use it, but only if phase
            # is None or equal to self.phase.
            if phase == self.phase:
                if self._interp_mass_function is not None:
                    self.interp_mass(M, new_object = False,
                                     record_interp_function = False,
                                     **kargs)
            # If interpolation function will not be used, perform interpolation
            else:
                # First interpolate phase
                self.interp_phase(phase, new_object=False, **kargs)
                # Then interpolate mass
                self.interp_mass(M, new_object = False,
                                 record_interp_function=record_interp_function,
                                 **kargs)

    def plot(self, xcol, ycol, M = None, **kargs):

        """
        """

        if M is None:
            M = self.M

        # If M given is different from self.M, interpolation is needed. Here
        # I will interpolate while creating a new object Set, and run the method
        # for the interpolated one.
        if list(M) != list(self.M):
            new_Set = self.interp_mass(M = M, new_object = True)

            # In this case, by definition M will be equal to new_Set.M, and
            # interpolation will not be necessary
            new_Set.plot(xcol = xcol, ycol = ycol, M = M, **kargs)

        # If M list given is the same as self.M, interpolation is not needed.
        else:
            for track in self:
                track.plot(xcol, ycol, **kargs)

    def __add__(self, evtrack):
        #\TODO implement
        """
        adds new data to self.array from an evtrack object provided it is from
        the same model, has the same composition and covers the same columns.

        the phases in evtrack.phase will be interpolated for its data to
        correspond to self.phase
        """

    def _set_array_age_beginning_phase(self):
        """
        Used internally to create the array that contains the age of the
        beginning of each phase (columns) for each mass in the set (rows).
        """

        # Get possible stages
        phases = self.phases

        # Set array that will contain the data
        age_beginning_phase = np.empty((len(self.M), len(phases)))
        age_beginning_phase[:] = np.nan

        for i in range(len(self.M)):
            track = self[i]

            # \todo change this so it works even if the column given is not
            #  exactly the age (e.g. self.LogAge)

            age_beginning_phase_i_fun = interp1d(x = track.phase,
                                                 y = track.age,
                                                 bounds_error=False,
                                                 fill_value=np.nan)

            age_beginning_phase[i,:] = age_beginning_phase_i_fun(phases)

        self.age_beg_phase = age_beginning_phase

    def make_isochrone(self, age, N = 5000, isoc_columns = None,
                       verbose = False):
        """
        Generates an isochrone of given age sampled by N points
        """

        # Set up columns parameter and prepare Set for interpolation
        if isoc_columns is None:
            isoc_columns = self.columns
            Set_for_interp = copy.deepcopy(self)
            
            if verbose:
                # print message
                print "Isoc_columns set as self.columns."

        else:

            if verbose:
                print "Simplifying data array to contain only given columns."
                t0 = time()
                
            Set_for_interp = self.simplify_array(columns = isoc_columns,
                                                 return_object= True)
            if verbose:
                # print message
                print "Simplifying took {0} seconds.".format(time()-t0)
              
        if verbose:
            print "Estimating masses necessary to sample the isochrone."
            t0 = time()
            
        isoc_masses = self.get_isochrone_masses(age=age, N=N)

        if verbose:
            print "Estimating {0} masses took {1} seconds.".format(N, time()-t0)
            print "Obtaining interpolation coeficients"
            t0 = time()
            
        # Update Set_for_interp
        interp_function = Set_for_interp.get_interp_mass_function()

        if verbose:
            print "Obtaining coeficients took {0} seconds.".format(time()-t0)
            print "Preparing isochrone array"
        
        # Generate isochrone array
        
        isoc_array = np.empty((N, len(isoc_columns)))
        isoc_array[:] = np.nan

        # Preparing columns
        if all(isinstance(name, str) for name in isoc_columns):
            isoc_columns = utils.colnames2etcolobjs(isoc_columns)
            
        if verbose:
            print "Empty array of shape {0} created.".format(isoc_array.shape)
            print "Filling isochrone array"
            t0 = time()
            
        for i in range(N):

            track_array = interp_function(isoc_masses[i])
            
            track_temp = EvTrack(mass = isoc_masses[i],
                                 Z = self.Z,
                                 model = self.model,
                                 array = track_array,
                                 columns = isoc_columns)
            
            isoc_array[i, :] = track_temp.interp_age(age=age)

        if verbose:
            print ""
            print "Filling data took {0} seconds.".format(time()-t0)
            print "Isochrone data created"

        return isoc_array

    def get_isochrone_masses(self, age, N = 5000):
        """

        """
        # Get possible stages
        phases = np.array(list(set(np.around(self.phase))), dtype=int)

        # Determine the mass of the beginning of each stage
        beg_mass = []
        for i in range(len(phases)):
            # Make the interpolation between age of the beginning of the stage
            # and mass
            x = self.age_beg_phase[:, i]
            y = self.M

            interp_fun = interp1d(x = x,
                                  y = y,
                                  bounds_error=False,
                                  fill_value=np.nan)

            # Include in the mass list the mass corresponding to this age
            beg_mass.append(interp_fun(age))

        beg_mass = np.array(beg_mass)

        # Remove the phases not covered by any mass in the Set
        phases = phases[~np.isnan(beg_mass)]

        # Remove nan's from beg_mass
        beg_mass = beg_mass[~np.isnan(beg_mass)]

        # Number of points by phase
        Ni = int(N/len(phases))
        Ni = np.array([Ni]*len(phases))

        # Add round-off points to first phase
        Ni[0] = Ni[0] + (N-Ni.sum())

        # Create array with isochrone
        isoc_mass = np.linspace(self.M[0], beg_mass[0], Ni[0])

        for i in range(1, len(phases)):
            isoc_mass = np.concatenate((isoc_mass,
                                        np.linspace(beg_mass[i-1],
                                                    beg_mass[i],
                                                    Ni[i])))
        return isoc_mass

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
                # # Try to get the phases from the first object in the list
                # try:
                #     self.phase = refEvTrack.phase
                #
                # except:
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
                # try:
                #     self.phase = refEvTrack.phase
                # except:
                try:
                    # Try to get default model phases
                    self.phase = default_interp_phase[self.model]
                    #print self.model
                    #print self.phase
                    #print default_interp_phase['PARSEC']

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

    def __add__(self, track):
        """
        
        :param track:
        :return:
        """
        # \Todo: this still needs to be tested
        
        # Only do something if the track's mass is not already present in the
        # Set
        if track.M not in self.M:
            
            # Checks if the track is compatible with the Set
            if track.Z != self.Z:
                raise ValueError(("Track metallicity does not match Set "
                                  "metallicity"))
    
            if track.model != self.model:
                raise ValueError("Track model does not match Set model")
            
            # Check if track contains all the columns necessary for the Set
            for column in self.columns:
                if column not in track.columns:
                    raise ValueError(("Not all columns in the Set are present "
                                      "in the Set."))
                
            # Remove additional columns from track
            track.simplify_array(columns = self.columns, return_EvTrack = False)
            
            # Normalize the track to fit Set's phases
            if track.phase != self.phase:
                track.interp_phase(phase=self.phase, return_EvTrack = False)
            
            # include track mass in self.M
            new_Set = copy.deepcopy(self)
            
            mass_list = copy.deepcopy(self.M)
            new_array = np.empty((self.array.shape[0]+1,
                                  self.array.shape[1],
                                  self.array.shape[2]))
            
            new_mass_list, new_id = get_new_mass_index(mass_list = mass_list,
                                                       new_mass = track.M)
            
            new_array[:new_id, :, :] = self.array[:new_id, :, :]
            new_array[new_id, :, :]  = track.array
            new_array[(new_id+1):, :, :] = self.array[new_id:, :, :]
            
            new_Set.M = new_mass_list
            new_Set.array = new_array
            
            return new_Set

    def include_HB(self, path, eta = 0.477):

        Z = self.Z

        if self.model == "PARSEC":
            # Get the masses for all HB models for this composition
            HB_M = utils.get_PARSEC_HB_masses(Z, path)

            # Selects phases for the HB models
            HB_start = 12
            HB_end = 16


        else:
            raise AttributeError(("The model {} is not supported by the "
                                  "include_HB method."))


        HB = ((self.phase >= HB_start) &
              (self.phase <= HB_end))

        HB_phases = self.phase[HB]

        # Load all HB tracks
        HBtracks = []
        for i in range(len(HB_M)):
            # Load HBtrack for mass M[i]
            HBtrack_i = EvTrack(mass=HB_M[i], Z=Z, path=path,
                                model=self.model, HB=True)

            HBtracks.append(HBtrack_i)

        # Create the EvTrack_MassSet for the HB
        HBtracks_Set = EvTrack_MassSet(EvTrack_list=HBtracks,
                                       phase=HB_phases,
                                       columns=self.columns)

        # Obtain interpolation of the HBtracks_Set
        HBtracks_interp_function = HBtracks_Set.get_interp_mass_function()

        # Select index of all self.M that can have HB included
        mass_index = np.array(range(len(self.M)))
        mass_index = mass_index[(self.M >= HB_M.min()) &
                                (self.M <= HB_M.max())]

        for i in mass_index:
            track_i = self[i]

            # Update RGB mass loss and get HB_init_mass
            HB_init_mass = track_i.rgb_mass_loss(eta = eta)
            if HB_init_mass is not None:

                HB_i_array = HBtracks_interp_function(HB_init_mass)

                # Include HB to track_i
                track_i.array[HB, :] = HB_i_array

                # Update self data
                self.array[i, :, :] = track_i.array
            else:
                continue


    def get_phase_completeness(self, proxy_column = 'log_Teff',
                               plot = False, show = False, **kwargs):
        """

        :param proxy: column that will be used to check if its value is present
                      for a given phase value.
        :return: a completeness array with lines representing different masses
                 and columns different phases. If the data is present for a
                 given mass and phase, its value in the array is True.
        """
        # Get proxy_column index
        N_cols = self.array.shape[2]
        column_names = np.array(self[0].column_names)
        proxy_column_id = np.arange(N_cols)[column_names == proxy_column]

        # Get completeness mask
        completeness_mask = ~np.isnan(self.array[:,:,proxy_column_id])

        if plot:
            N_lines = self.array.shape[1]
            for i in range(len(self.M)):
                mask = completeness_mask[i].reshape(1, N_lines)[0]
                x = self.phase[mask]
                y = np.array([self.M[i]]*N_lines)[mask]

                plt.plot(x,y,'o', **kwargs)

            if show:
                plt.show()

        return completeness_mask

class EvTrack_ZSet(object):
    """

    """

    def __init__(self, EvTrack_MassSet_list = None, Z = None, M = None,
                 phase = None, model = None, path = None, array = None,
                 columns = None, HB = False):
        """
        Initializes the EvTrack_ZSet. There are three possible ways to load
        EvTrack_ZSet. 1) By giving a list of EvTrack_MassSet objects. 2) By
        loading data from a file, specified by Z list, M list, model and path.
        3) By explicitly providing the whole data Z, M list, model, array,
        columns.
        """

        self.kind = "ZSet"

        # Fixing for the cases of single Z or single M
        Z = utils.array1d(Z) if (Z is not None) else None
        M = utils.array1d(M) if (M is not None) else None

        ########################################################################
        # Perform some tests to check if all necessary data is provided

        # Check the method used to load the data
        self.EvTrack_MassSet_list_is_provided = False
        self.array_is_provided = False
        self.load_info_is_provided = False

        # This will update the above booleans
        self._check_if_all_needed_info_is_given(EvTrack_MassSet_list=EvTrack_MassSet_list,
                                                Z=Z, M=M, phase=phase,
                                                model=model, path=path,
                                                array=array, columns=columns)

        if not any([self.EvTrack_MassSet_list_is_provided,
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
        self.phase = None  # Will be set by self._prepare_phase_parameter

        if self.EvTrack_MassSet_list_is_provided:

            # Get reference EvTrack
            refEvTrack_MassSet = EvTrack_MassSet_list[0]

            # self.Z is given by the reference object
            self.Z = []
            self.Y = []
            for evtrack_massset in EvTrack_MassSet_list:
                self.Z.append(evtrack_massset.Z)
                self.Y.append(evtrack_massset.Y)

            # self.M is a list containing the initial mass of each track for the
            # first mass set
            self.M = []
            for evtrack_massset_obj in refEvTrack_MassSet:
                self.M.append(evtrack_massset_obj.M)

            # self.model is given by the reference object
            self.model = refEvTrack_MassSet.model

            # if columns is None, get it from reference object
            if columns is None:
                self.columns = refEvTrack_MassSet.columns
            else:
                self.columns = columns

            # Get phase
            self.phase = refEvTrack_MassSet.phase

            # Generate self.array
            array = np.empty((len(self.Z), len(self.M),
                              len(self.phase), len(self.columns)))
            array[:] = np.nan

            # Fill the array
            for i in range(len(self.Z)):
                # Check if MassSet masses and phases are the same as self
                EvTrack_MassSet_tmp = EvTrack_MassSet_list[i]
                if list(EvTrack_MassSet_tmp.M) != list(self.M):
                    EvTrack_MassSet_tmp.interp_mass(self.M)
                if list(EvTrack_MassSet_tmp.phase) != list(self.phase):
                    EvTrack_MassSet_tmp.interp_phase(self.phase)

                array[i,:,:,:] = EvTrack_MassSet_tmp.array

            self.array = array


        elif self.load_info_is_provided:

            # Get reference EvTrack
            refEvTrack = EvTrack(mass=M[0], Z=Z[0], path=path, model=model)

            # self.Z is given by entry parameter
            self.Z = list(Z)
            self.Y = utils.abundanceY(Z)

            # self.M is given by entry parameter
            self.M = list(M)

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

            # Generate self.array
            array = np.empty((len(self.Z), len(self.M),
                              len(self.phase), len(self.columns)))
            array[:] = np.nan

            # Fill the array
            for i in range(len(self.Z)):
                # Check if MassSet masses and phases are the same as self
                EvTrack_MassSet_tmp = EvTrack_MassSet(Z = Z[i],
                                                      M = M,
                                                      model = model,
                                                      path = path)
                if list(EvTrack_MassSet_tmp.M) != list(self.M):
                    EvTrack_MassSet_tmp.interp_mass(self.M)
                if list(EvTrack_MassSet_tmp.phase) != list(self.phase):
                    EvTrack_MassSet_tmp.interp_phase(self.phase)

                array[i, :, :, :] = EvTrack_MassSet_tmp.array

            self.array = array

        elif self.array_is_provided:

            # self.Z is given by entry parameter
            self.Z = Z
            self.Y = utils.abundanceY(Z)

            # self.M is given by entry parameter
            self.M = M

            # self.model is given by entry parameter
            self.model = model

            # self.columns is given by entry parameter
            self.columns = np.array(columns)

            # phase is given by entry parameter, or taken from reference, or
            # taken from default value for model.
            self.phase = None
            self._prepare_phase_parameter(refEvTrack=None,
                                          phase=None, array=array,
                                          columns=self.columns)  # Sets self.phase.
            if self.phase is None:
                raise AttributeError("self.phase could not be attributed.")

            # Check if the shape of the array matches the given data
            array_error_message = ("The given array has a different number of "
                                 "dimensions compared to the number of {0} "
                                 "provided.")

            if array.shape[0] != len(Z):
                raise ValueError(array_error_message.format("Z"))

            if array.shape[1] != len(M):
                raise ValueError(array_error_message.format("masses"))

            if array.shape[2] != len(self.phase):
                raise ValueError(array_error_message.format("phases"))

            if array.shape[3] != len(columns):
                raise ValueError(array_error_message.format("columns"))

            self.array = array

        # Attribute that stores the Z interpolation when it
        # has already been calculated before.
        self._interp_Z_function = None

        # Transform M and Z to arrays
        self.M = utils.array1d(self.M)
        self.Z = utils.array1d(self.Z)

    def __getitem__(self, i):
        """
        self.__getitem__ returns the EvTrack_MassSet object which has mass
        self.Z[i]
        """

        #\todo check what needs to change for it to work with a single Z in
        # self.Z

        # Get the array for the EvTrack_MassSet
        array_i = self.array[i, :, :, :]

        # Create the evtrack_massset_i
        evtrack_massset_i = EvTrack_MassSet(Z = self.Z[i],
                                            M = self.M,
                                            model = self.model,
                                            columns = self.columns,
                                            array = array_i)

        # Return the EvTrack_MassSet object of Z = self.Z[i]
        return evtrack_massset_i

    def __iter__(self):
        """
        Iterates the set returning one EvTrack_Mass Set at a time
        """

        for i in range(len(self.Z)):
            evtrack_massset_i = self[i]
            yield evtrack_massset_i

    def interp_mass_and_phase(self, M, phase = None, new_object = False, **kargs):
        """
        Interpolates the evolutionary track set for the given list of masses M
        for each value of Z

        :param M: list of masses to interpolate

        also accepts any keyword argument for the function interp1d from the
        scipy.interpolate module
        """

        # If a new EvTrack Set is to be created, copy, evaluate and return it
        if new_object:
            new_set = copy.deepcopy(self)
            new_set.interp(M=M, phase=phase, new_object = False, **kargs)

            return new_set

        # Otherwise, only evaluate
        else:
            if phase is None:
                phase = self.phase

            # Create empty array to receive interpolated data
            interp_array = np.empty((self.array.shape[0],
                                     len(M),
                                     len(phase),
                                     self.array.shape[3]))

            # Perform interpolation for each value of Z and fill the array
            for i in range(len(self.Z)):

                # Get EvTrack_MassSet for the value of self.Z[i]
                evtrack_massset_i = self[i]

                # Interpolate this EvTrack_MassSet
                evtrack_massset_i.interp(M=M, phase=phase)

                # Write interpolated data to the created array
                interp_array[i, :, :, :] = evtrack_massset_i.array

            # Update self.array and self.M
            self.array = interp_array
            self.M = M

    def interp_Z(self, Z, new_object = False, record_interp_function = True,
                 **kargs):
        """
        Interpolates the evolutionary track set for the given list of masses M

        :param Z: list of masses to interpolate

        also accepts any keyword argument for the function interp1d from the
        scipy.interpolate module
        """

        # Controls if interpolation is actually necessary
        interpolate = True

        Z = utils.array1d(Z)

        # If a new EvTrack Set is to be created, copy, evaluate and return it
        if new_object:
            new_set = copy.deepcopy(self)
            new_set.interp_Z(Z=Z, new_object = False, **kargs)

            return new_set

        # Otherwise, only evaluate

        else:
            # First check if there is enough data to interpolate from.
            # And also check if data needs to be modified at all.
            if len(self.Z) == 1:
                if list(Z) == list(self.Z):
                    # The only data present is also the data wanted,
                    # in this case, nothing needs to be modified
                    interpolate = False
                else:
                    raise ValueError("This Set does not contain enough data "
                                     "to interpolate for this mass.")

            if interpolate:
                # If values asked for interpolation are already present
                # in the data, use them:
                if np.in1d(Z, self.Z).all():

                    # Even in this case, record the interpolate function
                    # if required
                    if record_interp_function:
                        self.interp_Z_function = interp1d(x=self.Z,
                                                          y=self.array,
                                                          axis=0,
                                                          bounds_error=False,
                                                          fill_value=np.nan,
                                                          **kargs)

                    self.array = self.array[np.in1d(self.Z, Z), :, :, :]
                    self.Z = Z

                else:
                    # If interpolation function is recorded, use it.
                    if self._interp_Z_function is not None:
                        self.array = self._interp_Z_function(Z)
                        self.Z = utils.array1d(Z)

                    else:
                        # Create the interpolation function
                        interp_function = interp1d(x=self.Z,
                                                   y=self.array,
                                                   axis=0,
                                                   bounds_error=False,
                                                   fill_value=np.nan,
                                                   **kargs)

                        self.array = interp_function(Z)
                        self.Z = utils.array1d(Z)

                        if record_interp_function:
                            self._interp_Z_function = interp_function


    def interp(self, Z, M = None, phase = None, new_object = False,
               record_interp_function=True, **kargs):
        """
        Interpolates the evolutionary track set for the given list of Z, M and
        phase

        :param phase: list of phases to interpolate
        :param M: list of masses to interpolate
        :param Z: list of Z to interpolate

        also accepts any keyword argument for the function interp1d from the
        scipy.interpolate module
        """

        # If a new EvTrack Set is to be created, copy, evaluate and return it
        if new_object:
            new_set = copy.deepcopy(self)
            new_set.interp(Z=Z, M=M, phase=phase, new_object=False, **kargs)

            return new_set

        else:
            # First prepare input variables
            Z = self.Z if (Z is None) else utils.array1d(Z)
            M = self.M if (M is None) else utils.array1d(M)
            phase = self.phase if (phase is None) else np.array(phase)

            # Interpolate mass and phase if necessary
            if np.array_equal(M,self.M) or np.array_equal(phase,self.phase):
                self.interp_mass_and_phase(M=M,
                                           phase=phase,
                                           new_object=False, **kargs)
                # if Mass and phase are interpolated, reset Z interp function
                self.interp_Z_function = None

            # Then interpolate Z
            self.interp_Z(Z, new_object = False,
                             record_interp_function=record_interp_function,
                             **kargs)

    def plot(self, xcol, ycol, Z = None, M = None, phase = None,
             Zcolor = None, **kargs):
        """
        """

        Z = self.Z if (Z is None) else utils.array1d(Z)

        # Create new evtrack with only the data chosen for ploting:
        evtrack_zset_plot = self.interp(Z = Z, M = M,
                                        phase = phase,
                                        new_object=True)

        # Plot
        if Zcolor is not None:
            for ev_track_massset_i, col_i in zip(evtrack_zset_plot, Zcolor):
                ev_track_massset_i.plot(xcol=xcol, ycol=ycol, color = col_i,
                                    **kargs)
        else:
            for ev_track_massset_i in evtrack_zset_plot:
                ev_track_massset_i.plot(xcol=xcol, ycol=ycol, **kargs)


    def make_isoc(self, age, Z, N = 5000, isoc_columns = None, verbose = False):
        """

        :param age: float
        :param Z: float
        :return:
        """
        # \todo write test for this

        # If self.array contains data for the given Z
        ev_track_mass_set = self[self.Z == Z]

        # If self.array does not contain data fot the given Z
        # \todo fix problems for single Z in self.Z for yesterday!!!!!!!!
        # \todo it will allow the change of Z=[Z, self.Z[0]] to Z=Z
        ev_track_mass_set = self.interp(Z=Z)[0]

        isoc_array = ev_track_mass_set.make_isochrone(age=age,
                                                      N=N,
                                                      isoc_columns=isoc_columns,
                                                      verbose=verbose)

        return isoc_array

    def simplify_array(self, columns, return_object = True):
        """

        :param columns:
        :param return_object:
        :return:
        """

        #\todo Write the test for this method

        # Use recursivity if the user desires to return a new EvTrack_MassSet
        # object with the simplified array
        if return_object:
            new_set = copy.deepcopy(self)
            new_set.simplify_array(columns, return_object=False)

            return new_set

        else:
            # Update self.columns
            etcol_type = etcol.Ev_track_column
            if all(isinstance(obj, etcol_type) for obj in columns):
                columns = utils.etcolobjs2colnames(columns)

            # Create new self.array
            new_array = np.empty((len(self.Z),
                                  len(self.M),
                                  len(self.phase),
                                  len(columns)))
            new_array[:] = np.nan

            # Update self.array with simplified data
            for i in range(len(self)):
                temp_mass_set = copy.deepcopy(self[i])
                temp_mass_set.simplify_array(columns=columns,
                                       return_object=False)

                # Fill the array
                new_array[i,:,:,:] = temp_mass_set.array

            # Update self.array and self.columns
            self.array = new_array
            self.columns = columns

    def _check_if_all_needed_info_is_given(self, EvTrack_MassSet_list = None,
                                           Z = None, M = None, phase = None,
                                           model = None, path = None,
                                           array = None, columns = None):

        """
        Used internally to check if the user provided all the necessary data to
        initialize the array from any of the given methods.
        """

        EvTrack_MassSet_list_is_provided = False
        array_is_provided = False
        load_info_is_provided = False

        # Check if EvTrack_MassSet_list is provided and if it is a list
        if EvTrack_MassSet_list is not None:
            if utils.isiterable(EvTrack_MassSet_list):
                EvTrack_MassSet_list_is_provided = True
            else:
                raise ValueError("if provided, EvTrack_MassSet_list must be a list of"
                                 "EvTrack_MassSet objects")

        # If EvTrack_list is provided, check if unnecessary data was
        # also given by the user:
        if EvTrack_MassSet_list_is_provided:
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
            if array.shape[0] != len(Z):
                raise ValueError(("The number of provided compositions in list Z "
                                  "({0}) does not agree with the size of the "
                                  "dimension 0 of the given array ({1})"
                                  ".").format(len(Z), array.shape[0]))

            if array.shape[1] != len(M):
                raise ValueError(("The number of provided masses in list M "
                                  "({0}) does not agree with the size of the "
                                  "dimension 1 of the given array ({1})"
                                  ".").format(len(M), array.shape[1]))

            if array.shape[3] != len(columns):
                raise ValueError(("The number of provided columns "
                                  "({0}) does not agree with the size of the "
                                  "dimension 3 of the given array ({1})"
                                  ".").format(len(columns), array.shape[3]))

        # If neither array, nor EvTrack objects are provided, check if all the
        # information to load from a file is provided
        if not any([EvTrack_MassSet_list_is_provided, array_is_provided]):
            param_dict = {'Z': Z, 'M': M, 'model': model, 'path': path}

            for param in param_dict.keys():
                if param_dict[param] is None:
                    raise ValueError(("When loading data from files, "
                                      "parameter {0} must be assigned"
                                      ".").format(param))

            # If it gets here
            load_info_is_provided = True

        self.EvTrack_MassSet_list_is_provided = EvTrack_MassSet_list_is_provided
        self.array_is_provided = array_is_provided
        self.load_info_is_provided = load_info_is_provided

    def _prepare_phase_parameter(self, refEvTrack=None, phase=None,
                                 array=None, columns=None):
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
            if self.EvTrack_MassSet_list_is_provided:
                # # Try to get the phases from the first object in the list
                # try:
                #     self.phase = refEvTrack.phase
                #
                # except:
                try:
                    # Try to get default model phases
                    self.phase = default_interp_phase[self.model]

                except:
                    raise ValueError("Could not assign phase attribute.")

            elif self.array_is_provided:
                # Try to get the phases from the first object in the array
                try:
                    self.phase = array[0, 0, :, columns == 'phase'][0]
                except:
                    try:
                        # Try to get default model phases
                        self.phase = default_interp_phase[self.model]

                    except:
                        raise ValueError("Could not assign phase attribute.")

            elif self.load_info_is_provided:
                # try:
                #     self.phase = refEvTrack.phase
                # except:
                try:
                    # Try to get default model phases
                    self.phase = default_interp_phase[self.model]
                except:
                    raise ValueError("Could not assign phase attribute.")
        ########################################################################

#\TODO move this class to Isochrone.py
class Isochrone(object):
    # \TODO expand this docstring
    """

    """

    def __init__(self, age = None, Z = None, model='Not_Assigned', path=None,
                 array=None, columns=None):

        # Check if given model is supported in this version of eitapy
        if model not in load.allowed_models:
            raise ValueError(("{0} is not a supported file format.\n"
                              "Supported formats are {0}."
                              "").format(load.allowed_models))

        # Load EvTrack according to the file format
        Isochrone = None

        IsochroneData = load.LoadedIsochrone(age=age,
                                             Z=Z,
                                             model=model,
                                             path=path,
                                             array=array,
                                             columns=columns
                                             )

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


def save(self):
        # \TODO implement
        pass
    

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

    return new_mass_list, index
    
def get_PARSEC_HB_masses(Z, path):
    """
    
    :param Z:
    :param path:
    :return:
    """
    
    Y = utils.abundanceY(Z)
    fullpath = path + '/' + utils.parsec_directory(Z,Y)
    
    filenames = os.listdir(fullpath)
    
    HB_files = []
    for filename in range(len(filenames)):
        if 'HB' in filename:
            HB_files.append(filename)
    
    M = []
    # The mass in the filename is what comes after M and before .HB, so:
    for HB_file in HB_files:
        M.append(float(HB_file.split('M')[1].split('.HB')[0]))
    
    return M