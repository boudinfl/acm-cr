# -*- coding: utf-8 -*-

"""Download pdf files from the bibtex dois."""

import os
import argparse
import requests
from pybtex.database.input import bibtex

# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input bibtex file.",
                    type=str)

parser.add_argument("--output",
                    help="output directory to store pdfs.",
                    type=str)

args = parser.parse_args()

parser = bibtex.Parser()
data = parser.parse_file(args.input)
for key, reference in  data.entries.items():
    #print(key)
    url = "https://dl.acm.org/doi/pdf/"+key
    print(url)
    response = requests.get(url)
    if "application/pdf" in response.headers['Content-Type']:
        pdf_file = args.output + '/' + key + ".pdf"
        os.makedirs(os.path.dirname(pdf_file), exist_ok=True)
        with open(pdf_file, 'wb') as f:
            f.write(response.content)






