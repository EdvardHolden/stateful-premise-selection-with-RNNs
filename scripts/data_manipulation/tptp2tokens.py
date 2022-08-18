#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(
    description="It produces a tokenized version of TPTP by adding and removing spaces. It likely doesn't work correctly..."
)

parser.add_argument("file", help="input TPTP file")
parser.add_argument(
    "--remove_end_space",
    action="store_true",
    help="it removes the last space after full stop (default: False)",
)


tptp_conns_orig = ["<=>", "<~>", "=>", "<=", "~|", "~&", "!=", "$t", "$f"]
tptp_conns = [" ".join(conn) for conn in tptp_conns_orig]
tptp_conns_dict = dict(zip(tptp_conns, tptp_conns_orig))


def tokenize_line(line, remove_end_space=False):

    if remove_end_space:
        line = line[:-1]

    line_list = []
    line_token = ""
    for ch in line:
        if ch == " ":
            if line_token:
                line_list.append(line_token)
                line_token = ""
        elif str.isalnum(ch) or (ch == "_"):
            line_token += ch
        else:
            if line_token:
                line_list.append(line_token)
                line_token = ""
            line_list.append(ch)

    out_str = " ".join(line_list)

    for conn in tptp_conns:
        if conn in out_str:
            out_str = out_str.replace(conn, tptp_conns_dict[conn])

    if remove_end_space:
        print(out_str)
    else:
        print(out_str, end="")


def main():
    """Run main for generating tokens for all the formulas in a file"""
    # Parse input arguments

    args = parser.parse_args()
    with open(args.file) as f:
        for line in f:

            tokenize_line(line, remove_end_space=args.remove_end_space)


if __name__ == "__main__":
    main()
