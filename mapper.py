#!/usr/bin/env python3
"""New mapper for Hadoop.

Be careful, that this mapper function does not sort all values."""

# Work with standard input.
import sys
# Lib to parse run's metadata.
import pandas as pd
# Effective parsing output of fastq-dump.
import subprocess
from functools import reduce


def get_meta(acc_num):
    """Get run's metadata using its accession number.

    Returns (library strategy, release date) or None, if data is not inaccessible or uncoplete."""
    try:
        csv = pd.read_csv("https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term=" + acc_num)
    except pandas.errors.EmptyDataError:
        return None
    else:
        try:
            # In date field only month and year are interesting for us.
            result = (csv["LibraryStrategy"][0], csv["ReleaseDate"][0][ : 7])
        except KeyError:
            return None
        else:
            return result


def read_input(data):
    """An iterator for input data.

    Reads each line from input."""
    for line in data:
        yield line.strip()



def map_fastq(acc_num):
    """Prints output with comma as separator.
    
    Single line of output: "technology name,date,phred score,count"."""
    process = subprocess.Popen(["fastq-dump-orig.2.11.0", "-Z", acc_num], stdout=subprocess.PIPE, bufsize=-1)
    total_phred = 0
    total_len = 0
    i = 0
    while True:
        line = process.stdout.readline()
        line = line.strip().decode("utf-8")

        if line == "":
            break
        
        if i == 3:
            # Information on Phred-score encoding in FASTQ-files:
            # http://people.duke.edu/~ccc14/duke-hts-2018/bioinformatics/quality_scores.html
            total_phred += reduce(lambda x, y: x + y, map(lambda x: ord(x) - 33, line))
            total_len += len(line)
        i += 1
        if i == 4:
            i = 0
    
    process.kill()

    name, date = get_meta(acc_num)    
    print(",".join([name, date, str(total_phred), str(total_len)]))


def main():
    for line in read_input(sys.stdin):
        map_fastq(line.strip())


if __name__ == "__main__":
    main()
