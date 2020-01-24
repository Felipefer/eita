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

__version__ = "0.0.2"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"
_parsec_tests_tracks_path = "./test_tracks_PARSEC"
_parsec_tests_isocs_path = "./test_isocs_PARSEC"


"""
This module contains quick tests for trying the functions, classes and methods
defined in the eitapy package.
"""

################################################################################

def do_test(test, message = 'run test? (y, N)'):
    """
    This function is used to run the tests when test.py is called. It asks user
    input before running each test

    Parameters
    ----------
    test : funtion
        which test is being run
    message : str
        the message to show to the user when asking if this test should be run

    Returns
    -------
        runs the input 'test'
    """

    if __name__ == "__main__":
        run = raw_input(message)

        if run in ('Y', 'y'):
            t0 = time()
            test()
            print "this test took {0} seconds".format(time() - t0)


################################################################################
def test_func_load_model():
    model_name = 'PARSEC'

    ev_filepath = ("./test_tracks_PARSEC/Z0.014Y0.273"
                "/Z0.014Y0.273OUTA1.74_F7_M001.000.DAT")

    ev_md = Models.load_model(filepath=ev_filepath, model=model_name,
                              delim_whitespace = True)
    print ev_md.data

    isoc_filepath = "./test_isocs_PARSEC/isoc_t1e9Z0152.dat"

    isoc_md = Models.load_model(filepath=isoc_filepath, model=model_name,
                                delim_whitespace = True, comment = '#')

    print isoc_md.data


if __name__ == "__main__":
    run = raw_input('run test_func_load_model? (y, N)')

    if run in ('Y', 'y'):
        t0 = time()
        test_func_load_model()
        print "this test took {0} seconds".format(time() - t0)


################################################################################


def test_func_load_multiple_models():
    model_name = 'PARSEC'

    isoc_filepath = "../isocs/SPLUS/"
    filelist = os.listdir(isoc_filepath)
    for i in range(len(filelist)):
        filelist[i] = isoc_filepath + filelist[i]

    isoc_md = Models.load_multiple_models(filelist=filelist,
                                          model=model_name,
                                          delim_whitespace = True,
                                          comment = '#')

    print isoc_md.data
    print isoc_md.data.shape


if __name__ == "__main__":
    run = raw_input('run test_func_load_multiple_models? (y, N)')

    if run in ('Y', 'y'):
        t0 = time()
        test_func_load_multiple_models()
        print "this test took {0} seconds".format(time() - t0)


################################################################################


def test_method_plot():

    model_name = 'PARSEC'

    ev_filepath = ("./test_tracks_PARSEC/Z0.014Y0.273"
                "/Z0.014Y0.273OUTA1.74_F7_M001.000.DAT")

    ev_md = Models.load_model(filepath=ev_filepath, model=model_name,
                              delim_whitespace = True)

    ev_md.plot('LOG_TE', 'LOG_L')

    isoc_filepath = "./test_isocs_PARSEC/isoc_t1e9Z0152.dat"

    isoc_md = Models.load_model(filepath=isoc_filepath, model=model_name,
                                delim_whitespace = True, comment = '#')

    isoc_md.plot('logTe', 'logL')

    plt.show()


if __name__ == "__main__":
    run = raw_input('run test_method_plot? (y, N)')

    if run in ('Y', 'y'):
        t0 = time()
        test_method_plot()
        print "this test took {0} seconds".format(time() - t0)

################################################################################

#def test_func_load_model():
#    model_name = 'PARSEC'
#
#    ev_filepath = ("./test_tracks_PARSEC/Z0.014Y0.273"
#                "/Z0.014Y0.273OUTA1.74_F7_M001.000.DAT")
#
#     ev_md = Models.load_model(filepath=ev_filepath, model=model_name,
#                               delim_whitespace = True)
#
#     # Set observation and errors0.07592   3.77232
#     obs = pd.DataFrame({'LOG_L': [0.074], 'LOG_TE': [3.774]})
#     obs_err = pd.DataFrame({'LOG_L': [0.1], 'LOG_TE': [0.1]})
#
#     model = ev_md.data[['LOG_L', 'LOG_TE', 'AGE', 'MASS']]
#
#     # Test the function
#     L = fc.isoc_L(obs, obs_err, model)
#
# if __name__ == "__main__":
#     run = raw_input('run test_func_load_model? (y, N)')
#
#     if run in ('Y', 'y'):
#         t0 = time()
#         test_func_load_model()
#         print "this test took {0} seconds".format(time() - t0)


