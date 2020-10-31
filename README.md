# Context-aware Citation Recommendation

This repository presents the test collection for context-aware (or local)
citation recommendation constructed for running document retrieval experiments.

## Requirements

### Install Python modules 

```
pip install -r requirements.txt 
```

### Install anserini

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

## Test collection

### Documents 

Documents are BibTeX reference files of papers about IR-related topics collected from the [ACM Digital Library](https://dl.acm.org/). We use the SIGs IR, KDD, CHI, WEB and MOD sponsored conferences and journals as filter. BibTeX files are grouped by year (e.g. 'sigir/sigir-1999' contains all citations from SIGIR-1999). Details about the venues are presented in ['data/acm-dl/venues.md'](data/acm-dl/venues.md). An example of document is given below:

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
|       82881 |      61169 | 54.2 | 11.6 | 18.8 | 15.4 | 13.0 |  4.4 |

### Queries

Following the methodology proposed in [[1]](https://doi.org/10.1145/3132847.3133085), 
we selected open-access (for data sharing reasons) papers from conferences and 
manually extracted the citation contexts and cited references (relevant
documents).

Papers (pdf versions) used for generating queries are in `data/topics+qrels`
directory. Papers are grouped by venue, and three files are created for each
paper, e.g.:

```
3397271.3401032.pdf    # paper id (last part of docid)

3397271.3401032.docids # manually curated list of docid for cited references
                       # references starting with - symbol are not linked to
                       # documents within the collection (or not found...)
                      
3397271.3401032.topics # queries are natural paragraphs from papers where most
                       # citations are present in the collection. Manual
                       # removing can be applied to remove parts (whole
                       # sentences) that are not coherent (e.g. containing
                       # unlinked citations) or to split very long queries. We
                       # try to keep contexts where at least one marker of a 
                       # series of references is linked. We only use
                       # introduction and related work sections. We remove 
                       # explicit citation markers (e.g. He et al. [19] -> [19])
                       
3397271.3401032.qrels  # relevant judgments                               
```

Actually, there are 20 papers and 113 topics.

## Document retrieval

```
./src/0_create_data.sh

56617 entries with T+A+K
present: 0.542283170700119
absent: 0.45771682929988433
|-> c1/Reordored (i.e. all words): 0.11594508357516725
|-> c2/Mixed (i.e. some words): 0.18817671085940116
|-> c3/Unseen (i.e. no words): 0.15359503486529488
|-> exp. : 0.12993978324091304
avg nb kps : 4.414472638660804
22 docids loaded for blacklist



./src/1_create_indexes.sh
./src/2_retrieve.sh
./src/3_evaluate.sh

```

| index | nDCG@10 | recall@10 |
| -----:| -------:| ---------:| 
|   T+A |   29.55 |     34.93 |
| ----- | ------- | --------- |
|    +P |   30.21 |     35.59 |
|    +R |   29.01 |     34.93 |
|    +M |   29.41 |     35.68 |
|    +U |   30.64 |     35.35 |
| ----- | ------- | --------- |
|    +A |   30.42 |     37.00 |
| ----- | ------- | --------- |
|  +P+R |   30.31 |     35.10 |
|  +M+U |   30.00 |     36.01 |
| ----- | ------- | --------- |
| T+A+K |   31.23 |     36.50 |

## References

1. Dwaipayan Roy. 2017. An Improved Test Collection and Baselines for
   Bibliographic Citation Recommendation. In Proceedings of the 2017 ACM on 
   Conference on Information and Knowledge Management (CIKM '17). Association 
   for Computing Machinery, New York, NY, USA, 2271–2274. 
   DOI:https://doi.org/10.1145/3132847.3133085