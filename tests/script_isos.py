import sys
sys.path.insert(0, '../eitapy')

import Models
import Star
import func as fc
from time import time
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os

# Data Columns should be:
# id RAJ2000 DEJ2000 d d_err Av Av_err U U_err F378 F378_err F395 F395_err....
# or the same, but with Gaia magnitudes

# Load table
filepath = '' # Path to the data file
data = pd.read_csv(filepath, delim_whitespace = True, comment = '#')

# Load model
model_filepath = '' # path to the model file
model = Models.load_model(filepath=model_filepathfilepath, model='PARSEC',
                          delim_whitespace = True, comment = '#')

# Calculate absolute magnitudes
mag_list = ['uJAVA', 'F378', 'F395', 'F410', 'F430', 'gSDSS', 'F515', 'rSDSS',
            'F660', 'iSDSS', 'F861', 'zSDSS']

l_list = [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
          1.00, 1.00]

# Check if absolute magnitudes are already estimated
if 'uJAVAmag' in data.
    calculate_mabs = False
else:
    calculate_mabs = True

# Calculate corrected absolute magnitudes and its errors
if calculate_mabs:
    for mag, l in zip(mag_list, l_list):
        Al = l*data['Av']
        Al_err = l*data['Av_err']

        mag_obs = data[mag]
        mag_obs_err = data[mag+'_err']

        mag_abs = np.empty(len(mag))
        mag_abs_err = np.empty(len(mag))

        for i in range(len(mag_obs)):
            mag_abs[i], mag_abs_err[i] = get_Mabs(mag_apr = mag_obs[i],
                                                  mag_apr_err = mag_obs_err[i],
                                                  dist = data['dist'][i],
                                                  dist_err = data['dist_err'][i],
                                                  A = Al[i],
                                                  A_err = Al_err[i],
                                                  N = 1000)

        data[mag+'mag'] = mag_abs
        data[mag+'mag_err'] = mag_abs_err

    # Save df to a file
    #
    #
    #
    #
    #
    #


# Characterize each star
#
#
#
#
#

# Save params to file
#
#
#
#
#
#

