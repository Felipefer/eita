"""
load.py contains the functions used to load evolutionary tracks and isochrones
"""

import utils

################################################################################

class loaded_evolutionary_track(object):
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
        self.Y    = utils.abundanceY(Z)
        
        self.file_format = file_format
    
    
    def load(self, path):
        """
        loads data from path to loaded_evolutionary_track
        
        param path: path leading to the file containing the data
        """
        
        if self.file_format == 'PARSEC':
            self._load_parsec(self)
    
    
    def _load_parsec(self):
        """
        used internally to load parsec data format
        """
        
        filename  = PARSEC_filename(Z    = self.Z, 
                                    Y    = self.Y, 
                                    mass = self.mass)
        
        directory = PARSEC_directory(Z   = self.Z, 
                                     Y   = self.Y)
        
        self.filename = directory+'/'+filename
        
        
################################################################################

def PARSEC_filename(Z, Y, mass):
    """
    Get default name for PARSEC evolutionary tracks with mass M, and 
    compositions Y, Z
    """
    
    Z_fmt = str(Z)
    Y_fmt = str(Y)
    OUTA = '1.77' if mass <= 0.7 else '1.74'
    
    return "Z{:s}Y{:s}OUTA{:s}_F7_M{:07.3f}.DAT".format(Z_fmt, Y_fmt, 
                                                        OUTA,  mass)


def PARSEC_directory(Z, Y):
    """
    Get the default PARSEC name for the folder containing data for composition 
    Y, Z.
    """
    
    Z_fmt = str(Z)
    Y_fmt = str(Y)
    
    return "Z{:s}Y{:s}".format(Z_fmt,Y_fmt)

