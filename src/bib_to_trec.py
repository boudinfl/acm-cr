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

parser.add_argument('--blacklist',
                    help='path to a blacklist of files.',
                    type=str,
                    default=None)

parser.add_argument('--collection',
                    help='path to a doc_ids collection.',
                    type=str,
                    default=None)

args = parser.parse_args()

# loading a blacklist if provided
blacklist = {}
if args.blacklist:
    with open(args.blacklist, "rt") as f:
        blacklist = f.read().splitlines()
        print("{} docids loaded for blacklist".format(len(blacklist)))

collection = {}
for filename in glob.iglob(args.directory+"/**", recursive=True):
    if os.path.isfile(filename):
        print('loading documents from {}'.format(filename))
        parser = bibtex.Parser()
        data = parser.parse_file(filename)

        for key, reference in  data.entries.items():
            if reference.type not in ["inproceedings", "article"]:
                continue

            if key in blacklist:
                continue

            collection[key] = reference

            # dd url
            #url = "https://dl.acm.org/doi/pdf/"+key
        #break

with gzip.open(args.output, 'wt') as o:
    for doc_id in collection:
        entry = collection[doc_id]
        o.write("<DOC>\n")
        o.write("<DOCNO>{}</DOCNO>\n".format(doc_id))
        o.write("<TITLE>{}</TITLE>\n".format(entry.fields['title'].strip()))
        if 'abstract' in entry.fields:
            o.write("<TEXT>{}</TEXT>\n".format(entry.fields['abstract'].strip()))
        if 'keywords' in entry.fields:
            o.write("<HEAD>{}</HEAD>\n".format(entry.fields['keywords'].strip()))
        o.write("</DOC>\n\n")

# writing doc_ids if necessary
if args.collection:
    with open(args.collection, "wt") as o:
        o.write('\n'.join(collection.keys()))





