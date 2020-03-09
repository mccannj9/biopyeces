#! /usr/bin/env python3

import argparse as ap

from seqio.Fastq import PairedFastq
from utils.misc import _smart_open


desc = """

A script for trimming and renaming reads as last step
in preparation for input to the RepeatExplorer pipeline.

"""

parser = ap.ArgumentParser(
    prog='trim_and_rename.py', description=desc
)

parser.add_argument(
    '-i', "--input_file", type=str, required=False, default='-'
    help="The input reads, as a paired, interleaved fastq, default = stdin"
)

parser.add_argument(
    '-p', "--prefix", type=str, required=True,
    help="Prefix to use for each read in the output file",
)

parser.add_argument(
    '-o', "--output_prefix", type=str, required=True,
    help="The output filename prefix for the plot (including path)",
)

args = parser.parse_args()
