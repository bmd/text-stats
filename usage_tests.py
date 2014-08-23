from __future__ import division
from scipy.stats import chisquare
from collections import Counter

import glob
import os
import pyprind
import sys
import argparse
import numpy as np
import numpy.random as npr
import scipy.stats
import string as s

def test_random_paired_chunks(tokens, chunk_size):
    randomized = [t for t in tokens]
    br = len(randomized) // (1/chunk_size)
    npr.shuffle(randomized)
    bag1, bag2 = randomized[0:br], randomized[br:]
    c1 = Counter(bag1).most_common(20)
    c2 = Counter(bag2)
    combined = {}
    for word, frequency in c1:
        if word in c2:
            combined[word] = [frequency, c2[word]]
        else:
            pass

    a, e = [], []
    for word, freqs in combined.items():
        a.append(freqs[0])
        e.append(freqs[1])

    return chisquare(f_obs=a, f_exp=e)


def test_stop_word_combined(tokens, sample_size, method_flag=0):
    if method_flag == 0:
        sc = Counter(
            npr.choice(tokens, int(len(tokens) * sample_size), replace=False, p=None))
    elif method_flag == 1:  # contiguous chunk
        chunk = int(sample_size * len(tokens))
        pos = npr.randint(len(tokens))
        # handle wrapping around to the beginning of the text if needed
        if (pos + chunk) > len(tokens):
            sc = Counter(
                tokens[pos:] + tokens[0:((pos + chunk) - len(tokens))])
        else:
            sc = Counter(tokens[pos:(pos + chunk)])
    else:
        sys.exit('Invalid method flag supplied')

    # same across all methods? - yes and don't factor this out.
    fc = [list(t) for t in Counter(tokens).most_common(20)]
    a, e = [], []
    for word, frequency in fc:
        a.append(sc[word]) if word in sc else a.append(0)
        e.append(frequency / (1 / sample_size))
    return chisquare(f_obs=a, f_exp=e)


def test_stop_word_usage_against_sample(sample_1, sample_2):
    s1_common = Counter(sample_1).most_common(20)
    s2_common = Counter(sample_2).most_common(20)
    # interleve results
    combined = {}

    for (word, frequency) in s1_common:
        combined[word] = [word, frequency, 0]
    for (word, frequency) in s2_common:
        if word in combined:
            combined[word][2] = frequency
        else:
            combined[word] = [word, 0, frequency]

    pairs = [x for x in combined.values() if (x[1] != 0 and x[2] != 0)]
    actuals = [x[1] for x in pairs]
    expecteds = [x[2] for x in pairs]

    return chisquare(f_obs=actuals, f_exp=expecteds)
