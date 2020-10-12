# Citation Recommendation

## Pre-requisites

```
pip install pybtex
```

## Test collection

### Documents (bibtex citations) collected from ACM DL

Bibtex files from SIGIR sponsorded conferences:

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
|              |         |        |          |
| Total        |         |  33364 |    26081 |

### Queries

Citation contexts extracted from Open Access articles. Only full sentences
where all references covered are kept. The previous/following sentence is
included if relevant. We only use contexts from Introduction/Related Work.

  - 3397271.3401188 (https://doi.org/10.1145/3397271.3401188).
    Choppy: Cut Transformer for Ranked List Truncation.
    collection coverage is 12/19 references:
    [1] 10.1145/1571941.1572031
    [3] 10.1145/1458082.1458216
    [4] 10.1145/564376.564429
    [5] 10.1145/3015022.3015026
    [6] 10.1145/2983323.2983769
    [7] 10.1145/1458082.1458311
    [9] 10.1145/383952.384005
    [10] 10.1145/383952.384005
    [11] 10.1145/502585.502657
    [17] 10.1145/2009916.2009934
    [18] 10.1145/3209978.3210041
    [19] 10.1145/1277741.1277835

  - 3397271.3401204 (https://doi.org/10.1145/3397271.3401204).
    Context-Aware Term Weighting For First Stage Passage Retrieval.
    collection coverage is 4/15 references:
    [1] 10.1145/3331184.3331303
    [2] 10.1145/3159652.3159659
    [5] 10.1145/2983323.2983769
    [15] 10.1145/3077136.3080809




 
