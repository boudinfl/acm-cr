# -*- coding: utf-8 -*-

"""Convert citation contexts into queries / qrels."""

import os
import glob
import statistics
import argparse
import xml.etree.ElementTree as ET

# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input directory.",
                    type=str)

parser.add_argument("--collection",
                    help="dois for the document collection.",
                    type=str)

args = parser.parse_args()

def flatten_list(a):
    return [item for sublist in a for item in sublist]

with open(args.collection, "rt") as f:
    collection = set([line.strip() for line in f])
    print('{} doc_ids in the collection'.format(len(collection)))

nb_citations = []
nb_citations_in_collection = []

p_citation_contexts_0 = 0
p_citation_contexts_1plus = 0
p_citation_contexts_all = 0

s_citation_contexts_0 = 0
s_citation_contexts_1plus = 0
s_citation_contexts_all = 0

for filename in glob.iglob(args.input+"/**", recursive=True):
    if os.path.isfile(filename) and filename.endswith(".xml"):

        tree = ET.parse(filename)
        root = tree.getroot()

        print('processing {}'.format(filename))

        # parse cited references
        citations = {}
        citations_in_collection = {}
        references = root.find('references')
        for reference in references.findall('reference'):
            citations[reference.get("id")] = reference.text

        nb_citations.append(len(citations))
        nb_citations_in_collection.append(len([c for c in citations if citations[c] in collection]))

        # parse citation contexts
        contexts = root.find('contexts')
        for context in contexts.findall('context'):

            context_markers = []
            context_markers_in_collection = []
            for sentence in context.findall('s'):
                # if sentence is citation context
                if sentence.get("cites"):
                    markers = sentence.get("cites").split(",")
                    markers_in_collection = [mark for mark in markers if citations[mark] in collection]

                    if len(markers) == len(markers_in_collection):
                        s_citation_contexts_all += 1
                    elif len(markers_in_collection):
                        s_citation_contexts_1plus += 1
                    else:
                        s_citation_contexts_0 +=1

                    context_markers.extend(markers)
                    context_markers_in_collection.extend(markers_in_collection)

            if len(context_markers):
                if len(context_markers) == len(context_markers_in_collection):
                    p_citation_contexts_all += 1
                elif len(context_markers_in_collection):
                    p_citation_contexts_1plus += 1
                else:
                    p_citation_contexts_0 += 1

print('*'*80)

print('avg number of cited documents: {:.2f} [{} - {}]'.format(statistics.mean(nb_citations), min(nb_citations), max(nb_citations)))
print('avg number of cited documents in collection: {:.2f} [{} - {}]'.format(statistics.mean(nb_citations_in_collection), min(nb_citations_in_collection), max(nb_citations_in_collection)))

coverage = [nb_citations_in_collection[i]/nb_citations[i] for i in range(len(nb_citations))]
print('avg coverage of collection: {:.4f} [{:.4f} - {:.4f}]'.format(statistics.mean(coverage), min(coverage), max(coverage)))

print('*'*80)

nb_s_citation_contexts = s_citation_contexts_all+s_citation_contexts_1plus+s_citation_contexts_0

print('- number of citation contexts (s): {}'.format(nb_s_citation_contexts))
print('- number of 1+/all citation contexts (s): {}'.format(s_citation_contexts_all+s_citation_contexts_1plus))
print("|     0 |    1+ |   All |")
print("| -----:| -----:| -----:|")
print("| {:.2f} | {:.2f} | {:.2f} |".format(100*s_citation_contexts_0/nb_s_citation_contexts, 100*s_citation_contexts_1plus/nb_s_citation_contexts, 100*s_citation_contexts_all/nb_s_citation_contexts))

print('*'*80)

nb_p_citation_contexts = p_citation_contexts_all+p_citation_contexts_1plus+p_citation_contexts_0
print('- number of citation contexts (p): {}'.format(nb_p_citation_contexts))
print('- number of 1+/all citation contexts (p): {}'.format(p_citation_contexts_all+p_citation_contexts_1plus))
print("|     0 |    1+ |   All |")
print("| -----:| -----:| -----:|")
print("| {:.2f} | {:.2f} | {:.2f} |".format(100*p_citation_contexts_0/nb_p_citation_contexts, 100*p_citation_contexts_1plus/nb_p_citation_contexts, 100*p_citation_contexts_all/nb_p_citation_contexts))






