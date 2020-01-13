import sys
sys.path.insert(0, '../eitapy')

import Models
from time import time
from matplotlib import pyplot as plt

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


