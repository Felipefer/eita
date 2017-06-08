"""
load.py contains the functions used to load evolutionary tracks and isochrones
"""

import numpy as np
import utils
import ev_track_columns as etcol

################################################################################


class LoadedEvolutionaryTrack(object):
    """
    Contains the data of an evolutionary track file and is used to initiate an 
    object of the class Ev_Track
    """
    
    def __init__(self, mass, Z, file_format = 'PARSEC'):
        """
        param file_format: format used in the evolutionary track file
        """
        
        self.loaded = False
        
        self.mass = mass
        self.Z    = Z
        
        # Calculate Helium abundances
        self.Y = utils.abundanceY(Z)
        
        self.file_format = file_format

    def load(self, path):
        """
        loads data from path to loaded_evolutionary_track
        
        param path: path leading to the file containing the data
        """
        
        if self.file_format == 'PARSEC':
            self._load_parsec(path)
    
    def _load_parsec(self, path):
        """
        used internally to load parsec data format
        """
        
        filename  = parsec_filename(Z    = self.Z,
                                    Y    = self.Y,
                                    mass = self.mass)
        
        directory = parsec_directory(Z   = self.Z,
                                     Y   = self.Y)
        
        self.filename = directory+'/'+filename
        
        # Load PARSEC file into ev_track_data
        ev_track_data = np.loadtxt(path+'/'+filename, skiprows = 1)
        
        # Columns that are present in the PARSEC tracks
        columns = [etcol.mass, etcol.age, etcol.log_L, etcol.log_Teff,
                   etcol.log_R, etcol.mdot, etcol.he_core_mass,
                   etcol.c_core_mass, etcol.center_H, etcol.center_He,
                   etcol.center_C, etcol.center_O, etcol.LH_frac,
                   etcol.LHe_frac, etcol.LC_frac, etcol.LNeutr_frac,
                   etcol.Lgrav_frac, etcol.surf_H, etcol.surf_He, etcol.surf_C,
                   etcol.surf_N, etcol.surf_O, etcol.phase]
        
        self.column_names = []
        
        # Loading columns data as attributes
        for col in columns:
            value = ev_track_data[:, col.PARSEC_col_id]
            self.__setattr__(col.name, value)
            self.column_names.append(col.name)

################################################################################

def parsec_filename(Z, Y, mass):
    """
    Get default name for PARSEC evolutionary tracks with mass M, and 
    compositions Y, Z
    """
    
    Z_fmt = str(Z)
    Y_fmt = str(Y)
    OUTA = '1.77' if mass <= 0.7 else '1.74'
    
    return "Z{:s}Y{:s}OUTA{:s}_F7_M{:07.3f}.DAT".format(Z_fmt, Y_fmt,
                                                        OUTA,  mass)


def parsec_directory(Z, Y):
    """
    Get the default PARSEC name for the folder containing data for composition 
    Y, Z.
    """
    
    Z_fmt = str(Z)
    Y_fmt = str(Y)
    
    return "Z{:s}Y{:s}".format(Z_fmt, Y_fmt)
