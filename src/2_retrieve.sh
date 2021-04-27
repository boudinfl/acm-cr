#!/usr/bin/env bash

# CONTEXTS="paragraphs"
# BASENAME="data/topics+qrels/contexts"

# # create topics/qrels from xml files
# python3 src/contexts_to_queries.py \
#         --input data/topics+qrels/papers/ \
#         --collection data/docs/collection.jsonl \
#         --output ${BASENAME}

CONTEXTS="sentences"
BASENAME="data/topics+qrels/sentences"

# create topics/qrels from xml files
python3 src/contexts_to_queries.py \
        --input data/topics+qrels/papers/ \
        --collection data/docs/collection.jsonl \
        --output ${BASENAME} \
        --sentences

TOPICS="${BASENAME}.topics"
QRELS="${BASENAME}.qrels"

#TOPICFIELD="title"
TOPICFIELD="description"
#TOPICFIELD="title+description"
mkdir -p output
for INDEX in data/indexes/lucene-index.*
do
    EXP=${INDEX##*/lucene-index.}
    for MODEL in "bm25" # "qld"
    do
        if [[ ! -f "output/run.${EXP}.${TOPICFIELD}.${CONTEXTS}.${MODEL}.txt" ]]
        then
            # retrieve documents using the given model
            sh anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics ${TOPICS} \
               -output output/run.${EXP}.${TOPICFIELD}.${CONTEXTS}.${MODEL}.txt -${MODEL} \
               -topicfield ${TOPICFIELD} \
               -hits 20
        fi

        # if [[ ! -f "output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt" ]]
        # then
        #    # compute model with pseudo-relevance feedback RM3
        #    sh anserini/target/appassembler/bin/SearchCollection \
        #       -topicreader Trec \
        #       -index ${INDEX} \
        #       -topics ${TOPICS} \
        #       -output output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt -${MODEL} -rm3 \
        #       -topicfield ${TOPICFIELD} \
        #       -hits 100
        # fi
    done
done