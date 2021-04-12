#!/usr/bin/env bash

BASENAME="data/topics+qrels/contexts"
#BASENAME="data/topics+qrels/naacl-21"

for RUN in output/*.txt
do
    echo "Evaluating ${RUN}"
    # -m P.30
    # -q
    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m recall.10 -q \
                                            ${BASENAME}.qrels \
                                            ${RUN} > ${RUN%.*}.results
    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m ndcg_cut.10 -m recall.10 \
                                            ${BASENAME}.qrels \
                                            ${RUN}
done