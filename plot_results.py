from text_comp_utils.utils import *

import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from ggplot import *

from scipy.stats import gaussian_kde

from scipy.optimize import fsolve
import pylab
import numpy

def find_intersection(fun1, fun2, x0):
    return [fsolve(lambda x : fun1(x) - fun2(x), y) for y in range(0, 1000)]

import argparse

OUTDIR = 'figures'

def read_configuration_options():
    """
    Set up and validate command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--use',
        type=str,
        help='Override use of most recent timestamped results directory'
    )
    return parser.parse_args()

def main():
    args = read_configuration_options()

    # use either the specified results dump or the most recent results dump
    if args.use:
        most_recent_results = glob.glob(os.path.join('outputs', args.use))
    else:
        most_recent_results = max(glob.glob(os.path.join('outputs', '*')))

    df_self = pd.read_csv(os.path.join(most_recent_results, 'self_vs_self_comparisons.csv'), index_col=0)
    df_text = pd.read_csv(os.path.join(most_recent_results, 'text_vs_others_comparisons.csv'), index_col=0)
    df_prae = pd.read_csv(os.path.join(most_recent_results, 'praiectus_section_comparisons.csv'), index_col=0)
    df_prae['Cmp2'] = df_prae.apply(lambda x: '%s vs %s' % (x['Base Section'],x['Comparison Section']), axis=1)

    # make sure we have somewhere to put it
    ensure_output_directory(os.path.join(most_recent_results, 'figures'))

    self_kde = gaussian_kde(df_self['Chi2 Statistic'])
    text_kde = gaussian_kde(df_text['Chi2 Statistic'])


    result = find_intersection(self_kde,text_kde,0.0)
    print result
    sys.exit()



    # make plot of self vs self comparisons
    plt = ggplot(aes(x='Chi2 Statistic', color='Text'), data=df_self)
    plt += geom_density(aes(fill=True, alpha=0.1),trim=False)
    plt += theme_bw()
    ggsave(plt, os.path.join(most_recent_results, 'figures', 'self_comparisons.pdf'))

    # make plot of self vs self comparisons
    plt = ggplot(aes(x='Chi2 Statistic', color='Base Text'), data=df_text)
    plt += geom_density(aes(fill=True, alpha=0.1),trim=False)
    plt += theme_bw()
    ggsave(plt, os.path.join(most_recent_results, 'figures', 'text_comparisons.pdf'))

    # make plot of praiectus section comparisons
    plt = ggplot(aes(x='Chi2 Statistic', color='Cmp2'), data=df_prae)
    plt += geom_density(aes(fill=True, alpha=0.1),trim=False)
    plt += theme_bw()
    ggsave(plt, os.path.join(most_recent_results, 'figures', 'prae_comparisons.pdf'))

    # make density curve overlaps
    plt = ggplot(aes(x='Chi2 Statistic', color='Cmp2'), data=df_prae)
    plt += geom_density(aes(fill=True, alpha=0.1))
    plt += geom_density(aes(x='Chi2 Statistic'), fill=True, alpha=0.1, data=df_text)
    plt += geom_density(aes(x='Chi2 Statistic'), fill=True, alpha=0.1, data=df_self)
    plt += theme_bw()
    plt += ggtitle('Text vs. Text and Text vs. Self Comparisons')
    plt += xlab('Chi2 Value')
    plt += ylab('Density')
    ggsave(plt, os.path.join(most_recent_results, 'figures', 'figure_1_curves.pdf'))
    sys.exit('Breakpoint')

    return


if __name__ == '__main__':
    main()


"""
#plot the avg curve

ggplot() + geom_density()
ggplot(aes(x='value'), data=df2) + geom_density(aes(x='value', data=df2, fill=True, alpha=0.1), trim=False)



ggplot(aes(x='Chi2 Statistic', colour='Comparison Text'), data=df) + geom_density(aes(fill=True, alpha=0.1), trim=False)

plt = ggplot(aes(x='Chi2 Statistic'), data=df)
plt = plt + geom_density(aes(fill=True, alpha=0.1), trim=False)
plt = plt + geom_density(aes(x='value'), fill=True, alpha=0.1, data=df2, trim=False)
plt + geom_density(aes(x='Chi2 Statistic', colour='Comparison Text'), data=df3, fill=True, alpha=0.1, trim=False)


ggplot(aes(x='Chi2 Statistic', colour='Base Text'), data=df3) + geom_density()
"""