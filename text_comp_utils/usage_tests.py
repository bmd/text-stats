from __future__ import division

import sys
import numpy.random as npr

from scipy.stats import chisquare
from collections import Counter
from tests import gtest


def compare_stop_words_against_other_texts(sample_tokens, comparison_tokens, sample_size, top_n_words, method='chisquare'):

    test_function = getattr(sys.modules[__name__], method)

    if len(sample_tokens) >= len(comparison_tokens):
        sample_count = int(round(len(comparison_tokens) * sample_size))
    elif len(comparison_tokens) > len(sample_tokens):
        sample_count = int(round(len(sample_tokens) * sample_size))

    sc = Counter(npr.choice(sample_tokens, sample_count, replace=False, p=None)).most_common()
    cc = Counter(npr.choice(comparison_tokens, sample_count, replace=False, p=None))
    len_ratio = len(sc) / len(cc)
    combined = {}

    ct = 0
    for word, frequency in sc:
        if word in cc:
            combined[word] = [frequency, int(round(cc[word] * len_ratio))]
            ct += 1
            if ct == top_n_words:
                break
    a, e = [], []
    for word, freqs in combined.items():
        a.append(freqs[0])
        e.append(freqs[1])

    return test_function(f_obs=a, f_exp=e)


def compare_stop_word_usage(tokens, sample_size, top_n_words, method='chisquare'):
    """
    :param tokens: Num
    :param sample_size: number of tokens or percentage of text to sample
    :param absolute: is sample_size an absolute count of tokens or percentage
    :param method: 0 for x-vs-all method, 1 for x-vs-y method
    :return: Tuple of Chi-2 statistic and p-value
    """
    # method to test a random set of words against the expected counts
    #   of those words across the entire text, controlling for chunk size.
    test_function = getattr(sys.modules[__name__], method)
    randomized = [t for t in tokens]
    # set break as either a a fixed or relative number of tokens
    br = int(len(randomized) // (1/sample_size))
    npr.shuffle(randomized)
    bag1, bag2 = randomized[0:br], randomized[br:br*2]
    c1, c2 = Counter(bag1).most_common(), Counter(bag2)
    combined = {}
    ct = 0
    for word, frequency in c1:
        if word in c2:
            combined[word] = [frequency, c2[word]]
            ct += 1
            if ct == top_n_words:
                break
        else:
            pass

    a, e = [], []
    for word, freqs in combined.items():
        a.append(freqs[0])
        e.append(freqs[1])

    return test_function(f_obs=a, f_exp=e)