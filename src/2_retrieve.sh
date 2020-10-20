#!/usr/bin/env bash
TOPICS=data/topics+qrels/all.para.topics
cat data/topics+qrels/sigir-2020/*.para.topics > ${TOPICS}
QRELS=data/topics+qrels/all.para.qrels
cat data/topics+qrels/sigir-2020/*.para.qrels > ${QRELS}

TOPICFIELD="title"
mkdir -p output
for INDEX in data/indexes/lucene-index.*
do
    EXP=${INDEX##*/lucene-index.}
    for MODEL in "bm25" # "qld"
    do
        if [[ ! -f "output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt.caca" ]]
        then
            # retrieve documents using the given model
            sh ../ir-using-kg/anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics ${TOPICS} \
               -output output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt -${MODEL} \
               -topicfield ${TOPICFIELD}
        fi

        #if [[ ! -f "output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt" ]]
        #then
            # compute model with pseudo-relevance feedback RM3
        #    sh ../ir-using-kg/anserini/target/appassembler/bin/SearchCollection \
        #       -topicreader Trec \
        #       -index ${INDEX} \
        #       -topics data/topics+qrels/3397271.3401188.topics \
        #       -output output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt -${MODEL} -rm3 \
        #       -topicfield ${TOPICFIELD}
        #fi
    done
done