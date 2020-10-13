# -*- coding: utf-8 -*-

"""Converting bibtex files to a TREC-formatted test collection."""

import os
import glob
from pybtex.database.input import bibtex


collection = {}
root_path = 'data/acm-dl/**'
#root_path = 'data/acm-dl/chi/cscw/**'
nb_entries = 0

for filename in glob.iglob(root_path, recursive=True):
    if os.path.isfile(filename):
        print('loading documents from {}'.format(filename))
        parser = bibtex.Parser()
        data = parser.parse_file(filename)
        nb_docs = 0

        for key, reference in  data.entries.items():
            nb_docs += 1
            if reference.type not in ["inproceedings", "article"]:
                continue

            if {'title', 'abstract', 'keywords'} <= set(reference.fields):
                #collection[key] = reference
                collection[key] = {}

            # dd url
            #url = "https://dl.acm.org/doi/pdf/"+key

            #print(key)
            #print(url)

            #exit(0)

        nb_entries += nb_docs

print('{} entries in total'.format(nb_entries))
print('{} documents in total'.format(len(collection)))


