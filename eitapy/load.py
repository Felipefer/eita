__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"

"""
load.py contains the functions used to load evolutionary tracks and isochrones
"""

import numpy as np
import utils
import ev_track_columns as etcol

# New version is set to allow it to load from an existing array. Column_names
# must be provided

################################################################################

allowed_models = ['PARSEC', 'PARSEC_ISOC_1_2']

_columns_parsec = [etcol.mass, etcol.age, etcol.log_L, etcol.log_Teff,
                   etcol.log_R, etcol.mdot, etcol.he_core_mass,
                   etcol.c_core_mass, etcol.center_H, etcol.center_He,
                   etcol.center_C, etcol.center_O, etcol.LH_frac,
                   etcol.LHe_frac, etcol.LC_frac, etcol.LNeutr_frac,
                   etcol.Lgrav_frac, etcol.surf_H, etcol.surf_He, etcol.surf_C,
                   etcol.surf_N, etcol.surf_O, etcol.phase]

_columns = {}

_columns["PARSEC"] = [etcol.mass, etcol.age, etcol.log_L, etcol.log_Teff,
                      etcol.log_R, etcol.mdot, etcol.he_core_mass,
                      etcol.c_core_mass, etcol.center_H, etcol.center_He,
                      etcol.center_C, etcol.center_O, etcol.LH_frac,
                      etcol.LHe_frac, etcol.LC_frac, etcol.LNeutr_frac,
                      etcol.Lgrav_frac, etcol.surf_H, etcol.surf_He,
                      etcol.surf_C, etcol.surf_N, etcol.surf_O, etcol.phase]

_columns["PARSEC_ISOC_1_2"] = [etcol.Z, etcol.log_age, etcol.initial_mass,
                               etcol.mass, etcol.log_L, etcol.log_Teff,
                               etcol.log_g, etcol.mag_bol, etcol.magU,
                               etcol.magB, etcol.magV, etcol.magR, etcol.magI,
                               etcol.magJ, etcol.magH, etcol.magK,
                               etcol.int_IMF, etcol.phase]

_columns["MESA"] = []

_columns["YALE"] = []

