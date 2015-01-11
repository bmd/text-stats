from __future__ import division

import datetime as dt
import glob
import os
import string as s

import pandas as pd


# ------------------
# File I/O Utilities
# ------------------
def timestamped(fname, fmt='%Y%m%d-%H%M%S_{fname}'):
    """
    Return a timestamped filename, quite elegantly

    Reference
    ---------
    http://stackoverflow.com/a/5215012
    """
    return dt.datetime.now().strftime(fmt).format(fname=fname)


def ensure_output_directory(outdir_path):
    if not os.path.exists(outdir_path):
        print 'Created output directory...'
        os.mkdir(outdir_path)
    return outdir_path


def set_up_results_directory(results_path, iterations, method):
    results_directory = timestamped('outputs_{}_iterations_{}'.format(iterations, method))
    res_dir = os.path.join(results_path, results_directory)
    os.mkdir(res_dir)
    return res_dir


def write_output_file(outdir, data, filename):
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_csv(os.path.join(outdir, filename))


def collect_project_files(base_dir):
    def get_txt_files_from_folder(path):
        texts = glob.glob(os.path.join(path, '*.txt'))
        for i, path in enumerate(texts):
            texts[i] = {
                'path': path,
                'proper': path.split('/')[-1].replace('.txt', '').replace('_', ' ')
            }
        return texts

    trial_text_path = os.path.join(base_dir, 'trial_texts')
    praiectus_text_path = os.path.join(base_dir, 'praiectus')

    return get_txt_files_from_folder(trial_text_path), get_txt_files_from_folder(praiectus_text_path)


# -------------------------
# Text processing utilities
# -------------------------
def ingest(fname):
    with open(fname, 'rU') as inf:
        return inf.read().replace('\n', '')


def depunctuate(text):
    return ''.join([c for c in text if c not in s.punctuation])


def tokenize(text, sep_char=' '):
    """ Lowercase and split a string into tokens.

    Parameters
    ----------
    text: str
        String to convert to tokens.
    sep_char: str, optional
        Character to use to split string; defaults to a single space.

    Returns
    -------
    tokens: list
        A list of word tokens.
    """

    return [x.lower() for x in text.split(sep_char) if x != '']
