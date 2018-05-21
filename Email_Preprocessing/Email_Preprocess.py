#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Email Preprocessing:
    Converting all pdf email files in "PDF/" to text files in "TEXT/";
    Applying de_identify() function to all emails;
    Saving the final version of de-identified emails to the folder "FinalVersion/"
    in txt formats.
"""
import os
import sys, getopt
from de_identify import de_identify 
from PDFToText import convertMultiple

pdfDir = "PDF/"
txtDir = "TEXT/"
convertMultiple(pdfDir, txtDir)

       
all_files = os.listdir("TEXT/")
txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
ListOfText = []
for i in range(len(txt_files)):
    with open ("TEXT/"+txt_files[i], "r") as myfile:
        ListOfText.append(myfile.read())

de_identify(ListOfText);

for i in range(len(txt_files)):
    text_file = open("FinalVersion/"+ txt_files[i]+".txt", "w")
    text_file.write(ListOfText[i])
    text_file.close()
