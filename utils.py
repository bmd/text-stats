from __future__ import division
import string as s
import numpy as np


def ingest(fname):
    with open(fname, 'rU') as inf:
        return inf.read().replace('\n', '')


def depunctuate(text):
    block = ''
    for char in text:
        if char not in s.punctuation:
            block += char
    return block


def tokenize(s):
    return [x.lower() for x in s.split(' ') if x != '']


def write_result(test_statistics, outfname):
    with open(outfname, 'wb') as outf:
        for i, t in enumerate(test_statistics):
            outf.write('{},{}\n'.format(i, t))


def summarize_results(r, statistic, pval=False):
    m, s = np.mean(r), np.std(r)
    print 'Mean {} value: {:.3f}'.format(statistic, m)
    # print significance indicators only if p values
    if pval:
        if m <= 0.01:
            print '***'
        elif m <= 0.05:
            print '**'
        elif m <= 0.10:
            print '*'
        print '90-percent CI: ({:.2f}, {:.2f})'.format(
            max(m-(1.67*s), 0), min(m+(1.67*s), 1)
        )
    else:
        print '90-percent CI: ({:.2f}, {:.2f})'.format(
            m-(1.67*s), m+(1.67*s)
        )
