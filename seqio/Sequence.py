#! /usr/bin/env python3

import textwrap


rclookup = {
    'a': 't', 't': 'a', 'g': 'c', 'c': 'g',
    'w': 'w', 's': 's', 'm': 'k', 'k': 'm',
    'r': 'y', 'y': 'r', 'b': 'v', 'd': 'h',
    'h': 'd', 'v': 'b', 'n': 'n', 'A': 'T',
    'T': 'A', 'G': 'C', 'C': 'G', 'W': 'W',
    'S': 'S', 'M': 'K', 'K': 'M', 'R': 'Y',
    'Y': 'R', 'B': 'V', 'D': 'H', 'H': 'D',
    'V': 'B', 'N': 'N', "-": "-"
}


class Sequence:

    """Sequence object that can be used for generating sequence objects 
       from fasta files, things can be added as needed for other applications"""

    def __init__(self, name="", seq="", qual="", file_format=None):
        self.name = name
        self.seq = seq
        self.qual = qual
        self.file_format = file_format
        self.is_revcomp = False

    def check_duplicate(self, other):
        return self.seq == other.seq

    def reverse_complement(self):
        tmp_seq = ""

        for base in self.seq[::-1]:
            tmp += rclookup[base]
            self.seq = tmp_seq

            if file_format == 'fastq':
                self.qual = self.qual[::-1]

        self.is_revcomp = not(self.is_revcomp)

    def as_fasta_oneline(self):
        return ">%s\n%s" % (self.name, self.seq)

    def as_fasta_wrapped(self, w=80):
        return f">{self.name}\n{textwrap.fill(self.seq, width=w)}"

    def as_fastq(self):
        if not(self.qual):
            self.qual = len(self.seq) * "I"

    def __str__(self):
        return f"name: {self.name}\nseq: {self.seq}"

    def __repr__(self):
        return f"name: {self.name}\nseq: {self.seq}"

    def __len__(self):
        return len(self.seq)

    def __eq__(self, other):
        return self.name == other.name
