#!/usr/bin/env python3
"""Get accession numbers of sequencings on a single day, print them to stdout.

Usage: ./accnums YYYY/MM/DD"""

import sys
import requests
import re
from datetime import datetime

# A more clearer name for ValueError in our case.
class WrongArgumentError(ValueError):
    pass


def get_date():
    """Gets the date from sys.argv and checks for correct input.
    
    Raises WrongArgumentError if input was incorrect."""
    # Check if input is there.
    try:
        date = sys.argv[1]
    except IndexError:
        raise WrongArgumentError("You must submit at least one argument!")
    
    # Check for date format.
    if not re.search(r"\d{4}/\d\d/\d\d", date):
        raise WrongArgumentError("The date must be in YYYY/MM/DD format!")
    
    # Check if date consist of numbers and exists.
    try:
        year, month, day = list(map(int, date.split("/")))
        datetime(year, month, day)
    except ValueError:
        raise WrongArgumentError("The date must consist of numbers and exist!")
    
    return date
    


def main():
    # Get the date from sys.argv
    date = get_date()
    # Build a search request for all entries on a chosen day.
    search_request = "(\"" + date + "\"[Publication Date] : \"" + date + "\"[Publication Date] NOT 0[Mbases])"
    
    # Send a request.
    url = "https://www.ncbi.nlm.nih.gov/sra"
    s = requests.Session()
    s.post(url, data = {"term" : search_request})
    search = s.get("https://www.ncbi.nlm.nih.gov/sra/advanced")
    
    # Extract the search-ID.
    id = re.search(r"MCID_[\w]*", search.text)[0]

    # get the accession numbers and print them as text.
    acc_nums = requests.get("https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&rettype=acclist&db=sra&WebEnv=" + id + "&query_key=1")
    print(acc_nums.text)


if __name__ == "__main__":
    main()
