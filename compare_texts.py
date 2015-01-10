from __future__ import division
import glob
import pyprind
from text_comp_utils.utils import *
from text_comp_utils.argconfig import *
from text_comp_utils.usage_tests import *

import sys
DIR = 'texts'
OUTDIR = 'outputs'

def main():
    """ Setup
    Set program configurations and identify texts for analysis
    """
    args = read_configuration_options()
    ensure_output_directory(OUTDIR)
    res_dir = set_up_results_directory(OUTDIR, args.iterations)

    trial_texts, praiectus_sections = collect_project_files(DIR)
    print 'Found {} trial texts to test.'.format(len(trial_texts))
    if args.verbose:
        for x in trial_texts:
            print '  - {proper}: {path}'.format(**x)

    ###############################
    # DO SELF VS SELF COMPARISONS #
    ###############################
    print 'Comparing each text against a sample of its own words'
    text_vs_self_results = [['Text', 'Chi2 Statistic']]

    for f in trial_texts:
        print 'Testing text "{proper}"...'.format(**f)
        tokens = tokenize(depunctuate(ingest(f['path'])))
        chunk_size = int(len(tokens)*args.sample)
        if args.verbose:
            print '  - Interpreted {} word-tokens'.format(len(tokens))
            print '  - Sample based on {} words ({:.0%} of full text)'.format(chunk_size, args.sample)
        if args.verbose:
            prbar = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
        for x in xrange(args.iterations):
            chi2, p = compare_stop_word_usage(tokens, args.sample, args.stopwords, method=1)
            if args.verbose:
                prbar.update()
            text_vs_self_results.append([f['proper'], chi2])

    write_output_file(res_dir, text_vs_self_results, 'self_vs_self_comparisons.csv')

    ###############################
    # DO TEXT VS TEXT COMPARISONS #
    ###############################
    print 'Comparing each text against other trial texts'
    text_vs_others_results = [['Base Text', 'Comparison Text', 'Chi2 Statistic']]
    for f in trial_texts:
        cmp_texts = [t for t in trial_texts if t['path'] != f['path']]
        for j in cmp_texts:
            print 'Comparing {} to {}'.format(f['proper'], j['proper'])
            base_text_tokens = tokenize(depunctuate(ingest(f['path'])))
            cmp_text_tokens = tokenize(depunctuate(ingest(j['path'])))
            if args.verbose:
                prbar = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
            for x in xrange(args.iterations):
                chi2, p = compare_stop_words_against_other_texts(base_text_tokens, cmp_text_tokens, args.sample, args.stopwords)
                if args.verbose:
                    prbar.update()
                text_vs_others_results.append([f['proper'], j['proper'], chi2])
    write_output_file(res_dir, text_vs_others_results, 'text_vs_others_comparisons.csv')

    ######################################
    # DO PRAIECTUS VS OTHERS COMPARISONS #
    ######################################

    print 'Comparing Suspected Praiectus Sections against Each Other'
    praiectus_comparisons = [['Base Section', 'Comparison Section','Chi2 Statistic']]
    for f in praiectus_sections:
        cmp_sections = [s for s in praiectus_sections if s['path'] != f['path']]
        for c in cmp_sections:
            section_1_tokens = tokenize(depunctuate(ingest(f['path'])))
            section_2_tokens = tokenize(depunctuate(ingest(c['path'])))
            if args.verbose:
                prbar = pyprind.ProgBar(int(args.iterations), stream=sys.stdout)
            for x in xrange(args.iterations):
                chi2, p = compare_stop_words_against_other_texts(section_1_tokens, section_2_tokens, args.sample, args.stopwords)
                if args.verbose:
                    prbar.update()
                praiectus_comparisons.append([f['proper'], c['proper'], chi2])
    write_output_file(res_dir, praiectus_comparisons, 'praiectus_section_comparisons.csv')

    return


if __name__ == '__main__':
    main()
