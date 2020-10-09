# -*- coding: utf-8 -*-

"""Converting bibtex files to a TREC-formatted test collection."""

import os
import glob
from pybtex.database.input import bibtex


collection = {}

for filename in glob.iglob('data/acm-dl/**', recursive=True):
    if os.path.isfile(filename):
        print('loading documents from {}'.format(filename))
        parser = bibtex.Parser()
        data = parser.parse_file(filename)

        for key, reference in  data.entries.items():
            if reference.type != "inproceedings":
                continue
            if {'title', 'abstract', 'keywords'} <= set(reference.fields):
                collection[key] = reference

            # dd url
            url = "https://dl.acm.org/doi/pdf/"+key

            print(key)
            print(url)

            exit(0)

        print('{} documents in total'.format(len(collection)))


