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

51915 entries with T+A+K
present: 0.5399608021160086
absent: 0.4600391978839947
|-> case 1 (all words): 0.11586832164444862
|-> case 2 (some words): 0.18840279640577265
|-> case 3 (no words): 0.15576807983374585
|-> exp. : 0.1315192920805101


./src/1_create_indexes.sh

```


 
