#!/usr/bin/env bash
for RUN in output/*.txt
do
    echo "Evaluating ${RUN}"
    # -m P.30
    # -q
    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m recall.1000 -q \
                                            data/topics+qrels/all.para.qrels \
                                            ${RUN} > ${RUN%.*}.results
    anserini/tools/eval/trec_eval.9.0.4/trec_eval -m ndcg_cut.10 -m recall.10 \
                                            data/topics+qrels/all.para.qrels \
                                            ${RUN}
done