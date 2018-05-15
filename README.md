# De-identification and K-Anonymity
This project will make preparation for data mining and analysis in recommendation letters. The preparation includes applicants' private information preprocessing and de-identification of letters. This repository is a python implementation for this purpose. 

There are two main steps for de-identification procedure:

(1) Letters Anonymization (removing proper nouns, numbers, capitalized words and etc.)

(2) Applicants' Information Attributes Anonymization (perturbing GPAs, test scores, removing identifying attributes, and applying Mondrian Algorithm to make the rest quasi-identifiers satisfy K-Anonymity)

## File Description
The list of files:
* PDFToText.py - Transferring PDF files to Text files
* K-Anonymity.py - Data Attributes Anonymization
* De-identify.py - Letters De-identification
* PDF - the folder of original PDF letter files
* TEXT - the folder of converted text letter files
* FinalVersion -  the folder of finalized and anonymized letter files
* perturbationList.txt -  the data attributes that need to be perturbed
* safeWords.txt -  words that do not have to be removed even it's capitalized
* Quasi.txt - quasi-identifiers in all data attributes
* Safe.txt  - safe (but not quasi) identifiers that do not have to be move
* SampleData.csv -
* PreviewData.csv - 
* Anonymity.csv
* Anonymity.json -

### Usage and Parameters

Firstly, drop the PDF files of letters you need to preprocess to the folder "PDF". The PDFToText.py will help transfer a directory of PDF files to another directory of TEXT files. This implemention is from here [1].

The de-identify.py provides functions implemented on the Letters Anonymization. The function `remSpecChar()` deals with spectial characters.

### Instructions





### References

[1] Manipulating PDFs with Python | Python. (n.d.). Retrieved from https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167

[2] K. LeFevre, D. J. DeWitt, R. Ramakrishnan. Mondrian Multidimensional K-Anonymity ICDE '06: Proceedings of the 22nd International Conference on Data Engineering, IEEE Computer Society, 2006, 25
