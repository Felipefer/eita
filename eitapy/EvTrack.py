__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "June 2017"

#\TODO expand this docstring
"""
EvTrack.py contains the functions used to work with evolutionary tracks
"""

import copy
import ev_track_columns as etcol
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from time import time
import config
import sys
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
        remove_common_phases_from_self = ((self.phase < evtrack.phase.min()) &
                                          (self.phase > evtrack.phase.max()))

        phase0 = self.phase[remove_common_phases_from_self]
        array0 = self.array[remove_common_phases_from_self]

        # Concatenate both data
        phase = np.concatenate((phase0, evtrack.phase))
        array = np.concatenate((array0, evtrack.array))

        # Order the data
        argsort = phase.argsort()
        array = array[argsort, :]

        # Update self data
        self.array = array
        self._update_colname_attributes()

        return self


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
                self.array = np.empty((1, array.shape[0], array.shape[1]))
                self.array[0, :, :] = array
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

            self.columns = columns

            # Create new self.array
            self.array = np.empty((len(self.M),
                                   len(self.phase),
                                   len(self.columns)))
            self.array[:] = np.nan

            # Update self.array with simplified data
            for i in range(len(self)):
                track_temp = self[i].simplify_array(columns = columns,
                                                    return_EvTrack= True)

                self.array[i, :, :] = track_temp.array

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

    def interp_mass(self, M = None, new_object = False,
                    record_interp_function = True, **kargs):
        """
        Interpolates the evolutionary track set for the given list of masses M

        :param M: list of masses to interpolate

        also accepts any keyword argument for the function interp1d from the
        scipy.interpolate module
        """

        # If a new EvTrack Set is to be created, copy, evaluate and return it
        if new_object:
            new_set = copy.deepcopy(self)
            new_set.interp_mass(M=M, new_object = False, **kargs)

            return new_set

        # Otherwise, only evaluate
        else:
            # If interpolation function is recorded, use it.
            if self._interp_mass_function is not None:
                if M is not None:
                    self.array = self._interp_mass_function(M)
                    self.M = M

            else:
                # Create the interpolation function
                interp_function = interp1d(x=self.M,
                                           y=self.array,
                                           axis=0,
                                           **kargs)

                if M is not None:
                    self.array = interp_function(M)
                    self.M = M

                if record_interp_function:
                    self._interp_mass_function = interp_function

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
                                                 bounds_error=False)

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
                print "Isoc_columns set as self.columns."

        else:
            # if isoc_columns given as name strings, trasform to etcol objects
            if all(isinstance(name, str) for name in isoc_columns):
                isoc_columns = utils.colnames2etcolobjs(isoc_columns)

            if verbose:
                print "Simplifying data array to contain only given columns."
                t0 = time()
            Set_for_interp = self.simplify_array(columns = isoc_columns,
                                                 return_object= True)
            if verbose:
                print "Simplifying took {0} seconds.".format(time()-t0)

        if verbose:
            print "Estimating masses necessary to sample the isochrone."
            t0 = time()
        isoc_masses = self.get_isochrone_masses(age=age, N=N)

        if verbose:
            print "Estimating {0} masses took {1} seconds.".format(N, time()-t0)

        if verbose:
            print "Obtaining interpolation coeficients"
            t0 = time()
        # Update Set_for_interp
        Set_for_interp.interp_mass(M=None, new_object=False,
                                   record_interp_function=True)

        if verbose:
            print "Obtaining coeficients took {0} seconds.".format(time()-t0)

        # Generate isochrone array
        if verbose:
            print "Preparing isochrone array"
        isoc_array = np.empty((N, len(isoc_columns)))
        isoc_array[:] = np.nan

        if verbose:
            print "Empty array of shape {0} created.".format(isoc_array.shape)

        if verbose:
            print "Filling isochrone array"

        for i in range(N):
            if verbose:
                t0 = time()
                pct = (i/float(N)) *100
                print "{:6.2f}%".format(pct)
                sys.stdout.flush()

            track_temp = Set_for_interp.interp_mass(M = isoc_masses[i],
                                                    new_object=True)
            track_temp = Set_for_interp[0]

            isoc_array[i,:] = track_temp.interp_age(age=age,
                                                    columns=isoc_columns)

        if verbose:
            print ""
            print "Filling data took {0} seconds.".format(time()-t0)
            print "Isochrone data created"

        return isoc_columns

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
                                  bounds_error=False)

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

    def save(self):
        # \TODO implement
        pass

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
