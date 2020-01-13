__version__ = "0.0.2"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "Jan 2020"

import pandas as pd
import numpy as np



def isoc_L(obs, obs_err, models, params = None):
    """

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

