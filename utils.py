from __future__ import division
import string as s
from scipy.stats import chisquare
from collections import Counter
import argparse
import sys

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
	


	#for [word, frequency] in s1_common:







