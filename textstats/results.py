import datetime
import os

class OutputManager(object):
    """
    Class for managing outputs in a variety of formats

    Attributes
    ----------
    self.output_base_directory : str or os.path object
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

    def __init__(self, output_directory='outputs'):

        if not os.path.exists(output_directory):
            os.mkdir(output_directory)

        self.output_base_directory = output_directory
        self.output_final_directory = None

    def setup(self, iterations, stopwords, percent):
        """

        :param iterations:
        :param stopwords:
        :param percent:
        :param method:
        :return:
        """
        def timestamped(f, fmt='%Y%m%d-%H%M%S_{fname}'):
            return datetime.datetime.now().strftime(fmt).format(fname=f)

        results_directory = timestamped('IT{}_SW{}_PCT{}'.format(iterations, stopwords, int(round(percent * 100))))
        output_dir = os.path.join(self.output_base_directory, results_directory)

        os.mkdir(output_dir)
        self.output_final_directory = output_dir
        return self

    def write_output(self, data):
        """

        :param data:
        :return:
        """
        import pandas as pd
        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_csv(self.output_final_directory)
