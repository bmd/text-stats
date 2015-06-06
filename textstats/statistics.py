from scipy import optimize, integrate

def calculate_curve_overlap(k, l, xmin=0, xmax=500):
    """ Calculate the overlapping area between two functions.

    Parameters
    ----------
    k : function-like
        The first function.
    l : function-like
        The second function.
    xmin : numeric, default 0
        The minimum x value to integrate over.
    xmax : numeric, default 500
        The maximum x value to integrate over.

    Returns
    -------
    float :
        The integral of k(x) - l(x) from xmin, xmax

    """
    overlap = integrate.quad(lambda y: min(k(y), l(y)), xmin, xmax)
    return overlap[0]


def find_intersection(f, g, x0):
    """ Find the intersection points between two functions

    Paramters
    ---------
    f : function-like
        The first function to analyze.
    g : function-like
        The second function to analyze.
    x0 : numeric or array of numeric types
        Guesses for the intersection point(s) of the two functions
        to start the search algorithms.

    Returns
    -------
    tuple
        A scipy.optimize.fsolve object,

    References
    ----------
    http://wiki.scipy.org/Cookbook/Intersection

    """
    return optimize.fsolve(lambda x: f(x) - g(x), x0, full_output=True, factor=1)


def calculate_test_overlap(t1, t2, a=0, b=500):
    """ Calculate the overlap between two test results

    Parameters
    ----------
    t1 : Test
        The results of the first test - must have a Test.kernel value
        calcuated.
    t2 : Test
        The results of the second test - must have a Test.kernel value
        calculated.
    a : numeric, default 0
        The minimum x value to integrate over.
    b : numeric, default 500
    xmax : numeric, default 500
        The maximum x value to integrate over.

    Returns
    -------
        float : The shared area
    """
    return calculate_curve_overlap(t1.kernel, t2.kernel, a, b)
