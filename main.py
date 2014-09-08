from __future__ import division
import glob
import pyprind
from text_comp_utils.utils import *
from text_comp_utils.argconfig import *
from text_comp_utils.usage_tests import *


def main():
    args = read_configuration_options()
    # grab all files in the text folder
    files_to_process = glob.glob(os.path.join('texts', '*.txt'))
    print 'Found {} files to test...'.format(len(files_to_process))
    if args.verbose:
        print '\n'.join(files_to_process)
    # make array shell to load results
    out_array = [[] for _ in range(int(args.iterations)+1)]

    for i, fname in enumerate(files_to_process):
        out_array[0].append(fname.split('/')[1].replace('.txt' ,''))
        print 'Testing File: {}'.format(fname).upper()
        tokens = tokenize(depunctuate(ingest(fname)))
        chunk_size = int(len(tokens) * args.sample)

        if args.verbose:
            print '  - Interpreted {} word-tokens'.format(len(tokens))
            print '  - Sample based on {} words ({:.0%} of full text)'.format(chunk_size, args.sample)

        bow_results = []
        if args.verbose:
            prbar = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
        for x in xrange(int(args.iterations)):
            r = compare_stop_word_usage(tokens, args.sample, args.absolute, method=1)[0]
            out_array[x+1].append(r)
            bow_results.append(r)
            if args.verbose:
                prbar.update()
        summarize_results(bow_results, 'Chi2')
        #write_result(bow_results, fname.replace('.txt', '') + '_bow_result.csv')
    write_output(out_array)
    return


if __name__ == '__main__':
    main()
