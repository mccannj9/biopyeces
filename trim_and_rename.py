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
    '-i', "--input_file", type=str, required=False, default='-',
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

parser.add_argument(
    '-l', "--trim_left", type=int, required=False, default=0,
    help="Number of bases to trim from beginning of reads",
)

parser.add_argument(
    '-r', "--trim_right", type=int, required=False, default=0,
    help="Number of bases to trim from end of reads",
)

args = parser.parse_args()

with _smart_open(args.input_file) as handle:
    fq = PairedFastq(handle)
    out = open(f"{args.output_prefix}.fas", "w")

    for n, (f, r) in enumerate(fq, start=1):
        if args.trim_right:
            f.seq = f.seq[args.trim_left:-args.trim_right]
            r.seq = r.seq[args.trim_left:-args.trim_right]
        else:
            f.seq = f.seq[args.trim_left:]
            r.seq = r.seq[args.trim_left:]
        f.name = f"{args.prefix}_{n}l"
        r.name = f"{args.prefix}_{n}r"
        print(
            f"{f.as_fasta_oneline()}\n{r.as_fasta_oneline()}", file=out
        )
    out.close()
