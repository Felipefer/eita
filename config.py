import os
import warnings

"""
Sets up default parameters
"""

__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "June 2017"

# Get user's eitapy path
config_file_path = os.path.realpath(__file__)
eitapy_path = "/".join(config_file_path.split('/')[:-1])

# Default folders to save files ################################################

default_evtrack_save_folder = eitapy_path+"/evtracks"
default_isoc_save_folder    = eitapy_path+"/isocs"
default_plot_save_folder    = eitapy_path+"/plots"

# If the folders don't exist, try to create it

warn = False # Used if the user must be warned of something
for folder in (default_evtrack_save_folder,
               default_isoc_save_folder,
               default_plot_save_folder):
    
    # Folder exists?
    exist = os.path.isdir(folder)

    if exist:
        continue
    
    else: # Try to create it
        try:
            os.makedirs(folder)
            warn = True
        except:
            raise Warning(("{0} does not exist, "
                           "and could not be created").format(folder))
        if warn:
            warn_message = ("For some reason, default folder {0} "
                            "was not present. It was created to "
                            "avoid errors").format(folder)
            warnings.warn(warn_message)
            warn = False
################################################################################