from __future__ import division

import random
from collections import Counter
from scipy.stats import gaussian_kde, chisquare
import numpy.random as npr


class Test(object):
    def run_tests(self, n):
        for i in xrange(n):
            self._compare_stop_word_usage()

        self.kernel = gaussian_kde(self.results)

    def _compare_stop_word_usage(self):
        # abstract method for doing the statistical comparisons
        raise NotImplementedError


class SelfVsSelfTest(Test):

    def __init__(self, text, sample=0.5, num_words=20):
        self.text = text.tokens
        self.num_words = num_words
        self.section_1_tokens = []
        self.section_2_tokens = []
        self.run_count = 0
        self.results = []
        self.kernel = None

        # split test into two sets of tokens
        self.partition_text()

    def partition_text(self):
        split = random.randint(0, len(self.text))
        midpoint = len(self.text) // 2

        if split >= midpoint:
            self.section_1_tokens = self.text[split - midpoint: split]
            self.section_2_tokens = self.text[:split - midpoint] + self.text[split - midpoint:]
        else:
            self.section_1_tokens = self.text[split: split+midpoint]
            self.section_2_tokens = self.text[:split+midpoint] + self.text[split + midpoint:]

    def _compare_stop_word_usage(self):
        bag1 = npr.choice(self.section_1_tokens, len(self.section_1_tokens) // 2)
        bag2 = npr.choice(self.section_2_tokens, len(self.section_2_tokens) // 2)
        c1, c2 = Counter(bag1).most_common(), Counter(bag2)
        combined = {}
        ct = 0
        for word, frequency in c1:
            if word in c2:
                combined[word] = [frequency, c2[word]]
                ct += 1
                if ct == self.num_words:
                    break

        a, e = [], []
        for word, freqs in combined.items():
            a.append(freqs[0])
            e.append(freqs[1])

        self.results.append(chisquare(f_obs=a, f_exp=e)[0])
        self.run_count += 1


class SelfVsOtherTest(Test):

    def __init__(self, text1, text2, sample=0.5, num_words=20):
        self.text1 = text1.tokens
        self.text_1_length = len(self.text1)
        self.text2 = text2.tokens
        self.text_2_length = len(self.text2)
        self.run_count = 0
        self.results = []
        self.num_words = num_words
        self.kernel = None
        self.sample_count = min(self.text_1_length, self.text_2_length) // 2

    def _compare_stop_word_usage(self):
        sc = Counter(npr.choice(self.text1, self.sample_count, replace=False, p=None)).most_common()
        cc = Counter(npr.choice(self.text1, self.sample_count, replace=False, p=None))
        len_ratio = len(sc) / len(cc)
        combined = {}

        ct = 0
        for word, frequency in sc:
            if word in cc:
                combined[word] = [frequency, int(round(cc[word] * len_ratio))]
                ct += 1
                if ct == self.num_words:
                    break

        a, e = [], []
        for word, freqs in combined.items():
            a.append(freqs[0])
            e.append(freqs[1])

        self.results.append(chisquare(f_obs=a, f_exp=e)[0])
        self.run_count += 1
