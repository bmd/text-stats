import argparse


def read_configuration_options():
    """
    Set up and validate command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'iterations',
        type=str,
        help='Number of times to run the simulation for each text.'
    )
    parser.add_argument(
        'sample',
        type=float,
        help='Percent of text to sample'
    )
    parser.add_argument(
        '--absolute',
        action='store_true',
        help='Whether sample is an absolute number of words to sample or a percentage'
    )
    return parser.parse_args()