# -*- coding: utf-8 -*-

"""Convert citation contexts into queries / qrels."""

import os
import json
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
    # collection = set([line.strip() for line in f])
    collection = []
    for i, line in enumerate(f):
        doc = json.loads(line.strip())
        collection.append(doc["id"])
    print('{} doc_ids in the collection'.format(len(collection)))

topics = []
json_topics = []
qrels = []
nb_papers = 0

for filename in glob.iglob(args.input+"/**", recursive=True):
    if os.path.isfile(filename) and filename.endswith(".xml"):

        tree = ET.parse(filename)
        root = tree.getroot()

        doi = root.find('doi').text
        title = root.find('title').text
        abstract = root.find('abstract').text

        print('processing {}'.format(doi))
        nb_papers += 1

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
                json_topics.append(json.dumps({"id": context_id, "context": " ".join(sentences)}))


with open(args.output+".topics", "wt") as o:
    o.write("\n".join(topics))

with open(args.output+".qrels", "wt") as o:
    o.write("\n".join(qrels))

with open(args.output+".jsonl", "wt") as o:
    o.write("\n".join(json_topics))

print('overall: {} queries and {} qrels from {} papers'.format(len(topics), len(qrels), nb_papers))

        





