import glob
import os
import string


class Text(object):

    QUE_PRESERVE = [
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

    def __init__(self, file_path):
        self.file_path = file_path
        self.proper_name = file_path.split('/')[-1].replace('.txt', '').replace('_', ' ').capitalize()
        self.tokens = []
        self.token_count = 0

    def __str__(self):
        print "{} ({})".format(self.proper_name, self.file_path)

    def _strip_enclitic_que(self, tokens):
        final_tokens = []
        for t in tokens:
            if t.endswith('que') and t not in Text.QUE_PRESERVE:
                final_tokens.append(t.replace('que', ''))
                final_tokens.append('-que')
            else:
                final_tokens.append(t)
        return final_tokens

    def load_and_tokenize(self, sep_char=' ', strip_que=False):
        with open(self.file_path, 'rU') as inf:
            raw_text = inf.read().replace('\n', '')

        clean_text = ''.join([c for c in raw_text if c not in string.punctuation])

        tokens = [x.lower() for x in clean_text.split(sep_char) if x != '']

        self.tokens = self._strip_enclitic_que(tokens) if strip_que else tokens
        self.token_count = len(self.tokens)


class Corpus(object):

    def __init__(self, corpus_directory='texts'):
        self.corpus_directory = corpus_directory
        self.comparison_texts = self._collect_files_from_directory('trial_texts')
        self.praiectus_texts = self._collect_files_from_directory('praiectus')

    def _collect_files_from_directory(self, d):
        texts = glob.glob(os.path.join(self.corpus_directory, d, '*.txt'))

        return [Text(t) for t in texts]
