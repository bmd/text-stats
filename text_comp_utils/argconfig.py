import argparse


def read_configuration_options():
    """
    Set up and validate command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'iterations',
        type=int,
        help='Number of times to run the simulation for each text.'
    )
    parser.add_argument(
        'stopwords',
        type=int,
        help='Use top N words of text 1'
    )
    parser.add_argument(
        'sample',
        type=float,
        help='Percent of text to sample'
    )
    parser.add_argument(
        'method',
        type=str,
        choices=['chisquare', 'gtest'],
        help='Statistical test for generating results'
    )
    parser.add_argument(
        '--stem',
        type=str,
        choices=['naive', 'schinke'],
        help='Choose a method for stemming tokens in source texts. NOT IMPLEMENTED'
    )
    parser.add_argument(
        '--strip-que',
        action='store_true',
        help='Strip the enclitic que and treat it as a separate stopword'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Output more text'
    )
    return parser.parse_args()