################################################################################


def test_param_probs():

    model_name = 'PARSEC'

    filepath = ("./test_isocs_PARSEC/isoc_teste_splus.dat")

    model = Models.load_model(filepath=filepath, model=model_name,
                              delim_whitespace = True, comment = '#')

    star = Star.Star(obs = {'uJAVAmag':[5.258],
                            'F378mag':[5.624],
                            'F395mag':[5.922],
                            'F410mag':[5.533],
                            'F430mag':[5.478],
                            'gSDSSmag':[5.079],
                            'F515mag':[4.869],
                            'rSDSSmag':[4.378],
                            'F660mag':[4.185],
                            'iSDSSmag':[4.040],
                            'F861mag':[3.905],
                            'zSDSSmag':[3.866]},
                     obs_err = {'uJAVAmag': [0.05],
                          'F378mag': [0.05],
                          'F395mag': [0.05],
                          'F410mag': [0.05],
                          'F430mag': [0.05],
                          'gSDSSmag': [0.05],
                          'F515mag': [0.05],
                          'rSDSSmag': [0.05],
                          'F660mag': [0.05],
                          'iSDSSmag': [0.05],
                          'F861mag': [0.05],
                          'zSDSSmag': [0.05]})


    star.get_param_probs(model=model, param_list=['Zini', 'logAge','Mini'],
                         pred_list=['logL', 'logTe'])

    plt.scatter(star.probs['logL'], star.probs['PROB'])
    plt.show()


if __name__ == "__main__":
    run = raw_input('run test_param_probs? (y, N)')

    if run in ('Y', 'y'):
        t0 = time()
        test_param_probs()
        print "this test took {0} seconds".format(time() - t0)


def test_best_model():

    model_name = 'PARSEC'

    filepath = ("./test_isocs_PARSEC/isoc_teste_splus.dat")

    model = Models.load_model(filepath=filepath, model=model_name,
                              delim_whitespace = True, comment = '#')

    star = Star.Star(obs = {'uJAVAmag':[5.258],
                            'F378mag':[5.624],
                            'F395mag':[5.922],
                            'F410mag':[5.533],
                            'F430mag':[5.478],
                            'gSDSSmag':[5.079],
                            'F515mag':[4.869],
                            'rSDSSmag':[4.378],
                            'F660mag':[4.185],
                            'iSDSSmag':[4.040],
                            'F861mag':[3.905],
                            'zSDSSmag':[3.866]},
                     obs_err = {'uJAVAmag': [0.05],
                          'F378mag': [0.05],
                          'F395mag': [0.05],
                          'F410mag': [0.05],
                          'F430mag': [0.05],
                          'gSDSSmag': [0.05],
                          'F515mag': [0.05],
                          'rSDSSmag': [0.05],
                          'F660mag': [0.05],
                          'iSDSSmag': [0.05],
                          'F861mag': [0.05],
                          'zSDSSmag': [0.05]})

    print star.best_model(model=model, param_list=['logAge','Mini'],
                          pred_list=['logL', 'logTe'])

if __name__ == "__main__":
    run = raw_input('run test_best_model? (y, N)')

    if run in ('Y', 'y'):
        t0 = time()
        test_best_model()
        print "this test took {0} seconds".format(time() - t0)


################################################################################

def test_pred_pdf():

    model_name = 'PARSEC'

    isoc_filepath = "../isocs/SPLUS/"
    filelist = os.listdir(isoc_filepath)
    for i in range(len(filelist)):
        filelist[i] = isoc_filepath + filelist[i]

    model = Models.load_multiple_models(filelist=filelist, model=model_name,
                              delim_whitespace = True, comment = '#')

    star = Star.Star(obs = {'uJAVAmag':[5.258],
                            'F378mag':[5.624],
                            'F395mag':[5.922],
                            'F410mag':[5.533],
                            'F430mag':[5.478],
                            'gSDSSmag':[5.079],
                            'F515mag':[4.869],
                            'rSDSSmag':[4.378],
                            'F660mag':[4.185],
                            'iSDSSmag':[4.040],
                            'F861mag':[3.905],
                            'zSDSSmag':[3.866]},

                     obs_err = {'uJAVAmag': [0.05],
                          'F378mag': [0.05],
                          'F395mag': [0.05],
                          'F410mag': [0.05],
                          'F430mag': [0.05],
                          'gSDSSmag': [0.05],
                          'F515mag': [0.05],
                          'rSDSSmag': [0.05],
                          'F660mag': [0.05],
                          'iSDSSmag': [0.05],
                          'F861mag': [0.05],
                          'zSDSSmag': [0.05]})

    star.get_param_probs(model=model, param_list=['Zini', 'logAge', 'Mini'],
                         pred_list=['logL', 'logTe'])

    pdf = star.pred_pdf(param = 'logL')

    plt.plot(pdf['logL'], pdf['prob'])
    #plt.plot([3.7683, 3.7683], [0,1])
    plt.plot([0, 0], [0,1])
    plt.show()

    #x = pdf.iloc[:,0].values
    #y = pdf.iloc[:,1].values

    #mean = np.sum(x*y)/np.sum(y)
    #ml = x[y == np.max(y)][0]


