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

    return parser.parse_args()