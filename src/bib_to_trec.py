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

parser.add_argument('--blacklist',
                    help='path to a blacklist of files.',
                    type=str,
                    default=None)

args = parser.parse_args()

# loading keyphrases if provided
keyphrases = {}
if args.path_to_keyphrases:
    with gzip.open(args.path_to_keyphrases, "rt") as f:
        keyphrases = json.loads(f.read())
        print("{} docids loaded for keyphrases".format(len(keyphrases)))

# loading a blacklist if provided
blacklist = {}
if args.blacklist:
    with open(args.blacklist, "rt") as f:
        blacklist = f.read().splitlines()
        print("{} docids loaded for blacklist".format(len(blacklist)))

collection = {}
nb_entries_with_t = 0
nb_entries_with_t_a = 0
nb_entries_with_t_a_k = 0
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

            if {'title', 'abstract', 'keywords'} <= set(reference.fields):
                nb_entries_with_t_a_k += 1
            elif {'title', 'abstract'} <= set(reference.fields):
                nb_entries_with_t_a += 1
            else:
                nb_entries_with_t += 1

            # dd url
            #url = "https://dl.acm.org/doi/pdf/"+key

print('{} T+A+K, {} T+A, {} T over {} entries'.format(nb_entries_with_t_a_k, nb_entries_with_t_a, nb_entries_with_t, len(collection)))

with gzip.open(args.output, 'wt') as o:
    for doc_id in collection:
        entry = collection[doc_id]
        o.write("<DOC>\n")
        o.write("<DOCNO>{}</DOCNO>\n".format(doc_id))
        o.write("<TITLE>{}</TITLE>\n".format(entry.fields['title'].strip()))
        if 'abstract' in entry.fields:
            o.write("<TEXT>{}</TEXT>\n".format(entry.fields['abstract'].strip()))
        if doc_id in keyphrases:
            kps = keyphrases[doc_id]
            kps = [k[0] for k in kps]
            o.write("<HEAD>{}</HEAD>\n".format(' // '.join(kps)))
        o.write("</DOC>\n\n")



