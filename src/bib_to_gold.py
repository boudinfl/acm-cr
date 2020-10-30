# -*- coding: utf-8 -*-

"""Extracting keyphrases from bibtex files."""

import os
import gzip
import json
import glob
import argparse
from pybtex.database.input import bibtex
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import defaultdict


# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--directory",
                    help="input directory with ACM DL bibtex files.",
                    type=str)

parser.add_argument("--output",
                    help="output file in json format.",
                    type=str)

args = parser.parse_args()


def tokenize(s):
    """Tokenize an input text."""
    return word_tokenize(s)


def lowercase_and_stem(_words):
    """lowercase and stem sequence of words."""
    return [PorterStemmer().stem(w.lower()) for w in _words]


def contains(subseq, inseq):
    return any(inseq[pos:pos + len(subseq)] == subseq for pos in
               range(0, len(inseq) - len(subseq) + 1))


# initialize gold annotation sub-containers
all_kps = defaultdict(list)
present_kps = defaultdict(list)
absent_kps = defaultdict(list)
absent_kps_case_1 = defaultdict(list)
absent_kps_case_2 = defaultdict(list)
absent_kps_case_3 = defaultdict(list)
present_and_case_1_kps = defaultdict(list)
absent_case_2_and_3_kps = defaultdict(list)

# initialize fold annotation statistics containers
sum_ratio_present_kps = 0
sum_ratio_absent_kps = 0
sum_ratio_absent_kps_case_1 = 0
sum_ratio_absent_kps_case_2 = 0
sum_ratio_absent_kps_case_3 = 0
nb_documents_with_kps = 0
nb_kps = 0

exp_ratio_case_2 = 0
exp_ratio_case_3 = 0
exp_ratio_case_2_and_3 = 0

for filename in glob.iglob(args.directory+"/**", recursive=True):

    if os.path.isfile(filename):
        print('loading documents from {}'.format(filename))
        parser = bibtex.Parser()
        data = parser.parse_file(filename)
        nb_docs = 0

        for doc_id, reference in  data.entries.items():
            nb_docs += 1
            if reference.type not in ["inproceedings", "article"]:
                continue

            if {'title', 'abstract', 'keywords'} <= set(reference.fields):

                keywords = reference.fields['keywords'].split(',')
                keywords = [kp.strip() for kp in keywords]
                tok_kw = [tokenize(kp) for kp in keywords]
                pp_kw = [lowercase_and_stem(kp) for kp in tok_kw]

                pp_ti = lowercase_and_stem(tokenize(reference.fields['title']))
                pp_ab = lowercase_and_stem(
                    tokenize(reference.fields['abstract']))

                nb_present_kps = 0
                nb_absent_kps = 0
                nb_absent_kps_case_1 = 0
                nb_absent_kps_case_2 = 0
                nb_absent_kps_case_3 = 0
                words_present = []
                words_absent = []

                # loop through the keyphrases
                for j, kp in enumerate(pp_kw):

                    keyphrase = keywords[j]
                    nb_kps += 1

                    # keyphrase is present
                    if contains(kp, pp_ti) or contains(kp, pp_ab):
                        present_kps[doc_id].append([keyphrase])
                        present_and_case_1_kps[doc_id].append([keyphrase])
                        all_kps[doc_id].append([keyphrase])
                        nb_present_kps += 1
                        words_present.extend(keyphrase)

                    # keyphrase is absent
                    else:
                        absent_kps[doc_id].append([keyphrase])
                        all_kps[doc_id].append([keyphrase])
                        nb_absent_kps += 1

                        nb_present_words = 0
                        for word in kp:
                            if word in pp_ti or word in pp_ab:
                                nb_present_words += 1
                                words_present.append(word)
                            else:
                                words_absent.append(word)

                        # Case 1: every word but not the sequence
                        if nb_present_words == len(kp):
                            absent_kps_case_1[doc_id].append([keyphrase])
                            present_and_case_1_kps[doc_id].append([keyphrase])
                            nb_absent_kps_case_1 += 1

                        # Case 2: some words appear
                        elif nb_present_words > 0:
                            absent_kps_case_2[doc_id].append([keyphrase])
                            absent_case_2_and_3_kps[doc_id].append([keyphrase])
                            nb_absent_kps_case_2 += 1

                        # Case 3: no word appears
                        else:
                            absent_kps_case_3[doc_id].append([keyphrase])
                            absent_case_2_and_3_kps[doc_id].append([keyphrase])
                            nb_absent_kps_case_3 += 1

                sum_ratio_present_kps += nb_present_kps / len(keywords)
                sum_ratio_absent_kps += nb_absent_kps / len(keywords)
                sum_ratio_absent_kps_case_1 += nb_absent_kps_case_1 / len(
                        keywords)
                sum_ratio_absent_kps_case_2 += nb_absent_kps_case_2 / len(
                        keywords)
                sum_ratio_absent_kps_case_3 += nb_absent_kps_case_3 / len(
                        keywords)
                nb_documents_with_kps += 1
                exp_ratio_case_2_and_3 += len(set(words_absent)) / (
                            len(set(words_absent)) + len(set(words_present)))


