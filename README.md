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

Bibtex files from SIGIR/SIGKDD/SIGCHI sponsored conferences:

| Venue        | Years   | #bib   | #(T+A+K) |
| ------------ |:-------:| ------:|---------:|
| SIGIR        | '78-'20 |   5251 |     3775 |
| CHIIR        | '16-'20 |    374 |      357 |
| WSDM         | '08-'20 |   1123 |     1051 |
| JCDL         | '01-'20 |   2183 |     1808 |
| CIKM         | '93-'20 |   5497 |     4764 |
| ICTIR        | '13-'20 |    313 |      297 |
| RecSys       | '07-'20 |   1279 |     1197 |
| ADCS         | '12-'19 |    115 |       88 |
| DocEng       | '01-'20 |    971 |      754 |
| FIRE         | '12-'19 |     91 |       79 |
| KDD          | '99-'20 |   3966 |     3589 |
| WWW          | '01-'20 |   6823 |     5962 |
| SIGMOD       | '75-'20 |   5378 |     2360 |
| IUI          | '93-'20 |   2043 |     1735 |
| DL           | '96-'20 |    244 |       41 |
| AVI          | '94-'20 |   1108 |      970 |
| BooksOnline  | '08-'12 |     57 |       43 |
| CIR          | '11     |      7 |        7 |
| CompSci      | '13     |      8 |        6 |
| DTMBIO       | '08-'15 |    151 |      117 |
| ESAIR        | '09-'15 |    101 |       84 |
| CSCW         | '86-'19 |   2726 |     2211 |
| IUST         | '88-'19 |   2076 |     1614 |
| UMAP         | '12-'20 |    728 |      652 |
| CHI/CHI-EA   | '82-'20 |  19446 |    15364 |
|              |         |        |          |
| Total        |         |  62059 |    47209 |

### Queries

Citation contexts extracted from Open Access articles. Only full sentences
where all references covered are kept. The previous/following sentence is
included if relevant. We only use contexts from Introduction/Related Work.

  - 3397271.3401204 (https://doi.org/10.1145/3397271.3401204).
    Context-Aware Term Weighting For First Stage Passage Retrieval.
    collection coverage is 4/15 references:
    [1] 10.1145/3331184.3331303
    [2] 10.1145/3159652.3159659
    [5] 10.1145/2983323.2983769
    [15] 10.1145/3077136.3080809

## Document retrieval

```
./src/0_create_data.sh

# 31295 entries with T+A+K
# present: 0.5585539082694746
# absent: 0.44144609173052485
# |-> case 1 (all words): 0.1233575106268052
# |-> case 2 (some words): 0.18370808173335545
# |-> case 3 (no words): 0.13438049937034974
# |-> exp. : 0.11816392772776158
```


 
