from __future__ import division
import string as s
import numpy as np
import pandas as pd
import datetime as dt

def timestamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    """
    Return a timestamped filename, quite elegantly

    Reference
    ---------
    http://stackoverflow.com/a/5215012
    """
    return dt.datetime.now().strftime(fmt).format(fname=fname)

def write_output(outfname, data):
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_csv(timestamped('test.csv'))


def ingest(fname):
    with open(fname, 'rU') as inf:
        return inf.read().replace('\n', '')


def depunctuate(text):
    #block = ''
    #for char in text:
    #    if char not in s.punctuation:
    #        block += char
    #return block
    return ''.join([c for c in text if c not in s.punctuation])

def tokenize(s):
    return [x.lower() for x in s.split(' ') if x != '']


def write_result(test_statistics, outfname):
    with open(outfname, 'wb') as outf:
        for i, t in enumerate(test_statistics):
            outf.write('{},{}\n'.format(i, t))


def summarize_results(r, statistic, p_sig=False, ):
    m, s = np.mean(r), np.std(r)
    print 'Mean {} value: {:.3f}'.format(statistic, m)
    # print significance indicators only if p values
    if p_sig:
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
            max(m-(1.67*s),0), m+(1.67*s)
        )
