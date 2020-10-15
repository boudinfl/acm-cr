#!/usr/bin/env bash

# create gold keyphrases files
#mkdir -p data/keyphrases/
#python src/bib_to_gold.py --directory data/acm-dl/ --output data/keyphrases/acm-dl.gold

# produce T+A documents
mkdir -p data/docs/t+a/
if [[ ! -f "data/docs/t+a/acm-dl.trec.gz" ]]
    then
        python src/bib_to_trec.py \
            --directory data/acm-dl/ \
            --output data/docs/t+a/acm-dl.trec.gz
fi

# produce T+A+K documents
mkdir -p data/docs/t+a+k/
if [[ ! -f "data/docs/t+a+k/acm-dl.trec.gz" ]]
    then
        python src/bib_to_trec.py \
               --directory data/acm-dl/ \
               --output data/docs/t+a+k/acm-dl.trec.gz \
               --path_to_keyphrases data/keyphrases/acm-dl.gold.all.json.gz
fi

# T+A + absent K or present K
for VARIANT in "abs" "pres" "abs_c1" "abs_c2" "abs_c3" "pres+abs_c1" "abs_c2+abs_c3"
do
    EXP="t+a+k-${VARIANT}"
    mkdir -p data/docs/${EXP}/
    for FILE in data/docs/*.gz
    do
        if [[ ! -f "data/docs/${EXP}/acm-dl.trec.gz" ]]
        then
            python src/bib_to_trec.py \
                   --directory data/acm-dl/ \
                   --output data/docs/${EXP}/acm-dl.trec.gz \
                   --path_to_keyphrases data/keyphrases/acm-dl.gold.${VARIANT}.json.gz
        fi
    done
done
