# De-identification and K-Anonymity
This project will make preparation for data mining and analysis in recommendation letters. The preparation includes applicants' private information preprocessing and de-identification of letters. This repository is a python implementation for this purpose. 

There are two main steps for de-identification procedure:

(1) Letters Anonymization (removing proper nouns, numbers, capitalized words and etc.)

(2) Applicants' Information Attributes Anonymization (perturbing GPAs, test scores, removing identifying attributes, and applying Mondrian Algorithm to make the rest quasi-identifiers satisfy K-Anonymity)

## File Description
There are two directories that respectively correspond to the two purposes above:
### Email_Preprocessing
The list of files:
* PDF - the folder of original PDF letter files
* TEXT - the folder of converted text letter files
* FinalVersion -  the folder of finalized and anonymized letter files
* Email_Preprocess.py - Run this file will output anonymized letters to the folder FinalVersion
* PDFToText.py - Transferring PDF files to Text files
* De-identify.py - main functions' implementions
* test_de_identify.py - test file of main functions in De-identify.py
* safeWords.txt - capitalized words that do not have to be removed

### Data_deidentification
* Data_Anonymity.py - input the K for K-Anonymity, the data file, and output the anonymized version
* K-Anonymity.py - main functions for Data Attributes Anonymization
* Test_KAnonymity.py test file of main functions in K-Anonymity.py
* perturbationList.txt -  the data attributes that need to be perturbed
* Quasi.txt - quasi-identifiers in all data attributes
* Safe.txt  - safe (but not quasi) identifiers that do not have to be move
* perturbationList -  attributes that need to be perturbed

Also, there are sample data files in both csv and json formats that would apply to the project:
* SampleData.csv 
* SampleData.json
## Usage and Parameters

### De-indentification of Letters

STEPS:
    
1. Remove words (ie. strings) contains special characters from each message, for example
  (1) Website addresses 
  (2) Email addresses
  (3) other cases, like an account name "@mondrian", or a hash tag "#mondrian"
  
2. Remove strings with number formats

3. Remove all proper nouns

4. Remove all Capitalized words (include accented words, exclude words from safeWords.txt)
  
  
### Anonymizing data attributes of applicants' information

STEPS

1. Convert the csv data table to a json file (assuming we have the csv file in the beginning)

2. Inputting users' required word lists of Quasi-Identifiers, safe attributes, and attributes 
needed to be perturbed, save the three lists in to one list containing all attributes

3. Remove attributes that belong to none of the three input lists

4. Order the data. Beginning with Quasi-identifiers (ordered by importance), then safe 
attributes, and finally the perturbing attributes 

5. In order to have a general comparison, we print out a previewed data csv file before the 
next step

6. Applying Mondrian Algorithm to de-identify the applicants' information, such that it 
satisfies K_Anonymity, with a user-inputted value K.

7. Safe the anonymized data into both csv file and json file.







### References

[1] Manipulating PDFs with Python | Python. (n.d.). Retrieved from https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167

[2] K. LeFevre, D. J. DeWitt, R. Ramakrishnan. Mondrian Multidimensional K-Anonymity ICDE '06: Proceedings of the 22nd International Conference on Data Engineering, IEEE Computer Society, 2006, 25

[3] Qiyuan Gong, Mondrian, (2017), GitHub repository, https://github.com/qiyuangong/Mondrian
