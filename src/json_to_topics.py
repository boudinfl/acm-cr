# -*- coding: utf-8 -*-

"""Converting bibtex files to a TREC-formatted test collection."""

import sys
import json

#json_path = 'data/open-access-papers/3397271.3401032.pdf.json'

with open(sys.argv[1], 'r') as f:
    content = f.read()
    parse = json.loads(content)
    #print(parse["name"])
    for i, reference in enumerate(parse["metadata"]["references"]):
        print("{}\tXXX".format(reference["citeRegEx"]))
        print(reference["title"], reference["venue"], reference["year"])

