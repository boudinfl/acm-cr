# Venues

This test collection contains the documents (BibTeX reference files) from the following venues (years, #nb of docs):

- Conferences:
    - ADCS (12-19, #115), AIRS (08-09, #120), AKBC (12-13, #44), AND (08-10, #48), ASONAM (09-19, #2033), AVI (94-20, #1108)
    - BooksOnline (08-12, #57)
    - CERI (16-18, #41), CHI/CHI-EA (82-20, #19446), CHIIR (16-20, #374), CIKM (93-20, #5497),
      CIR (11, #7), CLEF (00-15), CompSci (13, #8), Compute (08-17, #242), CSCW (86-19, #2726)
    - DL (96-00, #244), DocEng (01-20, #971), DTMBIO (08-15, #151), 
      DLRS (16-18, #24)
    - ECIR (02-14, #921), ESAIR (09-15, #101)
    - FAT* (19-20, #143), FIRE (12-19, #91)
    - HCIR (12-13, #9), HT (87-20, #1339)
    - ICML (04-09, #843), ICTIR (09, 11, 13-20, #313), ICTS (12-16, #238), IIIX (06-14, #242), IUI (93-20, #2043)
    - JCDL (01-20, #2183)
    - KDD (99-20, #3966)
    - NLPIR (18-19, #43)
    - MobileHCI (05-20, #1741), MUM (04-20, #737)
    - OzCHI (05-20, #1271)
    - PervasiveHealth (16, #60), PODS (82-20, #1369)
    - RecSys (07-20, #1279)
    - SAICSIT (02-19, #722), SIGDOC (82-20, #1492) SIGIR (78-20, #5251), SIGMOD (75-20, #5378), SPIRE (99-15, #497)
    - UAI (09, 14, #170), UbiComp (01-20), UIST (88-19, #2076), UMAP (12-20, #728)
    - VLDB (00-07, #1016), PVLDB (08-20, #2717)
    - WI (03-19, #1127), WIDM (99-19, #214), WIMS (11-20, #461), WSDM (08-20, #1123), WWW (01-20, #6823)
    - YLRC (10, #7)
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
    - ACM Transactions on Management Information Systems (tmis) (08-20, #200)
    - IEEE/ACM Transactions on Audio, Speech and Language Processing (TASLP)
      (14-20, #1237)
    - Proceedings of the ACM on Human-Computer Interaction (PACMHCI)
      (17-20, #659)
    - ACM Transactions on Interactive Intelligent Systems (tiis) (11-20, #250)
- Journals (non ACM)
    - User Modeling and User-Adapted Interaction (klu-user) (97-19, #362)
    - International Journal of Human-Computer Studies (ijhc) (94-20, #1872)
    - Foundations and Trends in Information Retrieval (trir) (06-18, #31)
    - The Journal of Machine Learning Research (jmlr) (01-19, #2042)
    - SIAM Journal on Computing (sicomp) (84-17, #2216)
    - IEEE Transactions on Knowledge and Data Engineering (tkde) (89-20, #3308)
    - Journal of Artificial Intelligence Research (jair) (93-19, #1094)
    - Journal of the Association for Information Science and Technology (jaist) (14-20, #1245)
    - Journal of the American Society for Information Science and Technology (jasist) (01-13, #2261)
    - Information Retrieval (infre) (99-19, #520)

## Using bibtool to remove duplicates from Bibtex files

```
cat *.bib > big.bib
bibtool -- 'print.deleted.entries = off' -d big.bib -o big-nodup.bib
```