print('{} entries with T+A+K'.format(len(all_kps)))

with gzip.open(args.output + '.all.json.gz', 'wt') as o:
    o.write(json.dumps(all_kps, indent=4, sort_keys=True))

with gzip.open(args.output + '.pres.json.gz', 'wt') as o:
    o.write(json.dumps(present_kps, indent=4, sort_keys=True))

with gzip.open(args.output + '.abs.json.gz', 'wt') as o:
    o.write(json.dumps(absent_kps, indent=4, sort_keys=True))

with gzip.open(args.output + '.abs_c1.json.gz', 'wt') as o:
    o.write(json.dumps(absent_kps_case_1, indent=4, sort_keys=True))

with gzip.open(args.output + '.abs_c2.json.gz', 'wt') as o:
    o.write(json.dumps(absent_kps_case_2, indent=4, sort_keys=True))

with gzip.open(args.output + '.abs_c3.json.gz', 'wt') as o:
    o.write(json.dumps(absent_kps_case_3, indent=4, sort_keys=True))

with gzip.open(args.output + '.pres+abs_c1.json.gz', 'wt') as o:
    o.write(json.dumps(present_and_case_1_kps, indent=4, sort_keys=True))

with gzip.open(args.output + '.abs_c2+abs_c3.json.gz', 'wt') as o:
    o.write(json.dumps(absent_case_2_and_3_kps, indent=4, sort_keys=True))

# print out some stats
print("present: {}".format(sum_ratio_present_kps/nb_documents_with_kps))
print("absent: {}".format(sum_ratio_absent_kps/nb_documents_with_kps))
print("|-> c1/Reordored (i.e. all words): {}".format(sum_ratio_absent_kps_case_1/nb_documents_with_kps))
print("|-> c2/Mixed (i.e. some words): {}".format(sum_ratio_absent_kps_case_2/nb_documents_with_kps))
print("|-> c3/Unseen (i.e. no words): {}".format(sum_ratio_absent_kps_case_3/nb_documents_with_kps))
print("|-> exp. : {}".format(exp_ratio_case_2_and_3/nb_documents_with_kps))
print("avg nb kps : {}".format(nb_kps/nb_documents_with_kps))

#print("nb_documents_with_kps: {}".format(nb_documents_with_kps))
#print("sum_ratio_present_kps: {}".format(sum_ratio_present_kps))
#print("sum_ratio_absent_kps: {}".format(sum_ratio_absent_kps))
#print("sum_ratio_absent_kps_case_1: {}".format(sum_ratio_absent_kps_case_1))
#print("sum_ratio_absent_kps_case_2: {}".format(sum_ratio_absent_kps_case_2))
#print("sum_ratio_absent_kps_case_3: {}".format(sum_ratio_absent_kps_case_3))
#print("exp_ratio_case_2_and_3: {}".format(exp_ratio_case_2_and_3))


