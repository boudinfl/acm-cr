# Citation Recommendation

## Pre-requisites

```
pip install pybtex

# install Science Parse
# https://github.com/allenai/science-parse/
brew tap AdoptOpenJDK/openjdk
brew cask install adoptopenjdk8
sbt -java-home /Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/ cli/assembly
java -Xmx6g -jar cli/target/scala-2.12/science-parse-cli-assembly-3.0.1.jar ../citation_rec/data/open-access-papers/ -o ../citation_rec/data/open-access-papers/
```

## Test collection

### Documents (bibtex citations) collected from ACM DL

`bibtex` files from SIGs IR/KDD/CHI/WEB/MOD sponsored conferences and journals:

| Venue        | Years   | #bib   | #(T+A+K) |
| ------------ |:-------:| ------:|---------:|
| ADCS         | '12-'19 |    115 |       88 |
| AIRS         | '08-'09 |    120 |       84 |
| AVI          | '94-'20 |   1108 |      970 |
| BooksOnline  | '08-'12 |     57 |       43 |
| CHI/CHI-EA   | '82-'20 |  19446 |    15364 |
| CHIIR        | '16-'20 |    374 |      357 |
| CIKM         | '93-'20 |   5497 |     4764 |
| CIR          | '11     |      7 |        7 |
| CompSci      | '13     |      8 |        6 |
| CSCW         | '86-'19 |   2726 |     2211 |
| DL           | '96-'20 |    244 |       41 |
| DocEng       | '01-'20 |    971 |      754 |
| DTMBIO       | '08-'15 |    151 |      117 |
| ESAIR        | '09-'15 |    101 |       84 |
| FIRE         | '12-'19 |     91 |       79 |
| ICTIR        | '13-'20 |    313 |      297 |
| IIIX         | '06-'14 |    242 |      181 |
| IUI          | '93-'20 |   2043 |     1735 |
| JCDL         | '01-'20 |   2183 |     1808 |
| KDD          | '99-'20 |   3966 |     3589 |
| OzCHI        | '05-'20 |   1271 |     1216 |
| RecSys       | '07-'20 |   1279 |     1197 |
| SIGIR        | '78-'20 |   5251 |     3775 |
| SIGMOD       | '75-'20 |   5378 |     2360 |
| UAI          | '09     |     76 |        0 |
| UIST         | '88-'19 |   2076 |     1614 |
| UMAP         | '12-'20 |    728 |      652 |
| WI           | '03-'19 |   1127 |      343 |
| WSDM         | '08-'20 |   1123 |     1051 |
| WWW          | '01-'20 |   6823 |     5962 |
| (journals)   |         |        |          |
| TIST journal | '10-'20 |    699 |       -  |
| TOIS journal | '83-'20 |    817 |          |
| SIGIR-Forum  | '71-'20 |   1032 |          |
| Comp. Surv.  | '69-'20 |   2053 |          |
|              |         |  4787  |     2386 |
|              |         |        |          |
| Total        |         |  68425 |    51915 |


### Queries

Citation contexts extracted from Open Access articles. Only full paragraphs
where all (most) references covered are kept. Remove explicit citation markers
He et al. [19] -> [19]


## Document retrieval

```
./src/0_create_data.sh

53131 entries with T+A+K
present: 0.5403410268535919
absent: 0.45965897314641135
|-> case 1 (all words): 0.11542222320070421
|-> case 2 (some words): 0.18819805014164132
|-> case 3 (no words): 0.15603869980403845
|-> exp. : 0.1315236158617357


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


 
