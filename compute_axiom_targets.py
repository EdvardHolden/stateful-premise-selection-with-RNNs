import os

import config
from compute_standard_conjecture_input import get_ids, get_id_parser


def main():

    args = get_id_parser().parse_args()

    # Load ids
    ids = get_ids(args.id_file)

    for prob_id in ids:
        # Read the whole problem
        with open(os.path.join(config.ORIGINAL_DATASET, prob_id), "r") as f:
            prob = f.read().splitlines()

        # Get hold of positive axioms
        delim = int((len(prob) + 1) / 2)
        prob = prob[1:delim]

        # Extract the axiom names
        ax_names = [ax_name.split(",")[0].split("(")[1] for ax_name in prob]

        # Sort by built-in to get a consistent order
        ax_names = sorted(ax_names)

        # Report
        print(" ".join(ax_names))


if __name__ == "__main__":
    main()
