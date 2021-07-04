# Work with standard input.
import sys
# Lib to parse run's metadata.
import pandas as pd


def get_meta(acc_num):
    """Get run's metadata using its accession number.

    Returns (library strategy, release date) or None, if data is not inaccessible or uncoplete."""
    try:
        csv = pd.read_csv("https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term=" + acc_num)
    except pandas.errors.EmptyDataError:
        return None
    else:
        try:
            # In data field only month and year are interesting for us.
            result = (csv["LibraryStrategy"][0], csv["ReleaseDate"][0][ : 7])
        except KeyError:
            return None
        else:
            return result


def get_acc_num(line):
    """Extracts accession number from a (line, its position).
    
    Raises ValueError, if line is not a header."""
    if line[1] == 0 or line[1] == 2:
        return line[0].split(".")[0][1 :]
    else:
        raise ValueError("Line is not a header!")


def read_input(data):
    """An iterator for input data.

    Counts every block of FASTQ-file and returns (line, its position):
    0: header
    1: sequence
    2: second header
    3: quality"""
    i = -1
    for line in data:
        if i == 3:
            i = 0
        else:
            i += 1
        yield (line.strip(), i)


def main():
    # Prints output with comma as separator.
    fastq = read_input(sys.stdin)
    acc_num = get_acc_num(next(fastq))
    name, date = get_meta(acc_num)
    for line in fastq:
        if line[1] == 3:
            for char in line[0]:
                # Information on Phred-score encoding in FASTQ-files:
                # http://people.duke.edu/~ccc14/duke-hts-2018/bioinformatics/quality_scores.html
                print(",".join([name, date, str(ord(char) - 33), "1"]))


if __name__ == "__main__":
    main()
