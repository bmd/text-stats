# 'dem imports
from __future__ import division
from collections import Counter
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

def read_configuration_options():
    """
    Set up and validate command line arguments
    """
    parser = argparse.ArgumentParser()
    #analysis_type = parser.add_mutually_exclusive_group(required = True)
    parser.add_argument(
        'iterations', 
        type = str, 
        help = 'Number of times to run the simulation for each text.'
    )
    parser.add_argument(
        'sample', 
        type = float, 
        help = 'Percent of text to sample'
    )
    #analysis_type.add_argument(
    #    '--bag-of-words', 
    #    action = 'store_true', 
    #    help = 'Randomly sample words'
    #)
    #analysis_type.add_argument(
    #    '--blocks', 
    #    action = 'store_true', 
    #    help = 'Sample words as contiguous blocks'
    #)
    return parser.parse_args()

def ingest(fname):
    with open(fname, 'rU') as inf:
        return inf.read().replace('\n','')

def depunctuate(text):
    block = ''
    for char in text:
        if char not in s.punctuation:
            block += char
    return block

def tokenize(str):
    return [x.lower() for x in str.split(' ') if x != '']

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

    return chisquare(f_obs = actuals, f_exp = expecteds)

## FUNCTIONS ##
def test_stop_word_multibag(tokens):
    randomized = [t for t in tokens]
    br = len(randomized) // 2
    npr.shuffle(randomized)
    bag1, bag2 = randomized[0:br], randomized[br:]
    c1 = Counter(bag1).most_common(20)
    c2 = Counter(bag2)
    combined = {}
    for word, frequency in c1:
        if word in c2:
            combined[word] = [frequency, c2[word]]
        else: pass

    a, e = [], []
    for word, freqs in combined.items():
        a.append(freqs[0])
        e.append(freqs[1])

    return chisquare(f_obs=a, f_exp=e)

def test_stop_word_combined(tokens, sample_size, method_flag=0):
    if method_flag == 0:
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
    m, s = np.mean(r), np.std(r)
    print 'Mean p-value: {:.3f}'.format(m),
    # print significance indicators
    #if m <= 0.01:      print '***'
    #elif m <= 0.05:    print '**'
    #elif m <= 0.1:     print '*'
    #else:              print ''
    #print '90-percent CI: ({:.2f}, {:.2f})'.format(max(m-(1.67*s),0), min(m+(1.67*s),1))   
    print '90-percent CI: ({:.2f}, {:.2f})'.format(m-(1.67*s), m+(1.67*s),1) 

if __name__ == '__main__':
    files_to_process = glob.glob(os.path.join('texts', '*.txt'))
    print 'Found {} files...'.format(len(files_to_process))
    args = read_configuration_options()

    for fname in files_to_process:
        #print '\n'
        #print 'Testing File: {}'.format(fname).upper()
        # tokenize the file
        tokens = tokenize(depunctuate(ingest(fname)))
        print 'Interpreted {} word-tokens'.format(len(tokens))
        chunk_size = int(len(tokens) * args.sample)      
        print 'Sample based on {} words ({:.0%} of full text)'.format(chunk_size, args.sample)
        #print '\n'        
        # test bag of words method
        #print '-----------------------------------'
        #print '-- Testing \'bag-of-words\' method --'
        #print '-----------------------------------'
        #bow_results = []
        #prbar = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
        #for x in xrange(int(args.iterations)):
        #    bow_results.append(test_stop_word_combined(tokens, args.sample, method_flag=0)[0])
        #    prbar.update()
        #summarize_results(bow_results)
        #print '\n'
        # test contiguous samples method
        #print '-----------------------------------------'
        #print '-- Testing \'contiguous samples\' method --'
        #print '-----------------------------------------'
        #con_results = []
        #prbar2 = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
        #for x in xrange(int(args.iterations)):
        #    con_results.append(test_stop_word_combined(tokens, args.sample, method_flag=1)[0])
        #    prbar2.update()
        #summarize_results(con_results)
        print '\n'
        print '-----------------------------------------'
        print '-- Testing \'multiple bags\' method --'
        print '-----------------------------------------'
        mul_bags = []
        #prbar3 = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
        for x in range(int(args.iterations)):
            mul_bags.append(test_stop_word_multibag(tokens)[0])
        #    prbar3.update()
        summarize_results(mul_bags)

        with open(fname.replace('.txt','') + '_result.csv', 'w') as outf:
            hist = np.histogram(mul_bags, bins=25)
            outf.write('Bins,Counts\n')
            for i in xrange(len(hist[0])):
                outf.write('{},{}\n'.format(hist[1][i], hist[0][i]))
