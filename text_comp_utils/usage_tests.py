from __future__ import division
from scipy.stats import chisquare
from collections import Counter

import sys
import numpy.random as npr


def compare_stop_words_against_other_texts(sample_tokens, comparison_tokens, sample_size, top_n_words):
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
    return chisquare(f_obs=a, f_exp=e)


def compare_stop_word_usage(tokens, sample_size, top_n_words, method=0):
    """
    :param tokens: Num
    :param sample_size: number of tokens or percentage of text to sample
    :param absolute: is sample_size an absolute count of tokens or percentage
    :param method: 0 for x-vs-all method, 1 for x-vs-y method
    :return: Tuple of Chi-2 statistic and p-value
    """
    # method to test a random set of words against the expected counts
    #   of those words across the entire text, controlling for chunk size.
    if method == 0:
        sc = Counter(npr.choice(tokens, int(len(tokens) * sample_size), replace=False, p=None))
        fc = [list(t) for t in Counter(tokens).most_common(20)]
        a, e = [], []
        for word, frequency in fc:
            a.append(sc[word]) if word in sc else a.append(0)
            e.append(frequency / (1 / sample_size))
    # method to directly compare two random sets of words, of the same size,
    #  and from the same text against each other
    elif method == 1:
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
    else:
        sys.exit('Invalid method flag supplied')
    return chisquare(f_obs=a, f_exp=e)

### DEPRECATED - STOP TOUCHING
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
