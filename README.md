# ACM-CR: A Manually Annotated Test Collection for Citation Recommendation

This repository contains the test collection for (context-aware)
citation recommendation constructed from bibliographic records and
open-access papers collected from the ACM Digital Library.

## Requirements

### Installing required Python modules

```
pip install -r requirements.txt 
```

## Test collection

### Document collection

Documents are bibliographic records of scientific papers (BibTeX entries) about IR-related topics collected from the [ACM Digital Library](https://dl.acm.org/). We use the SIGs IR, KDD, CHI, WEB and MOD sponsored conferences and journals as filter. BibTeX files are grouped by venue-year (e.g. 'sigir/sigir-1999' contains all citations from SIGIR-1999). Details about the venues are presented in [here]('data/acm-dl/venues.md'). An example of document is given below:

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

Some statistics of the document collection (2021-04-30): 114,882 records, from which 103,990 (91%) have abstracts and 83,517 have author-assigned keyphrases (73%).
We only consider 'article' and 'inproceedings' citations, and remove session papers (title starting with "Session" and empty abstract)

### Queries (citation contexts) and relevance judgments

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

Actually, there are 50 papers (the list of selected papers is [`data/topics+qrels/papers/list.md`](here)) and their manually extracted and curated citation contexts are in the following xml format:

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

Some statistics of the manually extracted citations and relevance judgements

```
python3 src/cc_stats.py --input data/topics+qrels/papers/ \
                        --collection data/topics+qrels/collection.txt

avg number of cited documents: 31.82 [8 - 71]
avg number of cited documents in collection: 15.86 [1 - 37]
avg coverage of collection: 0.5074 [0.0909 - 0.8333]
```

- number of citation contexts (s): 837
- number of 1+/all citation contexts (s): 552

|     0 |    1+ |   All |
| -----:| -----:| -----:|
| 34.05 | 20.91 | 45.04 |

- number of citation contexts (p): 341
- number of 1+/all citation contexts (p): 269

|     0 |    1+ |   All |
| -----:| -----:| -----:|
| 21.11 | 53.67 | 25.22 |

## Document retrieval (TODO)

### Installing anserini

Here, we use the open-source information retrieval toolkit 
[anserini](http://anserini.io/) which is built on 
[Lucene](https://lucene.apache.org/).
Below are the installation steps for a mac computer (tested on OSX 11.2.3) based
on their [colab demo](https://colab.research.google.com/drive/1s44ylhEkXDzqNgkJSyXDYetGIxO9TWZn).

```bash
# install maven
brew install adoptopenjdk
brew install maven

# cloning / installing anserini
git clone https://github.com/castorini/anserini.git --recurse-submodules
cd anserini/
# for 11.1 issues -> add the following in pom.xml
# <plugin>
#   <groupId>org.apache.maven.plugins</groupId>
#   <artifactId>maven-surefire-plugin</artifactId>
#   <configuration>
#     <forkCount>3</forkCount>
#     <reuseForks>true</reuseForks>
#     <argLine>-Xmx1024m -XX:MaxPermSize=256m</argLine>
#   </configuration>
# </plugin>
# for 10.14 issues -> changing jacoco from 0.8.2 to 0.8.3 in pom.xml to build correctly
# for 10.13 issues -> https://github.com/castorini/anserini/issues/648
mvn clean package appassembler:assemble

# compile evaluation tools and other scripts
cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
cd tools/eval/ndeval && make && cd ../../..
```

### Converting citations and building indexes

```
./src/0_create_data.sh
./src/1_create_indexes.sh
```

### Creating queries/qrels and retrieving citations using BM25

```
./src/2_retrieve.sh
```


### Reranking using SciBERT

```
python3 src/scibert_reranker.py --collection data/docs/collection.jsonl \
                                --contexts data/topics+qrels/contexts.jsonl \
                                --input output/run.t+a+k.description.paragraphs.bm25.txt \
                                --output output/run.t+a+k.description.paragraphs.scibert.txt

python3 src/scibert_reranker.py --collection data/docs/collection.jsonl \
                                --contexts data/topics+qrels/sentences.jsonl \
                                --input output/run.t+a+k.description.sentences.bm25.txt \
                                --output output/run.t+a+k.description.sentences.scibert.txt

python3 src/add-reranker.py output/run.t+a+k.description.paragraphs.bm25.txt \
                            output/run.t+a+k.description.paragraphs.scibert.txt \
                            output/run.t+a+k.description.paragraphs.bm25+scibert.txt
                            
python3 src/add-reranker.py output/run.t+a+k.description.sentences.bm25.txt \
                            output/run.t+a+k.description.sentences.scibert.txt \
                            output/run.t+a+k.description.sentences.bm25+scibert.txt
```

### Evaluating the retrieval models

```
./src/3_evaluate.sh

recall_10               all 0.3440
ndcg_cut_10             all 0.2937
Evaluating output/run.t+a+k.description.paragraphs.bm25.txt
recall_10               all 0.3358
ndcg_cut_10             all 0.2827
Evaluating output/run.t+a+k.description.paragraphs.scibert.txt
recall_10               all 0.3397
ndcg_cut_10             all 0.2307
Evaluating output/run.t+a+k.description.sentences.bm25+scibert.txt
recall_10               all 0.4030
ndcg_cut_10             all 0.3231
Evaluating output/run.t+a+k.description.sentences.bm25.txt
recall_10               all 0.3903
ndcg_cut_10             all 0.3156
Evaluating output/run.t+a+k.description.sentences.scibert.txt
recall_10               all 0.3340
ndcg_cut_10             all 0.1761
```
