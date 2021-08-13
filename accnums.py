#!/usr/bin/env python3
"""Get accession numbers of sequencings on a single day, print them to stdout,
if called as script.

Usage: ./accnums YYYY/MM/DD"""

import sys
import requests
import re
from datetime import datetime
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
    

def get_accnums_body(date):
    """Get all accnums for a chosen date.

    Return plain text with accnums."""
    check_date(date)

    # Build a search request for all entries on a chosen day.
    search_request = "((txid2697049[Organism:noexp] NOT 0[Mbases)) AND (\"" + date + "\"[Publication Date] : \"" + date + "\"[Publication Date])"
    
    # Send a request.
    url = "https://www.ncbi.nlm.nih.gov/sra"
    s = requests.Session()
    s.post(url, data = {"term" : search_request})
    search = s.get("https://www.ncbi.nlm.nih.gov/sra/advanced")
    
    # Extract the search-ID.
    id = re.search(r"MCID_[\w]*", search.text)[0]

    # get the accession numbers and print them as text.
    acc_nums = requests.get("https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&rettype=acclist&db=sra&WebEnv=" + id + "&query_key=1")

    return acc_nums.text


def get_accnums_as_list(date):
    return get_accnums_body(date).split("\n")


def get_meta(acc_num):
    """Get run's metadata using its accession number.

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
    """Get meta data for all accession numbers stored as iterable. If skip=True,
    save only the first appearance of a library strategy on this day.

    Return list of strings: "library strategy,release date,accession number"."""
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
    acc_nums = get_accnums_body(date)
    print(acc_nums)


if __name__ == "__main__":
    main()
