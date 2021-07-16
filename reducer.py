#!/usr/bin/env python3
"""Reducer for Hadoop.

Be careful, that it cannot work outside of Hadoop's environment:
The mapper function must also sort all values."""

# Work with standard input.
import sys
# Libs to sort input.
from itertools import groupby
from operator import itemgetter

def read_mapper_output(data):
    """Reads output of a mapper.
    
    Espects "library strategy,year-month,Phred-score,count",
    returns them splitted by comma."""
    for line in data:
        yield line.strip().split(",")


def main():
    """Reduces mapper's output. Calculates average Phred-score for each month.
    Ignores wrong input.
    
    Output: "Sequencing technology,date,average Phred-score"."""
    data = read_mapper_output(sys.stdin)
    for current_month, group in groupby(data, itemgetter(0, 1)):
        try:
            total_phred = 0
            total_len = 0
            for item in group:
                total_phred += int(item[-2])
                total_len += int(item[-1])
            print(",".join([item[0], item[1], str(total_phred), str(total_len)]))
        except:
            pass
        


main()
