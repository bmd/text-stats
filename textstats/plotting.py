import numpy as np
import matplotlib.pyplot as plt
import itertools
from scipy import integrate, optimize, stats
from statistics import find_intersection


def plot_test_results(self_tests, comp_tests):
    """ Plot the results comparison tests

    Parameters
    ----------
    self_tests : list
        A list of Test objects for comparisons between sections of the same
        text.
    comp_tests : list
        A list of test objects for comparisons between texts with different
        authors.

    Returns
    -------
    None

    """

    for tr in comp_tests:
        x_den = np.linspace(0, max(tr.results), 500)
        plt.plot(x_den, tr.kernel(x_den), 'blue', alpha=0.2)

    # calculate aggregate curve
    d = list(itertools.chain.from_iterable([tr.results for tr in comp_tests]))
    gd = stats.gaussian_kde(d)
    x_den = np.linspace(0, max(d), 500)
    plt.plot(x_den, gd(x_den), 'blue')

    for tr in self_tests:
        x_den = np.linspace(0, max(tr.results), 5000)
        plt.plot(x_den, tr.kernel(x_den), 'red', alpha=0.2)

    d2 = list(itertools.chain.from_iterable([tr.results for tr in self_tests]))
    gd2 = stats.gaussian_kde(d2)
    x_den = np.linspace(0, max(d2), 5000)
    plt.grid(b=10)
    plt.plot(x_den, gd2(x_den), 'red')

    result = find_intersection(gd, gd2, [0, 70])

    plt.plot(result[0], gd(result[0]), 'ro')
    plt.show()
