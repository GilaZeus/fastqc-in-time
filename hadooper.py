#!/usr/bin/env python3
"""Run hadoop separately for each subfolder."""
import subprocess
import os
import sys


def hadoop_call(input_folder="tmp", result_folder="result",
                mapper="fastqc-in-time/mapper.py",
                reducer="fastqc-in-time/reducer.py"):
    """Call hadoop for data in input_folder, safe it under result_folder."""
   
    subprocess.run(["hadoop", "jar", "hadoop-3.3.1/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar", 
                    "-archives", "fastq.tar", "-file", mapper, "-file", reducer,
                    "-mapper", mapper[mapper.find("/") + 1 :], "-reducer", reducer[reducer.find("/") + 1 :],
                    "-input", input_folder + "/*",  "-output", result_folder])


def hadoop_chain(input_folder="tmp", result_folder="result",
                 mapper="fastqc-in-time/mapper.py",
                 reducer="fastqc-in-time/reducer.py"):
    """Chain hadoop for subfolders in folder."""
    
    subfolders = os.listdir(input_folder)
    for subfolder in subfolders:
        if os.path.isdir(input_folder + "/" + subfolder):
            hadoop_call(input_folder=input_folder + "/" + subfolder,
                        result_folder=result_folder + "/" + subfolder,
                        mapper=mapper, reducer=reducer)


def main():
    input_folder, result_folder = sys.argv[1 :]
    hadoop_chain(input_folder=input_folder, result_folder=result_folder)


if __name__ == "__main__":
    main()