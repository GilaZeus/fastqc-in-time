#!/usr/bin/env python3
"""Mapper for Hadoop. Gets data from the harddrive.

Be careful, that this mapper function does not sort all values."""

# Work with standard input.
import sys
# Effective parsing output of fastq-dump.
from functools import reduce
# For pickled meta data.
import pickle
# Extracting accession number.
import re



def map_fastq(entry, meta, separator=";;LINE;;"):
    """Prints output with comma as separator.
    
    Single line of output:
        "technology name,date,phred score,count"."""
    acc_num, quality = entry.split(separator)[:: 2]
    acc_num = re.search(r"@.*\.", acc_num)[0][1 : -1]
    name, date = meta[acc_num]
    total_phred = reduce(lambda x, y: x + y, map(lambda x: ord(x) - 33, quality))
    total_len = len(quality)
    
    print(",".join([name, date, str(total_phred), str(total_len)]))


def main():
    meta = pickle.load(open("meta.dat", "rb"))
    for line in read_input(sys.stdin):
        map_fastq(line.strip(), meta)


if __name__ == "__main__":
    main()
