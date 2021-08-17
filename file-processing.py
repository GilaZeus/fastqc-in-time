#!/usr/bin/env python3
import subprocess
import sys
import os
"""Usage: ./file-processing.py name,
   where name = file with month's entries or folder with multiple month files."""


def get_month(file_name, separator=";LINE;;"):
    """Safe all FASTQ-files from a month file's entries in a new format.
    
    Save results in /tmp."""
    with open(file_name) as data:
        for line in data:
            fastq_transform(line, separator=separator)


def fastq_transform(entry, separator=";;LINE;;"):
    """Safe FASTQ-files in new format in /tmp.
    
    The standard TextInputFormat of Hadoop processes each line separately, but FASTQ-format
    contains multiple 4-line records.  So it is important to write a new TextInputFormat or
    to safe the FASTQ-files in new format, which packs every run in a single line."""
    acc_num = entry.strip().split(",")[2]
    
    with open("tmp/" + acc_num + ".fasth", "w") as data:
        process = subprocess.Popen(["fastq-dump-orig.2.11.0", "-Z", acc_num],
                                   stdout=subprocess.PIPE, bufsize=-1)
        i = 0
        while True:
            line = process.stdout.readline()
            line = line.strip().decode("utf-8")
            if line == "":
                break
            
            # New format:
            # first lineSEPARATORsecond lineSEPARATORforth line\n
            data.write(line)
            if i == 3:
                data.write("\n")
                i = 0
            elif i == 0 or i == 1:
                data.write(separator)
                i += 1
            else:
                i += 1

        process.kill()


def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        raise WrongArgumentError("You must submit at least one argument!")
    
    if os.path.isfile(file_name):
        get_month(file_name)
    elif os.path.isdir(file_name):
        for month in os.listdir(file_name):
            get_month(file_name + "/" + month)
    else:
        raise WrongArgumentError("Such file or directory does not exist!")


if __name__ == "__main__":
    main()