# Context-aware Citation Recommendation

This repository presents the test collection for context-aware (or local)
citation recommendation constructed for running document retrieval experiments.

## Requirements

### Installing required Python modules 

```
pip install -r requirements.txt 
```

## Test collection

### Documents 

Documents are BibTeX reference files of papers about IR-related topics collected from the [ACM Digital Library](https://dl.acm.org/). We use the SIGs IR, KDD, CHI, WEB and MOD sponsored conferences and journals as filter. BibTeX files are grouped by year (e.g. 'sigir/sigir-1999' contains all citations from SIGIR-1999). Details about the venues are presented in ['data/acm-dl/venues.md'](venues). An example of document is given below:

```bibtex
@inproceedings{10.1145/3383583.3398517,
  author = {Gallina, Ygor and Boudin, Florian and Daille, B\'{e}atrice},
  title = {Large-Scale Evaluation of Keyphrase Extraction Models},
  year = {2020},
  isbn = {9781450375856},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  url = {https://doi.org/10.1145/3383583.3398517},
  doi = {10.1145/3383583.3398517},
  abstract = {Keyphrase extraction models are usually evaluated under different, not directly comparable, experimental setups. [...]},
  booktitle = {Proceedings of the ACM/IEEE Joint Conference on Digital Libraries in 2020},
  pages = {271–278},
  numpages = {8},
  keywords = {natural language processing, keyphrase generation, evaluation},
  location = {Virtual Event, China},
  series = {JCDL '20}
}
```

Statistics of the test collection:

| #docs (T+A) | #docs (+K) |   %P |   %R |   %M |   %U | %exp | #kps |
| -----------:| ----------:| ----:| ----:| ----:| ----:| ----:| ----:|
|      102510 |      70956 | 53.6 | 11.7 | 19.3 | 15.4 | 13.4 |  4.5 |

### Queries (citation contexts)

Following the methodology proposed in [[1]](https://doi.org/10.1145/3132847.3133085), 
we selected open-access (on ACM or Arxiv) (for data sharing reasons) papers from 
conferences and manually extracted the citation contexts and cited references (relevant
documents).

Papers used for generating queries are in the `data/topics+qrels`
directory. They are grouped by venue (e.g. sigir-2020), and each of
them is represented by three separate files, e.g. for paper with
doi `10.1145/3397271.3401032`:

```
3397271.3401032.pdf   # pdf of the paper

3397271.3401032.dois  # manually curated list of dois for cited references
                      # the following rules are used for mapping dois :
                      #   1. DOI from the ACM DL
                      #   2. DOI from another publisher (including ACL-anthology DOIs)
                      #   3. arxiv/pubmed/acl-anthology url
                      #   4. pdf url
                      #   5. None

3397271.3401032.xml   # manually extracted citation contexts
```

Actually, there are 50 papers (list of selected papers is in 
[`data/topics+qrels/papers/list.md`](data/topics+qrels/papers/list.md) and
their manually extracted and curated citation contexts are in the
following xml format:

```xml
<doc>
  <doi>10.1145/3397271.3401032</doi>
  <title>Measuring Recommendation [...]</title>
  <abstract>Explanations have a large effect on [...]</abstract>
  <contexts>
  <contexts>
    <context id="01" section="introduction">
      <s>Recommendations are part of everyday life.</s>
      <s>Be they made by a person, or by [...]</s>
      <s cites="13,14,23,28">Explanations are known to strongly impact how the recipient of a recommendation responds [13, 14, 23, 28], yet the effect is still not well understood.</s>
    </context>
    [...]
  </contexts>
  <references>
    <reference id="1">10.1145/3173574.3174156</reference>
    <reference id="2">10.1145/3331184.3331211</reference>
    [...]
  </references>
</doc>
```

## Some statistics

```
python3 src/cc_stats.py --input data/topics+qrels/papers/ \
                        --collection data/topics+qrels/collection.txt

avg number of cited documents: 31.82 [8 - 71]
avg number of cited documents in collection: 15.62 [1 - 37]
avg coverage of collection: 0.5011 [0.0909 - 0.8333]
```

- number of citation contexts (s): 835
- number of 1+/all citation contexts (s): 550

|     0 |    1+ |   All |
| -----:| -----:| -----:|
| 34.13 | 21.20 | 44.67 |

- number of citation contexts (p): 341
- number of 1+/all citation contexts (p): 268

|     0 |    1+ |   All |
| -----:| -----:| -----:|
| 21.41 | 53.67 | 24.93 |

## Document retrieval

### Installing anserini

Here, we use the open-source information retrieval toolkit 
[anserini](http://anserini.io/) which is built on 
[Lucene](https://lucene.apache.org/).
Below are the installation steps for a mac computer (tested on OSX 10.14) based
on their [colab demo](https://colab.research.google.com/drive/1s44ylhEkXDzqNgkJSyXDYetGIxO9TWZn).

```bash
# install maven
brew cask install adoptopenjdk
brew install maven

# cloning / installing anserini
git clone https://github.com/castorini/anserini.git --recurse-submodules
cd anserini/
# for 10.14 issues -> changing jacoco from 0.8.2 to 0.8.3 in pom.xml to build correctly
# for 10.13 issues -> https://github.com/castorini/anserini/issues/648
mvn clean package appassembler:assemble

# compile evaluation tools and other scripts
cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
cd tools/eval/ndeval && make && cd ../../..
```

### Benchmarking IR models

```
./src/0_create_data.sh

75369 entries with T+A+K
present: 0.5341884786642571
absent: 0.46581152133573894
|-> c1/Reordored (i.e. all words): 0.11652164544805718
|-> c2/Mixed (i.e. some words): 0.19352479545861326
|-> c3/Unseen (i.e. no words): 0.15576508042908255
|-> exp. : 0.1349176087261396
avg nb kps : 4.537906424525423

75333 T+A+K, 20043 T+A, 13313 T over 108400 entries

./src/1_create_indexes.sh
./src/2_retrieve.sh
./src/3_evaluate.sh

```

| index | nDCG@10 | recall@10 |
| -----:| -------:| ---------:| 
|   T+A |   30.35 |     35.64 |
| ----- | ------- | --------- |
|    +P |   30.81 |     36.02 |
|    +R |   29.95 |     35.43 |
|    +M |   29.77 |     36.22 |
|    +U |   30.82 |     36.24 |
| ----- | ------- | --------- |
|    +A |   30.47 |     36.62 |
| ----- | ------- | --------- |
|  +P+R |   30.47 |     35.82 |
|  +M+U |   30.38 |     37.21 |
| ----- | ------- | --------- |
| T+A+K |   30.94 |     36.65 |

## References

1. Dwaipayan Roy. 2017. An Improved Test Collection and Baselines for
   Bibliographic Citation Recommendation. In Proceedings of the 2017 ACM on 
   Conference on Information and Knowledge Management (CIKM '17). Association 
   for Computing Machinery, New York, NY, USA, 2271–2274. 
   DOI:https://doi.org/10.1145/3132847.3133085