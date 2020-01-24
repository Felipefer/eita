__version__ = "0.0.2"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "Jan 2020"

"""
...
...

"""

import numpy as np

def IMF(m, imf = 'Kroupa', **kwargs):

    try:
        imf_arr = np.empty(len(m))
    except TypeError:
        m = np.array([m])
        imf_arr = np.empty(len(m))

    if imf == 'Kroupa':
        cond1 = m <= 0.08
        imf_arr[cond1] = m[cond1]**(-0.3)

        cond2 = (m > 0.08) & (m <= 0.5)
        imf_arr[cond2] = m[cond2]**(-1.3)

        cond3 = m > 0.5
        imf_arr[cond3] = m[cond3]**(-2.3)

    return imf_arr


def SFH(t, sfh = 'flat', **kwargs):

    try:
        sfh_arr = np.empty(len(t))
    except TypeError:
        t = np.array([t])
        sfh_arr = np.empty(len(t))

    if sfh == 'flat':
        sfh_arr[:] = 1

    return sfh_arr


def AMR(Z, amr='flat', **kwargs):
    try:
        amr_arr = np.empty(len(Z))
    except TypeError:
        t = np.array([Z])
        amr_arr = np.empty(len(Z))

    if amr == 'flat':
        amr_arr[:] = 1

    return amr_arr


def prior(t, m, Z, imf = 'Kroupa', sfh = 'flat', amr = 'flat'):

    sfh_arr = SFH(t, sfh = sfh)
    sfh_arr = SFH(t, sfh = sfh)
    sfh_arr = SFH(t, sfh = sfh)
