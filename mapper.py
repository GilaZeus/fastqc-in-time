# Work with standard input.
import sys

# Get the name of the sequencing technology and the date of the sample.
acc_num = sys.stdin.readline().split(".")[0][1 :]

csv = urllib.request.urlopen("https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term=" + acc_num)
csv.readline() 
csv = csv.readline().split(",")
name = csv[1]
date = csv[10]

# every forth line is interesting for us; create a counter.
i = 1

for line in sys.stdin:
    if i == 3:
        # Information on Phred-score encoding in FASTQ-files:
        # http://people.duke.edu/~ccc14/duke-hts-2018/bioinformatics/quality_scores.html
        for char in line:
            print(",".join([name, date, ord(char) - 33, 1]))
        i = 0
    else:
        i += 1