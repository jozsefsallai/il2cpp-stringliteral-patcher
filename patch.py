#!/usr/bin/python3

import argparse

from core.patcher import StringLiteralPatcher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Patch string literals in global-metadata.dat"
    )

    parser.add_argument(
        "-i", "--input", required=True, help="Path to original global-metadata.dat"
    )
    parser.add_argument("-p", "--patch", required=True, help="Path to patch file")
    parser.add_argument(
        "-o", "--output", required=True, help="Path to output global-metadata.dat"
    )

    args = parser.parse_args()

    patcher = StringLiteralPatcher(args.input, args.patch)
    patcher.update().patch(args.output)

    print("Done!")
