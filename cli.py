#!/bin/python3

import argparse
import json

from api.cli.main import run

parser = argparse.ArgumentParser(description="process a blockchain json file and outputs the overall balance for every account")
parser.add_argument('file', metavar='file', type=str, help="the blockchain json file")
parser.add_argument('--median', action="store_true", help="shows the median instead of the balance")
args = parser.parse_args()

print(json.dumps(run(args.file, args.median)))
