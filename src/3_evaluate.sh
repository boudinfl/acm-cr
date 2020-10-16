#!/usr/bin/env bash
for RUN in output/*.txt
do
    echo "Evaluating ${RUN}"
    # -m P.30
    # -q
    #../ir-using-kg/anserini/tools/eval/trec_eval.9.0.4/trec_eval -m map -q \
    #                                        data/topics+qrels/3397271.3401188.para.qrels \
    #                                        ${RUN} > ${RUN%.*}.results
    ../ir-using-kg/anserini/tools/eval/trec_eval.9.0.4/trec_eval -m map -m recall.10 \
                                            data/topics+qrels/all.para.qrels \
                                            ${RUN}
done