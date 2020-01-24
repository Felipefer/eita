__version__ = "0.0.2"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "Jan 2020"

import pandas as pd
import numpy as np



def isoc_L(obs, obs_err, models, params = None):
    """
    OBSOLETE

    Parameters
    ----------
    obs: pd dataframe
        each column corresponds to a different observable
    obs_err: pd dataframe
        each column corresponds to the uncertainty of an observable
    models: pd dataframe for models with different parameters and predicted
            observations for each case.



    Returns
    -------
    pd.DataFrame
        DataFrame columns are {L, params}
            where L is the isochronal method L(param | obs)


    Example
    -------

    obs
        logTe   logL
          3.8    4.5

    obs_err
        logTe   logL
          0.1    0.1

    models
        MASS                AGE      logL     logTe
     1.00000  0.00000000000E+00   2.51160   3.56539
     1.00000  3.96110000000E-05   2.51160   3.56539
     1.00000  8.91250000000E-05   2.51160   3.56539
     1.00000  1.51017000000E-04   2.51160   3.56539
     1.00000  2.28382000000E-04   2.51160   3.56539
     1.00000  3.25088000000E-04   2.51160   3.56539
     ...        ...                 ...         ...
     1.00000  1.10754617509E+10   3.40283   3.49380
     1.00000  1.10754621732E+10   3.40284   3.49379

    """

    if obs.shape[0] != 1 or obs_err.shape[0] != 1:
        raise ValueError(("obs and obs_err shape[0] must be 1"))


    # get obs columns names from obs. Obs columns names on models
    # must be the same.
    obs_columns = list(obs.columns)

    # turn dataframes to arrays (selecting obs columns)
    obs_arr = obs.values
    obs_err_arr = obs_err.values

    models_obs_arr = models[obs_columns].values

    # Calculate chi2 array
    chi2 = np.sum((obs_arr - models_obs_arr)**2 / obs_err_arr**2, axis = 1)

    # Calculate L
    L = np.prod(1/(np.sqrt(2*np.pi)*obs_err_arr), axis = 1) * np.exp(-chi2/2)

    return L



def delta_vec_1d(arr):
    """

    Parameters
    ----------
    arr

    Returns
    -------

    """
    arr = np.array(arr)

    delta = np.empty(len(arr))
    delta[:-1] = arr[1:]-arr[:-1]
    delta[-1] = arr[-1]/2-arr[-2]/2

    return delta



def delta_vec(arr):
    """
    \TODO raise error if array is not ordered

    Parameters
    ----------
    arr

    Returns
    -------

    """
    #print arr.shape

    delta = np.full(arr.shape, np.nan)

    # Calculating delta for the first column

    col_set = np.sort(list(set(arr[:, 0])))

    if len(col_set) == 1:
        delta_set = [1]
    else:
        delta_set = delta_vec_1d(col_set)

    for i in range(len(col_set)):
        slice = arr[:,0] == col_set[i]
        delta[:,0][slice] = delta_set[i]

        # If the array has more than one column, calculate delta iteratively
        if arr.shape[1] > 1:
            arr_son = arr[:,1:][slice]
            delta[:, 1:][slice] = delta_vec(arr_son)

    return delta


def get_Mabs(mag_apr, mag_apr_err, dist, dist_err, A, A_err, N = 1000):

    # Sample mags, dists and Avs
    mag_arr  = np.random.normal(mag_apr, mag_apr_err, N)
    dist_arr = np.abs(np.random.normal(dist, dist_err, N))
    A_arr   = np.random.normal(A, A_err, N)

    # Calculate absolute magnitudes
    Mag_arr = mag_arr - 5*np.log10(dist_arr) + 5 - A_arr

    Mag_abs = np.mean(Mag_arr)
    Mag_abs_err = np.sqrt(np.var(Mag_arr))

    return Mag_abs, Mag_abs_err



def isoc_L(star, model, params = None):
    """
    OBSOLETE

    Parameters
    ----------
    obs: pd dataframe
        each column corresponds to a different observable
    obs_err: pd dataframe
        each column corresponds to the uncertainty of an observable
    models: pd dataframe for models with different parameters and predicted
            observations for each case.



    Returns
    -------
    pd.DataFrame
        DataFrame columns are {L, params}
            where L is the isochronal method L(param | obs)


    Example
    -------

    obs
        logTe   logL
          3.8    4.5

    obs_err
        logTe   logL
          0.1    0.1

    models
        MASS                AGE      logL     logTe
     1.00000  0.00000000000E+00   2.51160   3.56539
     1.00000  3.96110000000E-05   2.51160   3.56539
     1.00000  8.91250000000E-05   2.51160   3.56539
     1.00000  1.51017000000E-04   2.51160   3.56539
     1.00000  2.28382000000E-04   2.51160   3.56539
     1.00000  3.25088000000E-04   2.51160   3.56539
     ...        ...                 ...         ...
     1.00000  1.10754617509E+10   3.40283   3.49380
     1.00000  1.10754621732E+10   3.40284   3.49379

    """

    # Prepare arrays to calculate chi2 and L
    obs_arr = star.obs.values
    obs_err_arr = star.obs_err.values

    obs_columns = list(star.obs.columns)
    models_obs_arr = model.data[obs_columns].values

    # Calculate chi2 array
    chi2 = np.sum((obs_arr - models_obs_arr)**2 / obs_err_arr**2, axis = 1)

    # Calculate L
    L = np.prod(1/(np.sqrt(2*np.pi)*obs_err_arr), axis = 1) * np.exp(-chi2/2)

    return L


def df_columns_except(df, columns):

    all_cols = list(df.columns)
    return_cols = []

    for col in all_cols:
        if col not in columns:
            return_cols.append(col)

    return return_cols


def get_bin_size(x, y, vmin = None, vmax = None, bin_size = None, Nbins = 100):

    x_interval = x[y >= 0.001]

    interval_ini = np.min(x_interval)
    interval_fin = np.max(x_interval)

    interval_size = interval_fin - interval_ini

    if Nbins is None:
        Nbins = int((vmax - vmin)/bin_size)

    if vmin is None:
        vmin = interval_ini - 3*interval_size

    if vmax is None:
        vmax = interval_fin + 3*interval_size

    if bin_size is None:
        bin_size = (vmax - vmin)/Nbins

    return vmin, vmax, bin_size, Nbins


