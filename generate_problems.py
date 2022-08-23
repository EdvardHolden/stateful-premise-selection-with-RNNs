"""Script to extract the predicted axioms from the model and generate the corresponding problem."""

import os
import pickle
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("id_file", help="File containing the problem names of the prediction set")
parser.add_argument("predictions", help="File containing the predictions from the onmt script")


AXIOM_MAP_PATH = "name_axiom_map.pkl"
TOKEN_UNK = "<unk>"
ORIGINAL_DATASET_PATH = "~/gnn-entailment-caption/nndata/"
DEST = "GENERATED_PROBLEMS/"


def get_problem_conjecture(problem_name):

    # Get problem name
    prob_path = os.path.join(ORIGINAL_DATASET_PATH, problem_name)

    # Get the first line - contains the conjecture
    with open(os.path.expanduser(prob_path), "r") as f:
        conj = f.readline()

    conj = conj[1:].replace("axiom", "conjecture", 1).strip()
    return conj


def main():

    args = parser.parse_args()

    # Load problem names to map with the conjecture and name
    with open(args.id_file, "r") as f:
        problem_names = f.read().splitlines()
    print(f"Number of ids: {len(problem_names)}")

    # Load the predictions
    with open(args.predictions, "r") as f:
        predictions = f.read().splitlines()
        print(f"Number of predictions: {len(predictions)}")

    # Check that provided files are roughly in order
    if (len(predictions) % len(problem_names)) != 0:
        raise ValueError("Length of predictions is n times the length of the ids. Provided the wrong files?")

    with open(AXIOM_MAP_PATH, "rb") as f:
        axiom_map = pickle.load(f)

    # Number of predictions per problems
    n_pred = int(len(predictions) / len(problem_names))

    # Get the prediction of each problem and save to file
    for prob_no, prob_name in enumerate(problem_names):
        # Variable to store the axioms for this problem
        axioms = set()
        # Loop over each prediction line in the group
        for pred in predictions[prob_no : prob_no + n_pred]:
            new_axioms = [axiom_map[premise] for premise in pred.split() if premise != TOKEN_UNK]
            axioms = axioms.union(new_axioms)

        # Get the conejcture
        conj = get_problem_conjecture(prob_name)

        with open(os.path.join(DEST, prob_name), "w") as f:
            f.write(conj)
            f.write("\n".join(axioms))


if __name__ == "__main__":
    main()
