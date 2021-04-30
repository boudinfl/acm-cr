# -*- coding: utf-8 -*-

"""Combine multiple rankings."""

import sys
from collections import defaultdict

p1 = 0.5
p2 = 0.5

def normalize(l):
    norm = max([score for doc_id, score in l])
    return {doc_id: score/norm for doc_id, score in l}

top_n_1 = defaultdict(list)
with open(sys.argv[1], 'rt') as f:
    for i, line in enumerate(f):
        cols = line.strip().split()
        top_n_1[cols[0]].append((cols[2], float(cols[4])))

top_n_2 = defaultdict(list)
with open(sys.argv[2], 'rt') as f:
    for i, line in enumerate(f):
        cols = line.strip().split()
        top_n_2[cols[0]].append((cols[2], float(cols[4])))


with open(sys.argv[3], 'w') as o:
    for context_id in top_n_1:

        normalized_top_n_1 = normalize(top_n_1[context_id])
        normalized_top_n_2 = normalize(top_n_2[context_id])
        combined_top_n = {doc_id: (p1*normalized_top_n_1[doc_id]+p2*normalized_top_n_2[doc_id]) for doc_id in normalized_top_n_1}
        reranking = {k: v for k, v in sorted(combined_top_n.items(), key=lambda item: item[1], reverse=True)}

        rank = 1
        for rel_doc, score in reranking.items():
            # 337177001 Q0 10.1145/2213556.2213568 1 74.030197 Anserini
            o.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(context_id, 'Q0', rel_doc, rank, score, "BM25+SciBert"))
            rank += 1

