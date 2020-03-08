#! /usr/bin/env python3

import argparse as ap
import multiprocessing as mp

import matplotlib.pyplot as plt
import numpy as np

from seqio.Fastq import PairedFastq

plt.style.use('seaborn-whitegrid')

desc = """

A script for plotting nucleotide frequencies across
positions of sequence reads from a fastq file

"""

parser = ap.ArgumentParser(
    prog='plot_nucleotide_distributions.py', description=desc
)

parser.add_argument(
    '-i', "--input_file", type=str, required=True,
    help="The input reads, as a paired, interleaved fastq"
)

parser.add_argument(
    '-o', "--output_prefix", type=str, required=True,
    help="The output filename prefix for the plot (including path)",
)

parser.add_argument(
    '-n', "--number-of-processes",
    help="number of processes to use, default=1",
    type=int, required=False, default=1, dest='n'
)

parser.add_argument(
    '-s', "--sequence_length", type=int, required=True
)

args = parser.parse_args()


fq = PairedFastq(args.input_file)

data = np.zeros((2, 4, args.sequence_length))
d = {'A': 0, 'T': 1, 'G': 2, 'C': 3}

for n, (f, r) in enumerate(fq, start=1):
    enc_f = [d[x] for x in f.seq]
    enc_r = [d[x] for x in r.seq]
    data[0, enc_f, np.arange(len(f))] += 1
    data[1, enc_r, np.arange(len(r))] += 1

data /= n
print(data)

fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
ax[0].set_title("Left Read", fontsize='small')
ax[1].set_title("Right Read", fontsize='small')
ax[0].set_xlabel("Position in Read", fontsize='small')
ax[1].set_xlabel("Position in Read", fontsize='small')
ax[0].set_ylabel("Base Frequency", fontsize='small')

fig.suptitle("Per Base Nucleotide Composition for Paired-End Reads")
labels = list(d.keys())

for x in range(data.shape[0]):
    ax[x].set_ylim(0, 1)
    ax[x].set_xticks(list(range(0, args.sequence_length, 10)))
    ax[x].set_yticks([x/10 for x in range(0,11)])
    for y in range(data.shape[1]):
        ax[x].step(np.arange(args.sequence_length), data[x, y, :], label=labels[y])

    for tick in ax[x].xaxis.get_major_ticks():
        tick.label.set_fontsize(6)
        tick.label.set_rotation(45)

    for tick in ax[x].yaxis.get_major_ticks():
        tick.label.set_fontsize(6)

    ax[x].legend(fontsize='small', frameon=True)

fig.savefig(f"{args.output_prefix}.png", dpi=300)
plt.close(fig)
