#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import sys

from words.interpreter.interpret import Interpreter

if __name__ == '__main__':
    argument_parser = ArgumentParser(description="Words programming language.")
    argument_parser.add_argument("input_file", metavar="I", help="Input file", type=Path)
    args = argument_parser.parse_args()

    sys.setrecursionlimit(4000)

    Interpreter.interpret_file(args.input_file)
