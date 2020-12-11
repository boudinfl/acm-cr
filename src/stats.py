# -*- coding: utf-8 -*-

import gzip
import sys
import json

# loading keyphrases
keyphrases = {}
with gzip.open(sys.argv[1], "rt") as f:
    keyphrases = json.loads(f.read())
    print("{} docids loaded for keyphrases".format(len(keyphrases)))
    nb_kps = sum([len(keyphrases[doc_id]) for doc_id in keyphrases])

    print(nb_kps/70971)

