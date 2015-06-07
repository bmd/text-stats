from __future__ import division

from textstats import *


def main():
    args = configure_args()

    output = OutputManager().setup(args.iterations, args.stopwords, args.sample)

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

    print 'Running Self-Comparisons between texts'
    self_test_results = []
    for t in corpus.comparison_texts:
        test = SelfVsSelfTest(t)
        test.run_tests(args.iterations)
        self_test_results.append(test)

    plot_test_results(self_test_results, test_results)

if __name__ == '__main__':
    main()
