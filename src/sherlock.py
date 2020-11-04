# -*- coding: utf-8 -*-

"""Sherlock the collection."""

import os
import sys
import glob
from pybtex.database.input import bibtex
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# For looking at qrels intersect collection

# qrels = set()
# for line in open(sys.argv[1], 'r'):
#     qrels.add(line.split()[2])

# for venue in glob.iglob(sys.argv[2]+"/*"):
#     print(venue)
#     nb_docs = 0
#     nb_docs_with_kw = 0
#     for instance in glob.iglob(venue+"/*.bib"):
#         parser = bibtex.Parser()
#         data = parser.parse_file(instance)
        
#         for key, reference in  data.entries.items():
#             nb_docs += 1 
#             if {'title', 'abstract', 'keywords'} <= set(reference.fields):
#                 nb_docs_with_kw += 1

#         if qrels & set(data.entries.keys()):
#             print('--', instance, 'OK')
#     print(nb_docs_with_kw/nb_docs)
