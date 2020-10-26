# Context-aware Citation Recommendation

This repository presents the test collection for context-aware (or local)
citation recommendation constructed for running document retrieval experiments.

## Requirements

### Install Python modules 

```
pip install -r requirements.txt 
```

## Test collection

### Documents 

Documents are BibTeX citation files collected from ACM DL using the SIGs IR,
KDD, CHI, WEB and MOD sponsored conferences and journals as filter. More,
specifically, the test collection contains the following venues:

- Conferences (years, #docs):
    - ADCS (12-19, #115), AIRS (08-09, #120), AVI (94-20, #1108)
    - BooksOnline (08-12, #57)
    - CHI/CHI-EA (82-20, #19446), CHIIR (16-20, #374), CIKM (93-20, #5497),
      CIR (11, #7), CompSci (13, #8), CSCW (86-19, #2726)
    - DL (96-00, #244), DocEng (01-20, #971), DTMBIO (08-15, #151)
    - ESAIR (09-15, #101)
    - FIRE (12-19, #91)
    - ICTIR (13-20, #313), IIIX (06-14, #242), IUI (93-20, #2043)
    - JCDL (01-20, #2183)
    - KDD (99-20, #3966)
    - OzCHI (05-20, #1271)
    - RecSys (07-20, #1279)
    - SIGIR (78-20, #5251), SIGMOD (75-20, #5378)
    - UAI (09, #76), UIST (88-19, #2076), UMAP (12-20, #728)
    - WI (03-19, #1127), WSDM (08-20, #1123), WWW (01-20, #6823)
- Journals (years, #docs):
    - ACM Transactions on Intelligent Systems and Technology (TIST) (10-20, #699)
    - ACM Transactions on Information Systems (TOIS) (83-20, #817)
    - ACM SIGIR Forum (71-20, #1032)
    - ACM Computing Surveys (CSUR) (69-20, #2053)
    - ACM Journal of Data and Information Quality (JDIQ) (09-20, #202)
    - ACM Transactions on Knowledge Discovery from Data (TKDD) (07-20, #515)
    - ACM Transactions on Asian and Low-Resource Language Information Processing (TALLIP) (02-20, #490)
    - IEEE/ACM Transactions on Audio, Speech and Language Processing (TASLP) (14-20, #1237)
    - Proceedings of the ACM on Human-Computer Interaction (PACMHCI) (17-20, #659)

Statistics of the test collection:

| #docs (T+A) | #docs (+K) |   %P |   %R |   %M |   %U | %exp | #kps |
| -----------:| ----------:| ----:| ----:| ----:| ----:| ----:| ----:|
|       72799 |      55315 | 54.2 | 11.6 | 18.8 | 15.4 | 13.0 |  4.4 |

### Queries

Citation contexts extracted from Open Access articles. Only full paragraphs
where all (most) references covered are kept. Remove explicit citation markers
He et al. [19] -> [19]


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

Evaluating output/run.t+a+k-abs.title.bm25+rm3.txt
recip_rank              all     0.2977
recall_10               all     0.3578
ndcg_cut_10             all     0.2785
Evaluating output/run.t+a+k-abs.title.bm25.txt
recip_rank              all     0.3319
recall_10               all     0.3872
ndcg_cut_10             all     0.3007
Evaluating output/run.t+a+k-abs_c1.title.bm25+rm3.txt
recip_rank              all     0.2797
recall_10               all     0.3523
ndcg_cut_10             all     0.2635
Evaluating output/run.t+a+k-abs_c1.title.bm25.txt
recip_rank              all     0.3152
recall_10               all     0.3670
ndcg_cut_10             all     0.2856
Evaluating output/run.t+a+k-abs_c2+abs_c3.title.bm25+rm3.txt
recip_rank              all     0.3055
recall_10               all     0.3611
ndcg_cut_10             all     0.2828
Evaluating output/run.t+a+k-abs_c2+abs_c3.title.bm25.txt
recip_rank              all     0.3283
recall_10               all     0.3927
ndcg_cut_10             all     0.3014
Evaluating output/run.t+a+k-abs_c2.title.bm25+rm3.txt
recip_rank              all     0.2890
recall_10               all     0.3647
ndcg_cut_10             all     0.2744
Evaluating output/run.t+a+k-abs_c2.title.bm25.txt
recip_rank              all     0.3172
recall_10               all     0.3799
ndcg_cut_10             all     0.2902
Evaluating output/run.t+a+k-abs_c3.title.bm25+rm3.txt
recip_rank              all     0.2838
recall_10               all     0.3620
ndcg_cut_10             all     0.2718
Evaluating output/run.t+a+k-abs_c3.title.bm25.txt
recip_rank              all     0.3350
recall_10               all     0.3799
ndcg_cut_10             all     0.3033
Evaluating output/run.t+a+k-pres+abs_c1.title.bm25+rm3.txt
recip_rank              all     0.2941
recall_10               all     0.3538
ndcg_cut_10             all     0.2681
Evaluating output/run.t+a+k-pres+abs_c1.title.bm25.txt
recip_rank              all     0.3249
recall_10               all     0.3698
ndcg_cut_10             all     0.2954
Evaluating output/run.t+a+k-pres.title.bm25+rm3.txt
recip_rank              all     0.2900
recall_10               all     0.3757
ndcg_cut_10             all     0.2718
Evaluating output/run.t+a+k-pres.title.bm25.txt
recip_rank              all     0.3280
recall_10               all     0.3698
ndcg_cut_10             all     0.2971
Evaluating output/run.t+a+k.title.bm25+rm3.txt
recip_rank              all     0.3118
recall_10               all     0.3767
ndcg_cut_10             all     0.2774
Evaluating output/run.t+a+k.title.bm25.txt
recip_rank              all     0.3477
recall_10               all     0.3817
ndcg_cut_10             all     0.3096
Evaluating output/run.t+a.title.bm25+rm3.txt
recip_rank              all     0.2976
recall_10               all     0.3650
ndcg_cut_10             all     0.2744
Evaluating output/run.t+a.title.bm25.txt
recip_rank              all     0.3242
recall_10               all     0.3606
ndcg_cut_10             all     0.2893
```


 
