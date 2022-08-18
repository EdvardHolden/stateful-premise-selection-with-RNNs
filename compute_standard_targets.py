import os
import argparse


import config
from scripts.data_manipulation.tptp2tokens import tokenize_line

parser = argparse.ArgumentParser()
parser.add_argument("id_file", help="Path to the problem ids")


def main():

    # Get arguments
    args = parser.parse_args()

    """
    # Get problem paths
    problem_paths = glob.glob(os.path.join(config.ORIGINAL_DATASET, "*"))
    """
    # TODO do not operate on paths! Need to do this with based on paths of ids
    with open(args.id_file, "r") as f:
        ids = f.read().splitlines()

    # Loop over each problem
    for prob_id in ids:
        # Get hold of the conjecture
        with open(os.path.join(config.ORIGINAL_DATASET, prob_id), "r") as f:
            conj = f.readline()[1:].strip()

        # Only get the formula
        conj = conj.split("axiom,")[1][:-2].strip()

        # Tokenize - and output to stdout
        tokenize_line(conj)
        print("\n", end="")


if __name__ == "__main__":
    main()
