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

parser.add_argument("--collection",
                    help="dois for the document collection.",
                    type=str)

args = parser.parse_args()

with open(args.collection) as f:
    collection = [line.strip() for line in f]

for filename in glob.iglob(args.input+"/**", recursive=True):
    if os.path.isfile(filename) and filename.endswith(".xml"):
        print('processing {}'.format(filename))

        #xmldoc = minidom.parse(filename)
        tree = ET.parse(filename)
        root = tree.getroot()

        doi = root.find('doi').text
        title = root.find('title').text
        abstract = root.find('abstract').text

        references = root.find('references')
        citations = {}
        for reference in references.findall('reference'):
            citations[reference.get("id")] = reference.text

        #print(doi)
        #print(title)

        contexts = root.find('contexts')
        for context in contexts.findall('context'):
            #print(context.get("id"))
            sentences = [sentence.text for sentence in context.findall('s')]
            cited_documents = [sentence.get("cites") for sentence in context.findall('s')]
            #print(' '.join(sentences))
            #print(cited_documents)

        #print(citations)

        