class LoadedEvolutionaryTrack(object):
    """
    Contains the data of an evolutionary track file and is used to initiate an 
    object of the class Ev_Track
    """
    
    def __init__(self, mass, Z, model = "Not_Assigned",
                 auto_load = True, path = None, array = None,
                 columns = None, HB = False):
        """
        :param model: Ev_Track model
        """
        
        self.loaded = False
        
        self.mass = mass
        self.Z    = Z
        
        # Calculate Helium abundances
        self.Y = np.around(utils.abundanceY(Z), 3)
        
        self.model = model

        if auto_load:
            self.load(path=path, array=array, columns=columns, HB=HB)
        
    def load(self, path = None, array = None, columns = None, HB = False):
        """
        loads data from path or array to loaded_evolutionary_track
        
        :param path    : path leading to the file containing the data
        :param array   : array containing the data
        :param columns : list of etcol.Ev_track_column objects in the
                         correct order of the array columns
        """
        # Check if user is using this function correctly. It has two options,
        # load from a file in "path" OR load from an array
        if path is not None:
            if array is not None:
                raise ValueError(("the array should not be given when the "
                                  "path to the data is already provided"))

        # Use defaults or check if user provided columns as it must be.
        if array is not None:
            if columns is None:
                columns = _columns[self.model]
            else:
                if len(columns) != array.shape[1]:
                    raise ValueError(("columns must be a list of "
                                      "etcol.Ev_track_column objects in the "
                                      "correct order of the array columns"))

            # If columns are given as strings, turn them to the corresponding
            # etcol.Ev_track_column object
            for i in range(len(columns)):
                col = columns[i]
                if isinstance(col, str):
                    try:
                        # etcol.columns is a dictionary where the keys are the
                        # columns names and the values are the objects of type
                        # etcol.Ev_track_column
                        columns[i] = etcol.columns[col]

                    except KeyError:
                        raise ValueError(("Column name {0} is not supported. "
                                          "Supported columns are {1}"
                                          ".").format(col,
                                                      etcol.columns.keys()))


        if self.loaded:
           raise Warning(("Already loaded with "
                        "{0} set").format(self.model))

        if path is not None:
            self._load_from_file(path=path, HB=HB)
            self.loaded = True

        elif array is not None:
            self._load_from_array(array, columns)
            self.loaded = True

    def _load_from_array(self, track_data, columns):
        """
        used internally to load evolutionary track from an array

        :param ev_track_data: array containing the data
        :param columns      : list of etcol.Ev_track_column objects in the
                              correct order of the array columns
        """

        model = self.model

        self.column_names = []
        self.column_fmt = {}

        # Loading columns data as attributes
        for i in range(len(columns)):
            col = columns[i]
            value = track_data[:, i]
            self.__setattr__(col.name, value)
            self.column_names.append(col.name)

            # Prepare fmt for file saving methods
            # first try parsec specific fmt, then col fmt
            # and if none is attributed, use a default value
            try:
                self.column_fmt[col.name] = col.model[model]["fmt"]
            except KeyError:
                try:
                    self.column_fmt[col.name] = col.fmt
                except AttributeError:
                    self.column_fmt[col.name] = "% 9.5f"

    def _load_from_file(self, path, HB=False):
        """
        used internally to load one of the standard models. Should generalize
        previous _load_model functions and make them obsolete.
        """
        model = self.model

        # Get full filename depending on the model
        filepath = self._get_full_filepath(model=model, path=path, HB=HB)

        # Load model file into ev_track_data
        # \todo check what to do with skiprows
        track_data = np.loadtxt(filepath, skiprows=1)

        # Columns that are present in the PARSEC tracks
        columns = _columns[model]

        self.column_names = []
        self.column_fmt = {}

        # Loading columns data as attributes
        for col in columns:
            value = track_data[:, col.model[model]["id"]]
            self.__setattr__(col.name, value)
            self.column_names.append(col.name)

            # Prepare fmt for file saving methods
            # first try model specific fmt, then col fmt
            # and if none is attributed, use a default value
            try:
                self.column_fmt[col.name] = col.model[model]["fmt"]
            except KeyError:
                try:
                    self.column_fmt[col.name] = col.fmt
                except AttributeError:
                    self.column_fmt[col.name] = "% 9.5f"

        # Fix PARSEC phases
        if HB:
            if model == "PARSEC":
                if self.column_names[-1] == 'phase':
                    track_data[:,-1] = track_data[:,-1]+11

    def _get_full_filepath(self, model, path, filename = None, HB=False):
        """
        used internally. Returns filepath (path + directory + filename) for each
        model
        """
        if model == "PARSEC":
            filename = utils.parsec_filename(path = path,
                                             Z = self.Z,
                                             Y = self.Y,
                                             mass=self.mass,
                                             HB=HB)

            directory = utils.parsec_directory(Z=self.Z,
                                         Y=self.Y)

            filepath = path + '/' + directory + '/' + filename
            return filepath

        elif model == "PARSEC_ISOC_1_2":
            if filename is None:
                filename = utils.parsec_isoc_filename(Z = self.Z,
                                                      age = self.age)
            filepath = path + '/' + filename
            return filepath

        elif model == "MESA":
            pass

        elif model == "YALE":
            pass

    def _load_parsec(self, path):
        # Obsolete

        """
        used internally to load parsec data format
        """
        
        filename  = utils.parsec_filename(path = path,
                                          Z = self.Z,
                                          Y = self.Y,
                                          mass = self.mass)
        
        directory = utils.parsec_directory(Z   = self.Z,
                                           Y   = self.Y)
        
        self.filename = directory+'/'+filename
        
        # Load PARSEC file into ev_track_data
        ev_track_data = np.loadtxt(path+'/'+self.filename, skiprows = 1)
        
        # Columns that are present in the PARSEC tracks
        columns = _columns_parsec

        self.column_names = []
        self.column_fmt   = {}

        # Loading columns data as attributes
        for col in columns:
            value = ev_track_data[:, col.PARSEC_col_id]
            self.__setattr__(col.name, value)
            self.column_names.append(col.name)

            # Prepare fmt for file saving methods
            # first try parsec specific fmt, then col fmt
            # and if none is attributed, use a default value
            try:
                self.column_fmt[col.name] = col.PARSEC_col_fmt
            except AttributeError:
                try:
                    self.column_fmt[col.name] = col.fmt
                except AttributeError:
                    self.column_fmt[col.name] = "% 9.5f"


class LoadedIsochrone(LoadedEvolutionaryTrack):
    """
    The class used to load Isochrones inherits the methods of the
    LoadedEvolutionaryTrack class. This is made possible because both data
    are very similar. The only change is that the initial mass is the quantity
    conserved in an evolutionary track, while in an Isochrone it's the age that
    is the same for all points.
    """

    def __init__(self, age, Z, model = "Not_Assigned",
                 auto_load = True, path = None, array = None,
                 columns = None):
        """
        :param model: Isochrone model
        """

        self.loaded = False

        self.age = age
        self.Z = Z

        # Calculate Helium abundances
        self.Y = np.around(utils.abundanceY(Z), 3)

        self.model = model

        if auto_load:
            self.load(path=path, array=array, columns=columns)

################################################################################

# def parsec_filename(Z, Y, mass, HB = False):
#     """
#     Get default name for PARSEC evolutionary tracks with mass M, and
#     compositions Y, Z
#     """
#
#     Z_fmt = str(Z)
#     Y_fmt = str(Y)
#     OUTA = '1.77' if mass <= 0.7 else '1.74'
#
#     if HB:
#         return "Z{:s}Y{:s}OUTA{:s}_F7_M{:05.3f}.HB.DAT".format(Z_fmt, Y_fmt,
#                                                                OUTA, mass)
#
#     else:
#         return "Z{:s}Y{:s}OUTA{:s}_F7_M{:07.3f}.DAT".format(Z_fmt, Y_fmt,
#                                                             OUTA,  mass)
#
#
# def parsec_directory(Z, Y):
#     """
#     Get the default PARSEC name for the folder containing data for composition
#     Y, Z.
#     """
#
#     Z_fmt = str(Z)
#     Y_fmt = str(Y)
#
#     return "Z{:s}Y{:s}".format(Z_fmt, Y_fmt)
