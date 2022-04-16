#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import sys

from words.compiler.compile import Compiler
from words.interpreter.interpret import Interpreter

if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description="Words programming language.")
    argument_parser.add_argument("input_file", help="Path to the input file.", type=Path)
    argument_parser.add_argument("--native", metavar="N", nargs="?", choices=["Cortex-M0"],
                                 help="If provided, will compile the program to run natively on target.")
    argument_parser.add_argument("--init", metavar="S", nargs="+",
                                 help="If provided, will place the following values in an initial stack")
    args = argument_parser.parse_args()

    sys.setrecursionlimit(4000)
    init = []
    if "init" in args and args.init is not None:
        init = args.init

    if args.native is not None:
        output_dir = Path("src/words/compiler/native_due/src")

        src = Compiler.compile_file(args.input_file, target=args.native)

        with open(output_dir / "my_words_script.S", "w") as output_file:
            output_file.write(src)

        subprocess.run(["pio", "run", "--environment", "due", "--target", "upload", "--upload-port", "/dev/ttyACM0"],
                       cwd=output_dir / "..")
    else:
        Interpreter.interpret_file(args.input_file, init=init)