if __name__ == "__main__":
    run = raw_input('run test_pred_pdf? (y, N)')

    if run in ('Y', 'y'):
        t0 = time()
        test_pred_pdf()
        print "this test took {0} seconds".format(time() - t0)


################################################################################

def test_model_pred():

    model_name = 'PARSEC'

    filepath = ("./test_isocs_PARSEC/isoc_teste_splus.dat")

    model = Models.load_model(filepath=filepath, model=model_name,
                              delim_whitespace = True, comment = '#')

    star = Star.Star(obs = {'uJAVAmag':[5.258],
                            'F378mag':[5.624],
                            'F395mag':[5.922],
                            'F410mag':[5.533],
                            'F430mag':[5.478],
                            'gSDSSmag':[5.079],
                            'F515mag':[4.869],
                            'rSDSSmag':[4.378],
                            'F660mag':[4.185],
                            'iSDSSmag':[4.040],
                            'F861mag':[3.905],
                            'zSDSSmag':[3.866]},
                     obs_err = {'uJAVAmag': [0.05],
                          'F378mag': [0.05],
                          'F395mag': [0.05],
                          'F410mag': [0.05],
                          'F430mag': [0.05],
                          'gSDSSmag': [0.05],
                          'F515mag': [0.05],
                          'rSDSSmag': [0.05],
                          'F660mag': [0.05],
                          'iSDSSmag': [0.05],
                          'F861mag': [0.05],
                          'zSDSSmag': [0.05]})

    print star.get_model_pred(model=model, param_list=['logAge','Mini'],
                              pred_list=['logL', 'logTe', 'logg'])

if __name__ == "__main__":
    run = raw_input('run test_model_pred? (y, N)')

    if run in ('Y', 'y'):
        t0 = time()
        test_model_pred()
        print "this test took {0} seconds".format(time() - t0)


################################################################################

def test_param_pdf():

    model_name = 'PARSEC'

    filepath = ("../isocs/SPLUS/SPLUS_0_0.dat")

    model = Models.load_model(filepath=filepath, model=model_name,
                              delim_whitespace = True, comment = '#')

    star = Star.Star(obs = {'uJAVAmag':[5.258],
                            'F378mag':[5.624],
                            'F395mag':[5.922],
                            'F410mag':[5.533],
                            'F430mag':[5.478],
                            'gSDSSmag':[5.079],
                            'F515mag':[4.869],
                            'rSDSSmag':[4.378],
                            'F660mag':[4.185],
                            'iSDSSmag':[4.040],
                            'F861mag':[3.905],
                            'zSDSSmag':[3.866]},
                     obs_err = {'uJAVAmag': [0.05],
                          'F378mag': [0.05],
                          'F395mag': [0.05],
                          'F410mag': [0.05],
                          'F430mag': [0.05],
                          'gSDSSmag': [0.05],
                          'F515mag': [0.05],
                          'rSDSSmag': [0.05],
                          'F660mag': [0.05],
                          'iSDSSmag': [0.05],
                          'F861mag': [0.05],
                          'zSDSSmag': [0.05]})

    star.get_param_probs(model=model, param_list=['MH', 'logAge', 'Mini'],
                         pred_list=['logL', 'logTe'],
                         param_cols={'t':'logAge','m':'Mini', 'Z':'MH'})

    pdf = star.get_param_pdf(param='logAge',
                             param_cols={'t':'logAge','m':'Mini', 'Z':'MH'})

    plt.plot(pdf['logAge'], pdf['prob'])
    plt.plot([9.66,9.66], [0,1])
    plt.show()


if __name__ == "__main__":
    run = raw_input('run test_param_pdf? (y, N)')

    if run in ('Y', 'y'):
        t0 = time()
        test_param_pdf()
        print "this test took {0} seconds".format(time() - t0)