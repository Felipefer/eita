"""
Contains common used functions necessary for different modules
"""

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
    pass

def etcolobjs2colnames(etcolobjs):
    pass
