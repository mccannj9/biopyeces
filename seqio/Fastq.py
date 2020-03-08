#! /usr/bin/env python3

from seqio.Sequence import Sequence


class Fastq(object):

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)
        self.data = []
        self.consumed = 0
        self.exhausted = False

    def consume(self):
        self.buffer = self.file.readline()
        if self.buffer == '':
            self.exhausted = True
            raise StopIteration
        self.data.append(self.buffer.strip())

    def __next__(self):
        self.data = []
        if self.exhausted:
            raise StopIteration

        for x in range(4):
            self.consume()

        # removing the '+' line
        if self.data:
            self.data.pop(2)

        self.consumed += 1

        return Sequence(*self.data, file_format='fastq')

    def __iter__(self):
        return self

    def close(self):
        self.file.close()

    def reset(self):
        if not(self.file.closed):
            self.file.seek(0)
            self.__next__()
        else:
            self.file = open(self.filename)

        self.exhausted = False
