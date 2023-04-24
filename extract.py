#!/usr/bin/python3

import argparse

from core.extractor import StringLiteralExtractor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract string literals from global-metadata.dat"
    )

    parser.add_argument(
        "-i", "--input", required=True, help="Path to global-metadata.dat"
    )
    parser.add_argument("-o", "--output", required=True, help="Path to output file")

    args = parser.parse_args()

    extractor = StringLiteralExtractor(args.input)
    extractor.extract().dump(args.output)

    print("Done!")
