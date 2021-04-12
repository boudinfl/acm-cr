#!/usr/bin/env bash
# TOPICS=data/topics+qrels/all.topics
# cat data/topics+qrels/sigir-2020/*.topics > ${TOPICS}
# cat data/topics+qrels/chiir-2020/*.topics >> ${TOPICS}
# cat data/topics+qrels/ictir-2020/*.topics >> ${TOPICS}
# cat data/topics+qrels/wsdm-2020/*.topics >> ${TOPICS}

# QRELS=data/topics+qrels/all.qrels
# cat data/topics+qrels/sigir-2020/*.qrels > ${QRELS}
# cat data/topics+qrels/chiir-2020/*.qrels >> ${QRELS}
# cat data/topics+qrels/ictir-2020/*.qrels >> ${QRELS}
# cat data/topics+qrels/wsdm-2020/*.qrels >> ${QRELS}


BASENAME="data/topics+qrels/contexts"

# create topics/qrels from xml files
python3 src/contexts_to_queries.py \
        --input data/topics+qrels/papers/ \
        --collection data/topics+qrels/collection.txt \
        --output ${BASENAME} #\
        #--sentences

TOPICS="${BASENAME}.topics"
QRELS="${BASENAME}.qrels"

#TOPICS="data/topics+qrels/naacl-21.topics"
#QRELS="data/topics+qrels/naacl-21.qrels"

#TOPICFIELD="title"
TOPICFIELD="description"
#TOPICFIELD="title+description"
mkdir -p output
for INDEX in data/indexes/lucene-index.*
do
    EXP=${INDEX##*/lucene-index.}
    for MODEL in "bm25" # "qld"
    do
        if [[ ! -f "output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt" ]]
        then
            # retrieve documents using the given model
            sh anserini/target/appassembler/bin/SearchCollection \
               -topicreader Trec \
               -index ${INDEX} \
               -topics ${TOPICS} \
               -output output/run.${EXP}.${TOPICFIELD}.${MODEL}.txt -${MODEL} \
               -topicfield ${TOPICFIELD}
        fi

        # if [[ ! -f "output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt" ]]
        # then
        #    # compute model with pseudo-relevance feedback RM3
        #    sh anserini/target/appassembler/bin/SearchCollection \
        #       -topicreader Trec \
        #       -index ${INDEX} \
        #       -topics ${TOPICS} \
        #       -output output/run.${EXP}.${TOPICFIELD}.${MODEL}+rm3.txt -${MODEL} -rm3 \
        #       -topicfield ${TOPICFIELD}
        # fi
    done
done