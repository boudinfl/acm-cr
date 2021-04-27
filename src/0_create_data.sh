#!/usr/bin/env bash

# generate TREC-formatted documents for indexing
mkdir -p data/docs/t+a+k/
if [[ ! -f "data/docs/t+a+k/acm-cr.trec.gz" ]]
    then
        python3 src/bibtex_to_trec.py \
            --directory data/acm-dl/ \
            --output data/docs/t+a+k/acm-cr.trec.gz \
            --blacklist data/topics+qrels/blacklist.txt \
            --collection data/docs/collection.jsonl
fi
