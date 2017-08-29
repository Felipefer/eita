"""
Contains common used functions necessary for different modules
"""

import ev_track_columns as etcol

def abundanceY(Z):
    """
    Return Y abundance for a given Z abundance.
    :param Z: metallicity
    :return: Y abundance scaled for a given metallicity Z.
    """
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


def parsec_filename(Z, Y, mass, HB = False):
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


def parsec_directory(Z, Y):
    """
    Get the default PARSEC name for the folder containing data for composition
    Y, Z.
    """
    
    Z_fmt = str(Z)
    Y_fmt = str(Y)
    
    return "Z{:s}Y{:s}".format(Z_fmt, Y_fmt)