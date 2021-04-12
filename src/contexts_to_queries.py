# -*- coding: utf-8 -*-

"""Convert citation contexts into queries / qrels."""

import os
import glob
import argparse
import xml.etree.ElementTree as ET
import spacy

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

parser.add_argument("--sentences",
                    help="use sentences instead of paragraphs for queries.",
                    action='store_true')

args = parser.parse_args()

naacl_papers = []
# sigir-2020 (18 papers)
naacl_papers.append("3397271.3401032")
naacl_papers.append("3397271.3401052")
naacl_papers.append("3397271.3401057")
naacl_papers.append("3397271.3401103")
naacl_papers.append("3397271.3401106")
naacl_papers.append("3397271.3401164")
naacl_papers.append("3397271.3401188")
naacl_papers.append("3397271.3401191")
naacl_papers.append("3397271.3401198")
naacl_papers.append("3397271.3401204")
naacl_papers.append("3397271.3401207")
naacl_papers.append("3397271.3401224")
naacl_papers.append("3397271.3401266")
naacl_papers.append("3397271.3401281")
naacl_papers.append("3397271.3401322")
naacl_papers.append("3397271.3401330")
naacl_papers.append("3397271.3401333")
naacl_papers.append("3397271.3401467")
# ictir-2020 (4 papers) 
naacl_papers.append("3409256.3409819")
naacl_papers.append("3409256.3409827")
naacl_papers.append("3409256.3409829")
naacl_papers.append("3409256.3409838")
# wsdm-2020 (5 papers)
naacl_papers.append("3336191.3371775")
naacl_papers.append("3336191.3371814")
naacl_papers.append("3336191.3371820")
naacl_papers.append("3336191.3371844")
naacl_papers.append("3336191.3371855")
# chiir-2020 (3 papers)
naacl_papers.append("3343413.3377957")
naacl_papers.append("3343413.3377977")
naacl_papers.append("3343413.3378011")

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

def tokenize(s):
    """tokenize an input text."""
    doc = nlp(s)
    return [word.text for word in doc]

def flatten_list(a):
    return [item for sublist in a for item in sublist]

with open(args.collection, "rt") as f:
    collection = set([line.strip() for line in f])
    print('{} doc_ids in the collection'.format(len(collection)))

topics = []
qrels = []
nb_papers = 0

for filename in glob.iglob(args.input+"/**", recursive=True):
    if os.path.isfile(filename) and filename.endswith(".xml"):

        tree = ET.parse(filename)
        root = tree.getroot()

        doi = root.find('doi').text
        title = root.find('title').text
        abstract = root.find('abstract').text

        #if doi.split('/')[-1] not in naacl_papers:
        #    continue

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
            cited_documents = []
            for sentence in context.findall('s'):
                sentences.append(sentence.text)
                if sentence.get("cites"):
                    markers = sentence.get("cites")
                    rel_documents.append([(mark, citations[mark]) for mark in markers.split(",") if citations[mark] in collection])
                    cited_documents.append(markers.split(","))
                else:
                    rel_documents.append([])

            #coverage = len(flatten_list(rel_documents)) / len(flatten_list(cited_documents))
            nb_tokens = len(tokenize(" ".join(sentences)))

            # context id is doc_id (after /)+ context number
            context_id = doi.split(".")[-1] + context.get("id")

            if args.sentences:
                for i, sentence in enumerate(sentences):
                    sentence_id = context_id[-6:] + str(i)
                    # consider query if there is at least one relevant document in the collection
                    if rel_documents[i]:
                        topics.append("<top>\n<num> Number: {}\n<title> {}\n\n<desc> Description:\n{}\n\n<narr> Narrative:\n{}\n</top>\n".format(sentence_id, title, sentence, ""))
                        for mark, rel_doc_id in set(rel_documents[i]):
                            qrels.append("{}\t{}\t{}\t{}".format(sentence_id, mark, rel_doc_id, "1"))
            else:
                # get the relevant documents
                context_qrels = flatten_list(rel_documents)

                # consider query if there is at least one relevant document in the collection
                if context_qrels and nb_tokens < 500:
                    topics.append("<top>\n<num> Number: {}\n<title> {}\n\n<desc> Description:\n{}\n\n<narr> Narrative:\n{}\n</top>\n".format(context_id, title, " ".join(sentences), ""))
                    for mark, rel_doc_id in set(context_qrels):
                        qrels.append("{}\t{}\t{}\t{}".format(context_id, mark, rel_doc_id, "1"))

with open(args.output+".topics", "wt") as o:
    o.write("\n".join(topics))

with open(args.output+".qrels", "wt") as o:
    o.write("\n".join(qrels))

print('overall: {} queries and {} qrels from {} papers'.format(len(topics), len(qrels), nb_papers))

        





