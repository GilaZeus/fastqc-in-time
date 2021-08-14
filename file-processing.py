#!/usr/bin/env python3
import subprocess
import sys

def get_month(file_name):
    """Safe all FASTQ-files from a month file's entries.
    
    Save results in ~/tmp."""
    with open(file_name) as data:
        for line in data:
            acc_num = line.strip().split(",")[2]
            subprocess.run(["fasterq-dump", acc_num, "-O ~/tmp"])


def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        raise WrongArgumentError("You must submit at least one argument!")
    get_month(file_name)


if __name__ == "__main__":
    main()