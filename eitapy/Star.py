__version__ = "0.0.2"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
__date__    = "Jan 2020"

import sys
sys.path.insert(0, '../eitapy')

import pandas as pd
import numpy as np
import func as fc

"""Defines the Star and StellarPopulation classes and their methods

...
...

"""



class Star(object):

    def __init__(self, id = None, obs = None, obs_err = None):
        """
        Each object of this instance represent a single star, and contains
        its observational parameters (position, distance, magnitude,
        abundances, atmospheric parameters, etc), and the methods to
        estimate different properties from these parameters.

        Parameters
        ----------
        id : str
            identificator of the star
        obs : dict, pd.DataFrame
            if a dictionary, keys must be names of observational parameters,
            and values the value of the observation. If a pd.DataFrame,
            each column must be a different observational parameter
        """

        self.id = id

        if obs is not None:
            if isinstance(obs, dict):
                self.obs = pd.DataFrame(obs)
            if isinstance(obs, pd.DataFrame):
                self.obs = obs

        if obs_err is not None:
            if isinstance(obs_err, dict):
                self.obs_err = pd.DataFrame(obs_err)
            if isinstance(obs, pd.DataFrame):
                self.obs_err = obs_err

        self.probs = None


    def get_param_probs(self, model, delta = True,
                        obs_list = None, param_list = None, pred_list = None):

        """

        Parameters
        ----------
        model
        delta
        obs_list
        param_list
        pred_list

        Returns
        -------

        """


        # Get default list of observables
        if obs_list is None:
            obs_list = list(self.obs.columns)

        if param_list is None:
            param_list = list(model.param_list)

        if pred_list is None:
            pred_list = list(model.pred_list)


        # Sort the model dataframe, which is needed for the proper use of delta
        if delta:
            model_dataframe = model.data.sort_values(by = param_list)
        else:
            model_dataframe = model.data


        # Prepare arrays to calculate chi2 and L
        obs_arr = self.obs.values
        obs_err_arr = self.obs_err.values


        # prepare model array
        models_obs_arr = model_dataframe.loc[:,obs_list].values
        models_param_arr = model_dataframe.loc[:,param_list].values


        # Calculate chi2 array
        chi2 = np.sum((obs_arr-models_obs_arr)**2 / obs_err_arr**2,
                      axis=1)


        # Calculate L
        L = np.prod(1 / (np.sqrt(2 * np.pi) * obs_err_arr),axis=1) * np.exp(
            -chi2 / 2)


        # Include delta
        if delta:
            delta_arr = fc.delta_vec(models_param_arr)

        L = L * np.prod(delta_arr, axis = 1)

        # Normalizing L
        L = L/L.max()

        probs = L

        # Prepare output dataframe
        self.probs = model.data.loc[:,param_list+pred_list]
        self.probs['PROB'] = probs


    def pred_pdf(self, param = 'logTe', vmin = None,
                 vmax = None, bin_size = None, Nbins = 100):

        x = self.probs[param]
        y = self.probs['PROB']

        vmin, vmax, bin_size, Nbins = fc.get_bin_size(x, y,
                                                      vmin = vmin,
                                                      vmax = vmax,
                                                      bin_size = bin_size,
                                                      Nbins = Nbins)

        print vmin, vmax, bin_size

        bins = np.arange(vmin, vmax, bin_size)
        bins_center = bins[:-1]+bin_size/2.0

        counts = np.full(len(bins_center), 0.0)


        for i in range(len(bins)-1):

            bin_slice = (x >= bins[i]) & (x < bins[i+1])
            counts[i] = np.sum(y[bin_slice])

        counts = counts/counts.max()

        pdf = pd.DataFrame({param:bins_center, 'prob':counts})

        return pdf


    def get_pred_value(self, param, estimator = 'mean'):

        # first, get the pdf
        pdf = self.pred_pdf(param)

        x = pdf.loc[:,param].values
        y = pdf.loc[:,'prob'].values

        if estimator in ('mean', 'Mean'):

            X = np.sum(x*y)/np.sum(y)


        elif estimator in ('most likely', 'Most likely', 'Most Likely',
                           'MostLikely', 'ml', 'ML'):

            X = x[y == np.max(y)][0]

        return X


    def get_model_pred(self, pred_list, model = None, obs_list = None,
                       param_list = None):

        if self.probs is None:
            self.get_param_probs(model=model, obs_list=obs_list,
                                 param_list=param_list,
                                 pred_list = pred_list)

        predictions = {}

        for pred in pred_list:
            predictions[pred] = [self.get_pred_value(pred)]

        self.model_pred = pd.DataFrame(predictions)
        return self.model_pred


    def best_model(self, model, obs_list = None,
                   param_list = None, pred_list = None):

        if self.probs is None:
            self.get_param_probs(model=model, obs_list=obs_list,
                                 param_list=param_list,
                                 pred_list = pred_list)

        best_model = self.probs['PROB'] == np.max(self.probs['PROB'])

        return self.probs.loc[best_model,:]



    def marginalize_prob(self, param, marginalize = 'all'):

        # first get default params to be marginalized, if needed
        if marginalize == 'all':
            marginalize = fc.df_columns_except(self.probs, ['PROB', param])

        # Now, estimate the bin centers
        param_bin_center = set(self.probs[param])

        marginalized_prob = np.zeros(len(param_bin_center), np.nan)

        for i in range(len(marginalized_prob)):
            param_value = marginalized_prob[i]

            vec_to_sum = self.probs['PROB'][param==param_value]
            for jkl in range(len(marginalize)):
                param_jkl = marginalize[jkl]
                vec_to_sum *= fc.delta_vec(self.probs[param_jkl])

            marginalized_prob[i]=np.sum(vec_to_sum)


        return marginalized_prob


class ParamProbs(object):

    def __init__(self, model_params, probs):
        self.probs = model_params
        self.probs['PROB'] = probs





class StellarPopulation(object):
    pass