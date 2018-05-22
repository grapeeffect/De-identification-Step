#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Anonymizing attributes of applicants
"""

from K_Anonymity import csvToJson, finalJson, inputAttr, KAnonymity, GetPreview

inputAttr('perturbationList.txt', 'Safe.txt', 'Quasi.txt')
num = input('Enter the K of K-Anonymity: ')
filename = str(raw_input('Enter the filename: '))
csvToJson(filename)
finalJson(KAnonymity(num, GetPreview(filename)))
print('The unanonymized data is saved as PreviewData.csv')
print('The anonymized file has been saved as Anonymity.json and Anonymity.csv in the folder.')


