from __future__ import division

import datetime
import itertools
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate, optimize, stats

from textstats import configure_args, Corpus, SelfVsSelfTest, SelfVsOtherTest


class OutputManager(object):

    def __init__(self, output_directory='outputs'):
        """

        :param output_directory:
        :param output_directory:
        :return:
        """
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)

        self.output_base_directory = output_directory

    def setup(self, iterations, stopwords, percent, method):
        """

        :param iterations:
        :param stopwords:
        :param percent:
        :param method:
        :return:
        """
        def timestamped(f, fmt='%Y%m%d-%H%M%S_{fname}'):
            return datetime.datetime.now().strftime(fmt).format(fname=f)

        results_directory = timestamped('IT{}_SW{}_PCT{}_{}'.format(iterations, stopwords, int(round(percent * 100)), method))
        self.output_final_directory = os.path.join(self.output_base_directory, results_directory)

        os.mkdir(self.output_final_directory)

        return self

    def write_output(self, data):
        """

        :param data:
        :return:
        """
        import pandas as pd
        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_csv(self.output_final_directory)







def main():
    args = configure_args()

    output = OutputManager().setup(args.iterations, args.stopwords, args.sample, args.method)

    corpus = Corpus(corpus_directory='texts')
    print 'Found {} trial texts to test.'.format(len(corpus.comparison_texts))

    print 'Loading and tokenizing texts'
    for txt in corpus.comparison_texts + corpus.praiectus_texts:
        txt.load_and_tokenize()

    print 'Running Comparisons between texts of Known Different Authorship'
    test_results = []
    for t in itertools.permutations(corpus.comparison_texts, 2):
        test = SelfVsOtherTest(t[0], t[1])
        test.run_tests(args.iterations)
        test_results.append(test)

    print 'Plotting Results'
    for tr in test_results:
        x_den = np.linspace(0, max(tr.results), 500)
        plt.plot(x_den, tr.kernel(x_den), 'blue', alpha=0.2)

    d = list(itertools.chain.from_iterable([tr.results for tr in test_results]))
    gd = stats.gaussian_kde(d)
    x_den = np.linspace(0, max(d), 500)
    plt.plot(x_den, gd(x_den), 'blue')

    print 'Running Self-Comparisons between texts'
    self_test_results = []
    for t in corpus.comparison_texts:
        test = SelfVsSelfTest(t)
        test.run_tests(args.iterations)
        self_test_results.append(test)

    print 'Plotting Results'
    for tr in self_test_results:
        x_den = np.linspace(0, max(tr.results), 5000)
        plt.plot(x_den, tr.kernel(x_den), 'red', alpha=0.2)

    d2 = list(itertools.chain.from_iterable([tr.results for tr in self_test_results]))
    gd2 = stats.gaussian_kde(d2)
    x_den = np.linspace(0, max(d2), 5000)
    plt.grid(b=10)
    plt.plot(x_den, gd2(x_den), 'red')

    print "{:.2f}%".format(calculate_curve_overlap_without_test_object(gd,gd2, xmax=550))

    result = find_intersection(gd, gd2, [0, 70])
    real_int = result[0][1]

    print integrate.quad(gd, real_int, np.inf)[0]
    plt.plot(result[0], gd(result[0]), 'ro')
    plt.show()


if __name__ == '__main__':
    main()
