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
    files_to_process.remove('texts/praeiecti.txt')
    print 'Found {} files to test...'.format(len(files_to_process))
    if args.verbose:
        print '\n'.join(files_to_process)
    # make array shell to load results
    out_array = [[] for _ in range(int(args.iterations)+1)]

    print 'COMPARING TEXT VS ITSELF'
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

    write_output(out_array)

    print 'COMPARING TEXT VS OTHER TEXT'
    text_vs_other_out_array = [['Base Text', 'Comparison Text','Chi2 Statistic']]
    for i, fname in enumerate(files_to_process):
        z = files_to_process[:]
        z.remove(fname)
        base_name = fname.replace('.txt', '').replace('texts/', '')
        for j, cmpname in enumerate(z):
            cmp_name = cmpname.replace('.txt', '').replace('texts/', '')
            file_1_tokens = tokenize(depunctuate(ingest(fname)))
            file_2_tokens = tokenize(depunctuate(ingest(cmpname)))
            print 'Comparing {} to {}'.format(fname, cmpname)
            for x in xrange(int(args.iterations)):
                r = compare_stop_words_against_other_texts(file_1_tokens, file_2_tokens, args.sample, args.absolute)[0]
                text_vs_other_out_array.append([base_name, cmp_name, r])
    write_output(text_vs_other_out_array)

    print 'COMPARING PRAIECTUS PIECES VS OTHER TEXT'
    text_vs_other_out_array = [['Base Text', 'Comparison Text','Chi2 Statistic']]
    p_pieces = ['texts/praiectus_1.txt', 'texts/praiectus_2.txt', 'texts/praiectus_3.txt']
    for i, fname in enumerate(p_pieces):
        z = p_pieces[:]
        z.remove(fname)
        base_name = fname.replace('.txt', '').replace('texts/', '')
        for j, cmpname in enumerate(z):
            cmp_name = cmpname.replace('.txt', '').replace('texts/', '')
            file_1_tokens = tokenize(depunctuate(ingest(fname)))
            file_2_tokens = tokenize(depunctuate(ingest(cmpname)))
            print 'Comparing {} to {}'.format(fname, cmpname)
            for x in xrange(int(args.iterations)):
                r = compare_stop_words_against_other_texts(file_1_tokens, file_2_tokens, args.sample, args.absolute)[0]
                text_vs_other_out_array.append([base_name, cmp_name, r])
    write_output(text_vs_other_out_array)


    return


if __name__ == '__main__':
    main()
