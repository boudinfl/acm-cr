# -*- coding: utf-8 -*-

"""Convert citation contexts into queries / qrels."""

import os
import glob
import argparse
import xml.etree.ElementTree as ET

# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--input",
                    help="input directory.",
                    type=str)

parser.add_argument("--output",
                    help="output filename.",
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

topics = []
qrels = []

for filename in glob.iglob(args.input+"/**", recursive=True):
    if os.path.isfile(filename) and filename.endswith(".xml"):

        tree = ET.parse(filename)
        root = tree.getroot()

        doi = root.find('doi').text
        title = root.find('title').text
        abstract = root.find('abstract').text

        print('processing {}'.format(doi))

        citations = {}
        references = root.find('references')
        for reference in references.findall('reference'):
            citations[reference.get("id")] = reference.text

        contexts = root.find('contexts')
        for context in contexts.findall('context'):
            sentences = []
            rel_documents = []
            for sentence in context.findall('s'):
                sentences.append(sentence.text)
                if sentence.get("cites"):
                    markers = sentence.get("cites")
                    rel_documents.append([(mark, citations[mark]) for mark in markers.split(",") if citations[mark] in collection])

            # context id is doc_id (after /)+ context number
            context_id = doi.split(".")[-1] + context.get("id")

            # get the relevant documents
            context_qrels = flatten_list(rel_documents)

            # consider query if there is at least one relevant document in the collection
            if context_qrels:
                topics.append("<top>\n<num> Number: {}\n<title> {}\n\n<desc> Description:\n{}\n\n<narr> Narrative:\n{}\n</top>\n".format(context_id, title, " ".join(sentences), ""))
                for mark, rel_doc_id in set(context_qrels):
                    qrels.append("{}\t{}\t{}\t{}".format(context_id, mark, rel_doc_id, "1"))

with open(args.output+".topics", "wt") as o:
    o.write("\n".join(topics))

with open(args.output+".qrels", "wt") as o:
    o.write("\n".join(qrels))

print('overall: {} queries and {} qrels'.format(len(topics), len(qrels)))

        





