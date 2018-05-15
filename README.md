# De-identification and K-Anonymity
===========================
This project will make preparation for data mining and analysis in recommendation letters. The preparation includes applicants' private information preprocessing and de-identification of letters. This repository is a python implementation for this purpose. 
There are two main steps for de-identification procedure:
(1) Letters Anonymization
(2) Applicants' Data Attributes Anonymization

(1) Anonymize the letters of recommendation (e.g. remove all numbers, capitalized words, and proper nouns)(2) Anonymize the data attributes we have on each applicant (e.g. remove name and other identifying information, perturb all numeric data by a small amount of noise, ensure remaining quasi­identifiers satisfy k­anonymity)

###Motivation

###Usage and Parameters
The PDFToText.py will help transfer a directory of PDF files to another directory of TEXT files. This implemention is from here [1].
The de-identify.py focuses on the Letters Anonymization. It will take input 


###References

[1] Manipulating PDFs with Python | Python. (n.d.). Retrieved from https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
