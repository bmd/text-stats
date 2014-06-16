from __future__ import division
import string as s
from scipy.stats import chisquare
from collections import Counter


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
	return str.split(' ')

def test_stop_word_usage(tokens, complete_counts):
	sample_counts = Counter(tokens)
	target_words = complete_counts.most_common(20)
	# detupelize
	target_words = [[t[0], t[1]] for t in target_words]
	# wrestle everything into an array
	for pair in target_words:
		if pair[0] in sample_counts:
			pair.append(sample_counts[pair[0]])
			pair.append(pair[1]/2)
		else:
			pair.append(0)
			pair.append(pair[1]/2)

	#values to analyze are in pair2-3
	actuals = [x[2] for x in target_words]
	expecteds = [x[3] for x in target_words]

	return chisquare(f_obs = actuals, f_exp = expecteds, ddof = 1)




