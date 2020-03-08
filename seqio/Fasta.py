#! /usr/bin/env python3

import re


class Fasta(object):
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.buffer = ''
        while not self.buffer.startswith('>'):
            self.consume()
        self.exhausted = False

    def consume(self):
        self.buffer = self.file.readline()
        if self.buffer == '':
            raise StopIteration

    def __next__(self):
        if self.exhausted:
            raise StopIteration

        desc = self.buffer.strip('>').strip()
        self.consume()
        seq = []

        while not self.buffer.startswith('>'):
            seq.append(self.buffer)
            try:
                self.consume()
            except StopIteration:
                self.exhausted = True
                break

        return desc, re.sub(r'\s+', '', ''.join(seq))

    def __iter__(self):
        return self

    def close(self):
        self.file.close()

    def reset(self):
        if not(self.file.closed):
            self.file.seek(0)
            self.exhausted = False
            self.__next__()
