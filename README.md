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
|      102510 |      70956 | 53.6 | 11.7 | 19.3 | 15.4 | 13.4 |  4.5 |

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
                       # explicit citation markers (e.g. He et al. [19] -> [19]).
                       # We also remove last paragraph sentences if they
                       # are such as "in this paper" or "in this study".
                       
3397271.3401032.qrels  # relevant judgments                               
```

Actually, there are 39 papers and XXX topics.

Below is the list of papers used for generating queries.

```
├── sigir-2020 (20 papers)
    ├── 3397271.3401032.pdf
    ├── 3397271.3401051.pdf (*)
    ├── 3397271.3401052.pdf
    ├── 3397271.3401057.pdf
    ├── 3397271.3401103.pdf
    ├── 3397271.3401106.pdf
    ├── 3397271.3401061.pdf (*)
    ├── 3397271.3401164.pdf
    ├── 3397271.3401188.pdf
    ├── 3397271.3401191.pdf
    ├── 3397271.3401198.pdf
    ├── 3397271.3401204.pdf
    ├── 3397271.3401207.pdf
    ├── 3397271.3401224.pdf
    ├── 3397271.3401266.pdf
    ├── 3397271.3401281.pdf
    ├── 3397271.3401322.pdf
    ├── 3397271.3401330.pdf
    ├── 3397271.3401333.pdf
    ├── 3397271.3401467.pdf
├── ictir-2020 (10 papers) 
    ├── 3409256.3409817.pdf (*)
    ├── 3409256.3409819.pdf
    ├── 3409256.3409820.pdf (*)
    ├── 3409256.3409825.pdf (*)
    ├── 3409256.3409827.pdf
    ├── 3409256.3409829.pdf
    ├── 3409256.3409830.pdf (*)
    ├── 3409256.3409837.pdf (*)
    ├── 3409256.3409838.pdf
    ├── 3409256.3409847.pdf (*)
├── wsdm-2020 (5 papers)
    ├── 3336191.3371775.pdf
    ├── 3336191.3371814.pdf
    ├── 3336191.3371820.pdf
    ├── 3336191.3371844.pdf
    ├── 3336191.3371855.pdf
├── chiir-2020 (4 papers)
    ├── 3343413.3377957.pdf
    ├── 3343413.3377968.pdf (*)
    ├── 3343413.3377977.pdf
    ├── 3343413.3378011.pdf
```

## Document retrieval

```
./src/0_create_data.sh

70960 entries with T+A+K
present: 0.5356199337142871
absent: 0.4643800662857018
├──> c1/Reordored (i.e. all words): 0.1172396547138912
├──> c2/Mixed (i.e. some words): 0.19282425867095065
├──> c3/Unseen (i.e. no words): 0.15431615290087136
├──> exp. : 0.1341835075750805
avg nb kps : 4.5367317609265365

70956 T+A+K, 18726 T+A, 13117 T over 102510 entries

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