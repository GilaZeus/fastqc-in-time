#!/usr/bin/env python3
"""Get accession numbers of sequencings on a single day, print them to stdout,
if called as script.

Usage: ./accnums YYYY/MM/DD"""

import sys
import requests
import re
from datetime import datetime
import urllib
import urllib3
import pandas as pd

# A more clearer name for ValueError in our case.
class WrongArgumentError(ValueError):
    pass


def check_date(date):
    """Gets the date from sys.argv and checks for correct input.
    
    Raise WrongArgumentError if input was incorrect."""
    
    # Check for date format.
    if not re.search(r"\d{4}/\d\d/\d\d", date):
        raise WrongArgumentError("The date must be in YYYY/MM/DD format!")
    
    # Check if date consist of numbers and exists.
    try:
        year, month, day = list(map(int, date.split("/")))
        datetime(year, month, day)
    except ValueError:
        raise WrongArgumentError("The date must consist of numbers and exist!")
    

def accnum_iter(date, min_len=5, max_len=10):
    """Iterator for the first appearances of each sequencing platform for a chosen date.

    Return "platform,release date,accession number"."""
    check_date(date)
    # Build a string for selected appropriate sequencing length.
    mbases = "("
    for i in range(min_len, max_len + 1):
        mbases += "(\"{0:011d}\"[Mbases]) OR ".format(i)
    mbases = mbases[: -4] + ")"
    # Build a search request for all entries on a chosen day.
    search_request = mbases + " AND (\"" + date + \
                     "\"[Publication Date] : \"" + date + "\"[Publication Date]) AND (\""
    
    # List of differen sequencing platforms.
    seq_platforms = ["abi solid", "bgiseq", "capillary", "complete genomics",
                     "helicos", "illumina", "ion torrent", "ls454",
                     "oxford nanopore", "pacbio smrt"]

    for seq_platform in seq_platforms:
        # Send a request and handle connection issues.
        acc_num = None
        while acc_num is None:
            try:
                # Sometimes it gets empty result, so re.search returns None.
                id = None
                while id is None:
                    url = "https://www.ncbi.nlm.nih.gov/sra"
                    s = requests.Session()
                    s.post(url, data = {"term" : search_request + seq_platform + "\"[Platform])"})
                    search = s.get("https://www.ncbi.nlm.nih.gov/sra/advanced")
    
                        # Extract the search-ID.
                    id = re.search(r"MCID_[\w]*", search.text)
                id = id[0]

                # get the first accession number and safe them as text:
                # "platform,release date,accession number"
                acc_num = requests.get("https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&rettype=acclist&db=sra&WebEnv=" +
                                       id + "&query_key=1").text
                acc_num = acc_num[: acc_num.find("\n")]
            except requests.exceptions.ConnectionError:
                pass
        if acc_num != "":
            print(seq_platform, acc_num)
            yield ",".join([seq_platform, date[: - 3], acc_num])
        else:
            continue
            

def get_meta(acc_num):
    """DEPRECATED
    Get run's metadata using its accession number.

    Return (library strategy, release date) or None, if data is not inaccessible or uncoplete."""
    try:
        # Avoid entries without meta data and connection crushes.
        csv = pd.read_csv("https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term=" + acc_num)
    except (pd.errors.EmptyDataError, urllib.error.URLError, OSError) as error:
        return None
    else:
        try:
            # In date field only month and year are interesting for us.
            result = (csv["Platform"][0], csv["ReleaseDate"][0][ : 7], acc_num)
        except KeyError:
            return None
        else:
            return result


def get_all_meta(acc_nums, skip=True):
    """DEPRECATED
    Get meta data for all accession numbers stored as iterable. If skip=True,
    save only the first appearance of a library strategy on this day.

    Return list of strings: "platform,release date,accession number"."""
    result = []
    if skip:
        libs = []
        for acc_num in acc_nums:
            meta = get_meta(acc_num)
            if meta != None and not meta[0] in libs:
                libs.append(meta[0])
                result.append(",".join(meta))
    else:
        for acc_num in acc_nums:
            meta = get_meta(acc_num)
            if meta != None:
                result.append(",".join(meta))
    
    return result


def main():
    # Get the date from sys.argv
    # Check if input is there.
    try:
        date = sys.argv[1]
    except IndexError:
        raise WrongArgumentError("You must submit at least one argument!")
    for acc_num in accnum_iter(date):
        print(acc_num)


if __name__ == "__main__":
    main()
