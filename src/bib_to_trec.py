# -*- coding: utf-8 -*-

"""Converting bibtex files to a TREC-formatted test collection."""

import os
import gzip
import json
import glob
import argparse
from pybtex.database.input import bibtex

# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--directory",
                    help="input directory with ACM DL bibtex files.",
                    type=str)

parser.add_argument("--output",
                    help="output file in TREC format.",
                    type=str)

parser.add_argument('--path_to_keyphrases',
                    help='path to the (json formatted) keyphrases.',
                    type=str,
                    default=None)

args = parser.parse_args()

# loading keyphrases if provided
if args.path_to_keyphrases:
    with gzip.open(args.path_to_keyphrases, "rt") as f:
        keyphrases = json.loads(f.read())
        print("{} docids loaded for keyphrases".format(len(keyphrases)))

collection = {}
nb_entries = 0
for filename in glob.iglob(args.directory+"/**", recursive=True):
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
                collection[key] = reference

            # dd url
            #url = "https://dl.acm.org/doi/pdf/"+key

        nb_entries += nb_docs

print('{} entries with {} T+A+K'.format(nb_entries, len(collection)))

with gzip.open(args.output, 'wt') as o:
    for doc_id in collection:
        entry = collection[doc_id]
        o.write("<DOC>\n")
        o.write("<DOCNO>{}</DOCNO>\n".format(doc_id))
        o.write("<TITLE>{}</TITLE>\n".format(entry.fields['title'].strip()))
        o.write("<TEXT>{}</TEXT>\n".format(entry.fields['abstract'].strip()))
        if args.path_to_keyphrases and doc_id in keyphrases:
            kps = keyphrases[doc_id]
            kps = [k[0] for k in kps]
            o.write("<HEAD>{}</HEAD>\n".format(' // '.join(kps)))
        o.write("</DOC>\n\n")



