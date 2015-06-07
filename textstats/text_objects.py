import glob
import os
import string


class Text(object):

    """
    Representation of a single text or section of text as a set of tokens.


    The Text class contains information about a single text used in the analysis.
    Each Text object maintains a reference to the original file, as well as core attributes
    (length) and the cleaned and normalized token corpus from the text.

    Attributes
    ----------
    file_path : str or os.path object
        Path to text file on disk.
    proper_name : str
        Capcased name for the text based on a cleaned version of
        `file_path`.
    tokens : list
        A list of cleaned tokens derived from the words in the original
        text file supplied.
    token_count : int
        The number of tokens in `tokens`, equivalent to len(tokens).

    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.proper_name = file_path.split('/')[-1].replace('.txt', '').replace('_', ' ').capitalize()
        self.tokens = []
        self.token_count = 0

    def __str__(self):
        print "{} ({})".format(self.proper_name, self.file_path)

    def _strip_enclitic_que(self, tokens):
        """
        Strip '-que' from words and treat it as a separate stopword
        """
        que_preserve = [
            'atque', 'quoque', 'neque', 'itaque', 'absque',
            'apsque', 'abusque', 'adaeque', 'adusque', 'denique', 'deque',
            'susque', 'oblique', 'peraeque', 'plenisque', 'quandoque',
            'quisque', 'quaeque', 'cuiusque', 'cuique', 'quemque', 'quamque',
            'quaque', 'quique', 'quorumque', 'quarumque', 'quibusque', 'quosque',
            'quasque', 'quotusquisque', 'quousque', 'ubique', 'undique',
            'usque', 'uterque', 'utique', 'utroque', 'utribique', 'torque',
            'coque', 'concoque', 'contorque', 'detorque', 'decoque', 'excoque',
            'extorque', 'obtorque', 'optorque', 'retorque', 'recoque',
            'attorque', 'incoque', 'intorque', 'praetorque'
        ]
        final_tokens = []

        for t in tokens:
            if t.endswith('que') and t not in que_preserve:
                final_tokens.extend([t.replace('que',''), '-que'])
            else:
                final_tokens.append(t)

        return final_tokens

    def load_and_tokenize(self, sep_char=' ', strip_que=False):
        """ Read a file and convert it to tokens

        Load the file specified when initializing the Text class,
        strip and sanitize, and convert into a set of lowercase tokens.
        This function update's the object's `tokens` and `token_count`
        attributes directly.

        Parameters
        ----------
        sep_char : str, default ' '
            Character(s) that delimit tokens, used to split the text
        strip_que : bool, default False
            If True, strip the suffix '-que' from words and treat it
            as its own token. By default, a list of common Latin words
            ending in '-que' will be preserved intact

        Returns
        -------
        None

        """
        with open(self.file_path, 'rU') as inf:
            raw_text = inf.read().replace('\n', '')

        clean_text = ''.join([c for c in raw_text if c not in string.punctuation])

        tokens = [x.lower() for x in clean_text.split(sep_char) if x != '']

        self.tokens = self._strip_enclitic_que(tokens) if strip_que else tokens
        self.token_count = len(self.tokens)


class Corpus(object):
    """ A collection of texts.

    The Corpus class provides a wrapper for managing a collection of texts. It
    pulls in text files from two directories - comparison texts in the 'trial_texts'
    directory and the three sections of the Vita Praiectus from the 'praiectus'
    directory.

    Attributes
    ----------
    corpus_directory : str, default 'texts'
        The base directory path for the project texts.
    comparison_texts : array
        An array of text objects assembled from all distinct text
        files in the 'trial_texts' directory.
    praiectus_texts : array
        An array of text objects assembled from all distinct text
        files in the 'praiectus' directory.

    Returns
    -------
    None

    """

    def __init__(self, corpus_directory='texts'):
        self.corpus_directory = corpus_directory
        self.comparison_texts = self._collect_files_from_directory('trial_texts')
        self.praiectus_texts = self._collect_files_from_directory('praiectus')

    def _collect_files_from_directory(self, d):
        texts = glob.glob(os.path.join(self.corpus_directory, d, '*.txt'))

        return [Text(t) for t in texts]
