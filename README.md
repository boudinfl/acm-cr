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
# changing jacoco from 0.8.2 to 0.8.3 in pom.xml to build correctly
mvn clean package appassembler:assemble

# compile evaluation tools and other scripts
cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..
cd tools/eval/ndeval && make && cd ../../..
```

## Test collection

### Documents 

Documents are BibTeX citation files collected from ACM DL using the SIGs IR,
KDD, CHI, WEB and MOD sponsored conferences and journals as filter. More,
specifically, the test collection contains the following venues (years, #docs):

- Conferences:
    - ADCS (12-19, #115), AIRS (08-09, #120), AVI (94-20, #1108)
    - BooksOnline (08-12, #57)
    - CHI/CHI-EA (82-20, #19446), CHIIR (16-20, #374), CIKM (93-20, #5497),
      CIR (11, #7), CompSci (13, #8), CSCW (86-19, #2726)
    - DL (96-00, #244), DocEng (01-20, #971), DTMBIO (08-15, #151), 
      DLRS (16-18, #24)
    - ESAIR (09-15, #101)
    - FIRE (12-19, #91)
    - ICTIR (13-20, #313), IIIX (06-14, #242), IUI (93-20, #2043)
    - JCDL (01-20, #2183)
    - KDD (99-20, #3966)
    - OzCHI (05-20, #1271)
    - PervasiveHealth (16, #60)
    - RecSys (07-20, #1279)
    - SIGIR (78-20, #5251), SIGMOD (75-20, #5378)
    - UAI (09, #76), UIST (88-19, #2076), UMAP (12-20, #728)
    - WI (03-19, #1127), WSDM (08-20, #1123), WWW (01-20, #6823)
- Journals:
    - ACM Transactions on Intelligent Systems and Technology (TIST)
      (10-20, #699)
    - ACM Transactions on Information Systems (TOIS) (83-20, #817)
    - ACM SIGIR Forum (71-20, #1032)
    - ACM Computing Surveys (CSUR) (69-20, #2053)
    - ACM Journal of Data and Information Quality (JDIQ) (09-20, #202)
    - ACM Transactions on Knowledge Discovery from Data (TKDD) (07-20, #515)
    - ACM Transactions on Asian and Low-Resource Language Information Processing
      (TALLIP) (02-20, #490)
    - IEEE/ACM Transactions on Audio, Speech and Language Processing (TASLP)
      (14-20, #1237)
    - Proceedings of the ACM on Human-Computer Interaction (PACMHCI)
      (17-20, #659)
- Journals (non ACM)
    - User Modeling and User-Adapted Interaction (klu-user) (97-19, #362)
    - International Journal of Human-Computer Studies (ijhc) (94-20, #1872)
    - Foundations and Trends in Information Retrieval (trir) (06-18, #31)

Statistics of the test collection:

| #docs (T+A) | #docs (+K) |   %P |   %R |   %M |   %U | %exp | #kps |
| -----------:| ----------:| ----:| ----:| ----:| ----:| ----:| ----:|
|       75033 |      56539 | 54.2 | 11.6 | 18.8 | 15.4 | 13.0 |  4.4 |

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

55315 entries with T+A+K
present: 0.5419029326860507
absent: 0.4580970673139533
|-> case 1 (all words): 0.11563620550602775
|-> case 2 (some words): 0.18800505876294774
|-> case 3 (no words): 0.15445580304495474
|-> exp. : 0.1304352691244849
avg nb kps : 4.3930145199739945



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