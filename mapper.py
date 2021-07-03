# Work with standard input.
import sys
# Lib to parse run's metadata.
import pandas as pd

# Get the name of the sequencing technology and the date of the sample.
acc_num = sys.stdin.readline().split(".")[0][1 :]
csv = pd.read_csv("https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term=" + acc_num)

date = csv["ReleaseDate"][0][ : 10]
name = csv["LibraryStrategy"][0]

print(name)
print(date)
# every forth line is interesting for us; create a counter.
i = 1

for line in sys.stdin:
    if i == 3:
        # Information on Phred-score encoding in FASTQ-files:
        # http://people.duke.edu/~ccc14/duke-hts-2018/bioinformatics/quality_scores.html
        for char in line:
            print(",".join([name, date, str(ord(char) - 33), "1"]))
        i = 0
    else:
        i += 1
