#!/usr/bin/env python3
"""FASTQ-files do not contain meta info: so we must store it somewhere,
if we work directly with fastq-files. for faster work I decided to
pickle them in a dictionary."""
import sys
import pickle
import os

def main():
    folder = sys.argv[1]
    meta = {}
    for month in os.listdir(folder):
        month = folder + "/" + month
        if os.path.isfile(month):
            with open(month) as data:
                for line in data:
                    line = line.strip().split(",")
                    meta[line[2]] = line[: 2]
    
    with open("meta.dat", "wb") as data:
        pickle.dump(meta, data)

if __name__ == "__main__":
    main()