"""
Contains common used functions necessary for different modules
"""

import numpy as np
import ev_track_columns as etcol
import os

def abundanceY(Z):
    """
    Return Y abundance for a given Z abundance.
    :param Z: metallicity
    :return: Y abundance scaled for a given metallicity Z.
    """
    if type(Z) is list:
        Z = np.array(Z)

    return 0.2485 + 1.78*Z

def isiterable(x):
    """
    Checks if x is an iterable object

    :param x: object to check if its iterable
    :return: boolean
    """

    if hasattr(x, '__iter__'):
        return True
    else:
        return False


def colnames2etcolobjs(colnames):
    etcols_list = []

    for name in colnames:
        etcols_list.append(etcol.columns[name])

    return etcols_list

def etcolobjs2colnames(etcolobjs):
    colnames_list = []

    for etcolobj in etcolobjs:
        colnames_list.append(etcolobj.name)

    return colnames_list

def parsec_filename_old(Z, Y, mass, HB = False):
    """
    Get default name for PARSEC evolutionary tracks with mass M, and
    compositions Y, Z
    """
    Z_fmt = str(Z)
    Y_fmt = str(Y)
    OUTA = '1.77' if mass <= 0.7 else '1.74'

    if HB:
        return "Z{:s}Y{:s}OUTA{:s}_F7_M{:05.3f}.HB.DAT".format(Z_fmt, Y_fmt,
                                                               OUTA, mass)

    else:
        return "Z{:s}Y{:s}OUTA{:s}_F7_M{:07.3f}.DAT".format(Z_fmt, Y_fmt,
                                                            OUTA, mass)

def parsec_filename(path, Z, Y, mass, HB = False):
    """
    Get default name for PARSEC evolutionary tracks with mass M, and
    compositions Y, Z
    """
    fullpath = path + "/" + parsec_directory(Z,Y)
    filenames = os.listdir(fullpath)

    for filename in filenames:
        if HB:
            Mstr = 'M{:05.3f}'.format(mass)
            if Mstr in filename:
                return filename
        else:
            Mstr = 'M{:07.3f}'.format(mass)
            if Mstr in filename:
                return filename

    return None

def parsec_isoc_filename(Z, age):
    Z_value = "{:7.5f}".format(Z)[2:]
    t_value = "{:6.3f}".format(age/1e9)

    # Remove possible empty " "
    t_value = t_value.split(" ")
    try:
        t_value.remove("")
    except ValueError:
        pass

    t_value = "".join(t_value)

    return "PARSEC_Z{0}t{1}e9.dat".format(Z_value, t_value)

def parsec_directory(Z, Y):
    """
    Get the default PARSEC name for the folder containing data for composition
    Y, Z.
    """
    
    Z_fmt = str(Z)
    Y_fmt = str(round(Y,3))
    
    return "Z{:s}Y{:s}".format(Z_fmt, Y_fmt)


def get_PARSEC_masses(Z, path):
    """

    :param Z:
    :param path:
    :return:
    """

    Y = abundanceY(Z)
    fullpath = path + '/' + parsec_directory(Z,Y)

    filenames = os.listdir(fullpath)

    files = []
    for filename in filenames:
        if 'HB' not in filename:
            files.append(filename)

    M = []
    # The mass in the filename is what comes after M and before .HB, so:
    for file in files:
        M.append(float(file.split('M')[1][:7]))

    # Sorting masses
    M.sort()

    # Converting to array
    M = np.array(M)

    return M


def get_PARSEC_HB_masses(Z, path):
    """

    :param Z:
    :param path:
    :return:
    """

    Y = abundanceY(Z)
    fullpath = path + '/' + parsec_directory(Z,Y)

    filenames = os.listdir(fullpath)

    HB_files = []
    for filename in filenames:
        if 'HB' in filename:
            HB_files.append(filename)

    M = []
    # The mass in the filename is what comes after M and before .HB, so:
    for HB_file in HB_files:
        M.append(float(HB_file.split('M')[1].split('.HB')[0]))

    # Sorting masses
    M.sort()

    # Converting to array
    M = np.array(M)

    return M

################################################################################
# Custom errors to raise

class LoadingError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)