# 'dem imports
from __future__ import division
from utils import *
from collections import Counter

import glob
import os
import pyprind
import sys

import numpy as np
import numpy.random as npr
import scipy.stats

## FUNTIONS ##
def test_stop_word_combined(tokens, sample_size, method_flag=0):
    if method_flag == 0: # bag of words
        sc = Counter(npr.choice(tokens, int(len(tokens)*sample_size), replace=False, p=None))
    elif method_flag == 1: # contiguous chunk
        chunk = int(sample_size * len(tokens))
        pos = npr.randint(len(tokens))
        # handle wrapping around to the beginning of the text if needed
        if (pos + chunk) > len(tokens):
            sc = Counter(tokens[pos:] + tokens[0:((pos+chunk) - len(tokens))])
        else:
            sc = Counter(tokens[pos:(pos+chunk)])
    else:
        sys.exit('Invalid method flag supplied')

    # same across all methods? - yes and don't factor this out.
    fc = [list(t) for t in Counter(tokens).most_common(20)]
    a, e = [], []
    for word, frequency in fc:
        a.append(sc[word]) if word in sc else a.append(0)
        e.append(frequency/(1/sample_size))
    return chisquare(f_obs=a, f_exp=e)

def summarize_results(r):
    mu = np.mean(r)
    print 'Mean p-value: {:.3f}'.format(mu),
    # print significance indicators
    if mu <= 0.01:      print '***'
    elif mu <= 0.05:    print '**'
    elif mu <= 0.1:     print '*'
    else:               print ''
    print '90-percent CI: ({:.2f}, {:.2f})'.format(max(np.mean(r)-(1.67*np.std(r)),0), 
                                                   min(np.mean(r)+(1.67*np.std(r)),1)
                                                   )   


if __name__ == '__main__':
    files_to_process = glob.glob(os.path.join('texts', '*.txt'))
    print 'Found {} files...'.format(len(files_to_process))
    args = read_configuration_options()

    for fname in files_to_process:
        print 'Testing File: {}'.format(fname).upper()
        # tokenize the file
        tokens = tokenize(depunctuate(ingest(fname)))
        print 'Interpreted {} word-tokens'.format(len(tokens))
        chunk_size = int(len(tokens) * args.sample)      
        print 'Sample based on {} words ({:.0%} of full text)'.format(chunk_size, args.sample)
        
        # test bag of words method
        print '-----------------------------------'
        print '-- Testing \'bag-of-words\' method --'
        print '-----------------------------------'
        bow_results = []
        prbar = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
        for x in xrange(int(args.iterations)):
            bow_results.append(test_stop_word_combined(tokens, args.sample, method_flag=0)[1])
            prbar.update()
        summarize_results(bow_results)

        # test contiguous samples method
        print '-----------------------------------------'
        print '-- Testing \'contiguous samples\' method --'
        print '-----------------------------------------'
        con_results = []
        prbar2 = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
        for x in xrange(int(args.iterations)):
            con_results.append(test_stop_word_combined(tokens, args.sample, method_flag=1)[1])
            prbar2.update()
        summarize_results(con_results)

        #with open(fname.replace('.txt','') + '_result.csv', 'w') as outf:
        #    hist = np.histogram(bow_results, bins=25)
        #    outf.write('Bins,Counts\n')
        #    for i in xrange(len(hist[0])):
        #        outf.write('{},{}\n'.format(hist[1][i], hist[0][i]))


