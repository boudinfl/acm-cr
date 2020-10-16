#!/usr/bin/env bash
for EXP in data/docs/t+a*
do
    if [[ ! -d "data/indexes/lucene-index.${EXP##*/}" ]]
    then
        sh ../ir-using-kg/anserini/target/appassembler/bin/IndexCollection \
            -collection TrecCollection \
            -threads 2 \
            -input ${EXP}/ \
            -index data/indexes/lucene-index.${EXP##*/} \
            -storePositions -storeDocvectors -storeRaw
    else
        echo "Index for ${EXP##*/} already exists"
    fi
done