__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "June 2017"

#\TODO expand this docstring
"""
EvTrack.py contains the functions used to work with evolutionary tracks
"""

import numpy as np
import utils
import load

class EvTrack(object):
    #\TODO expand this docstring
    """
    
    """
    
    def __init__(self, mass, Z, path, file_format = 'PARSEC'):
        
        # Check if given file_format is supported in this version of eitapy
        if file_format not in load._allowed_file_formats:
            raise ValueError(("{0} is not a supported file format.\n"
                              "Supported formats are {0}."
                              "").format(load._allowed_file_formats))
        
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
        
        # Fill the array and point the attributes to it:
        for i in range(self.Ncols):
            
            column = self.column_names[i]
            
            self.array[:,i] = getattr(EvTrackData, column)
            setattr(self, column, self.array[:,i])