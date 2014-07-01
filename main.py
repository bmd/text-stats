from __future__ import division

import utils as u
import glob
import os
from collections import Counter
import sys

import numpy as np
import scipy.stats

if __name__ == '__main__':
	files_to_process = glob.glob(os.path.join('texts', '*.txt'))
	print 'Found {} files...'.format(len(files_to_process))
	
	for fname in files_to_process:
		print 'Running analysis on {}'.format(fname)
		# tokenize the file
		tokens = u.tokenize(u.depunctuate(u.ingest(fname)))
		chunk_size = len(tokens) // 2		
		total_word_counts = Counter(tokens)

		# bag of words
		bow_results = []
		for x in xrange(int(sys.argv[1])):
			if x % 100 == 0 and x != 0: print '\r{}'.format(x)
			# randomly sample 50% of the words
			sample = np.random.choice(tokens, len(tokens)//2, replace=False, p=None)
			bow_results.append(u.test_stop_word_usage(sample, total_word_counts)[1])
		# contiguous chunks

		with open(fname.replace('.txt','') + '_result.csv', 'w') as outf:
			hist = np.histogram(bow_results, bins=25)
			for i in xrange(len(hist[0])):
				outf.write('{},{}\n'.format(hist[0][i], hist[1][i]))

