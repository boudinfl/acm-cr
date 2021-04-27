# -*- coding: utf-8 -*-

"""Rerank top-N retrieved documents using Transformers."""

import json
import torch
import argparse
from collections import defaultdict
from scipy.spatial.distance import cosine
from transformers import *

tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased')
model.eval()

# get the command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--collection",
                    help="path to the collection of documents in TREC format.",
                    type=str)

parser.add_argument("--contexts",
                    help="path to the collection of documents in TREC format.",
                    type=str)

parser.add_argument("--input",
                    help="input file in trec_eval format.",
                    type=str)

parser.add_argument("--output",
                    help="output file in trec_eval format.",
                    type=str)

args = parser.parse_args()

print("Loading the document collection ...", end='', flush=True)
collection = {}
with open(args.collection, 'rt') as f:
    for i, line in enumerate(f):
        doc = json.loads(line.strip())
        collection[doc["id"]] = doc["title"] + ' ' + doc["abstract"]
print("... {} documents".format(len(collection)))

print("Loading the contexts ...", end='', flush=True)
contexts = {}
with open(args.contexts, 'rt') as f:
    for i, line in enumerate(f):
        query = json.loads(line.strip())
        contexts[query["id"]] = (query["context"], tokenizer(query["context"], return_tensors="pt", max_length=512, truncation=True))
print("... {} contexts".format(len(contexts)))

print("Loading the top-N retrieved documents ...", end='', flush=True)
top_n = defaultdict(list)
with open(args.input, 'rt') as f:
    for i, line in enumerate(f):
        cols = line.strip().split()
        top_n[cols[0]].append((cols[2], cols[4]))
print("... {} ranked queries".format(len(top_n)))

print("Inferring embeddings for contexts ...")
reranked_contexts = {}
contexts_embeddings = {}
for context_id in contexts:
    print(" - Processing {} ({}) ...".format(context_id, len(reranked_contexts)+1), end='', flush=True)
    with torch.no_grad():
        outputs = model(**contexts[context_id][1])
        context_embedding = torch.mean(outputs.last_hidden_state, dim=1).squeeze()
        print("... context embedding done")
    print(" - Inferring embeddings for the top-N relevant documents ...", end='', flush=True)
    cosine_similarities = {}
    document_embeddings = []
    for doc_id, score in top_n[context_id]:
        with torch.no_grad():
            inputs = tokenizer(collection[doc_id], return_tensors="pt", max_length=512, truncation=True)
            outputs = model(**inputs)
            document_embedding = torch.mean(outputs.last_hidden_state, dim=1).squeeze()
            document_embeddings.append(document_embedding)
            cosine_similarities[doc_id] = 1.0 - cosine(context_embedding, document_embedding)
    print("... {} document embeddings done".format(len(document_embeddings)))

    reranked_documents = {k: v for k, v in sorted(cosine_similarities.items(), key=lambda item: item[1], reverse=True)}
    reranked_contexts[context_id] = reranked_documents

    # print(context_id, context_embedding)
    # break

with open(args.output, 'w') as o:
    for context_id in reranked_contexts:
        rank = 1
        for rel_doc, score in reranked_contexts[context_id].items():
            # 337177001 Q0 10.1145/2213556.2213568 1 74.030197 Anserini
            o.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(context_id, 'Q0', rel_doc, rank, score, "SciBert"))
            rank += 1


