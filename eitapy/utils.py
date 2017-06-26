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

