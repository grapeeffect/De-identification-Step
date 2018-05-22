

#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Steps for anonymizing data attributes of applicants' information

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


"""
import itertools
from itertools import groupby
from pprint import pprint
import unittest
from mondrian import mondrian
from itertools import count
import csv
import json
import pandas as pd  
import ast
import random
import decimal
import dateutil.parser as parser
from collections import OrderedDict
from  more_itertools import unique_everseen
from collections import Counter
import sys

global perturbList, attrList, Safe, Quasi, perturbationList

def csvToJson(filename):
    """
    Firstly Convert csv format data to json
    """
    csvfile = open(filename, 'r')
    jsonfile = open(filename+".json", 'w')
    reader = csv.DictReader(csvfile)
    out = json.dumps([ row for row in reader ],encoding='latin-1')
    jsonfile.write(out)
    
def Transpose(data):
    """
    A useful function for transposing data
    """
    return map(list, zip(*data))
"""
attrList =[] #the list of all attributes that will be kept
Safe = [] #the list of attributes that are not quasi-identifiers, but good to be kept
Quasi = [] # the list of quasi-identifiers
perturbList = [] #the list of attributes that need to be perturbed
"""
def inputAttr(perturb_file, safeAttributes_file, QuasiAttributes_file):
    """
    Inputting users' designed lists of Quasi-Identifiers, safe attributes, 
    and perturbing attributes 
    """
    lines = [line.rstrip('\n') for line in open(perturb_file)]
    global perturbationList
    perturbationList = []
    for i in range(len(lines)):
        split = lines[i].split(',')
        pList = [split[0], int(split[1]) if split[1].isdigit() else float(split[1])]
        perturbationList.append(pList)
    
    global perturbList, attrList, Safe, Quasi
    
    #introduce perturbation list
    perturbList = Transpose(perturbationList)[0]
    #introduce Quasi Identifiers and Safe Indentifiers
    Safe0 = open(safeAttributes_file, "r")
    Safe = Safe0.read().split(',')
    Quasi0 = open(QuasiAttributes_file, "r")
    Quasi = Quasi0.read().split(',')
    #inputing all attributes need to be kept to attrList
    attrList = Quasi +Safe+ perturbList

def JSON_To_SafeList(data):
    """
    Remove irrelevant attributes; keep useful attributes
    """
    with open(data) as json_data:
        SampleData = json.load(json_data) #using json format
    for d in SampleData:
        for k, v in d.items():
            if v is None:
                d[k] = "default"   #assigning default value for none-exist data
    
    SampleData = ast.literal_eval(json.dumps(SampleData))
    allAttr = []
    for k, v in SampleData[1].items():
        allAttr.append(k)

    remAttr = list(set(allAttr) - set(attrList)) #removed attributes

    for d in SampleData:
        for attr in remAttr:
            del d[attr] 
    return SampleData
        

def Order_Data(data):
    """
    Order the data in an efficient way
    """
    ordData = []
    for i in range(len(data)):
        List = []
        for attr in attrList:
            List.append(data[i][attr])
        ordData.append(List)
    return ordData

def DOB_To_Year(data):
    """
    Convert all the date of births data to years
    """
    dateList = data[attrList.index('DOB')]
    yearList = ['None' if date == '' else parser.parse(date).year for date in dateList]
    newdata = [yearList if x==dateList else x for x in data]
    return newdata

def Perturb(data):
    """
    Perturb GPA/GRE/TOEFL, or some other attributes contaning grades information
    """
    T = Transpose(perturbationList)
    for i in range(len(perturbationList)):
        if type(T[1][i])==float:
            LIST0 = list(data[attrList.index(T[0][i])])
            LIST = []
            for value in LIST0:
                try:
                    LIST.append(float(value) + float(decimal.Decimal(random.randrange(-T[1][i]*100, T[1][i]*100))/100))
                except:
                    LIST.append('None')
            data = [LIST if x==LIST0 else x for x in data]
        else:
            LIST0 = list(data[attrList.index(T[0][i])])
            LIST = []
            for value in LIST0:
                try:
                    LIST.append(int(value) + int(decimal.Decimal(random.randrange(-T[1][i], T[1][i]))))
                except:
                    LIST.append('None')
            data = [LIST if x==LIST0 else x for x in data]

    return data
              

def JSON_Converter(data):
    """
    Applying the above functions to our data; data preprocessing
    """
    d1 = JSON_To_SafeList(data)
    d2 = Order_Data(d1)
    d3 = Transpose(d2)
    return d3

def GetPreview(filename):
    """
    Output a csv file with previewed data
    """
    dataT = JSON_Converter(filename+'.json')
    preview = []
    for i in range(len(Transpose(dataT))):
        preview.append(OrderedDict(zip(attrList, Transpose(dataT)[i])))
    preview = pd.DataFrame(preview)#preview unanonymized data
    preview.to_csv('PreviewData.csv', encoding='utf-8')
    return dataT

def KAnonymity(k, dataT):
    """
    k: k parameter for k-anonymity
    This function takes use of Mondrian function that implemented here 
    https://github.com/qiyuangong/Mondrian
    """
    IsRelaxedMondrian = False #Decide to relax or not
    
    dataT = DOB_To_Year(dataT)
    dataT = Perturb(dataT)
    
    listOfDict = []
    reverseDict = []
    newdata = []
    for i in range(len(Quasi)):
        originalList = list(dataT[i])
        originalList.sort(key=Counter(originalList).get, reverse=True)
        rankedAttr = list(unique_everseen(originalList))
        listOfDict.append(dict(zip(rankedAttr,range(len(rankedAttr)))))
        reverseDict.append(dict(zip(range(len(rankedAttr)),rankedAttr)))
        newdata.append([listOfDict[i][x] for x in dataT[i]])
    for i in range(len(Quasi),len(attrList)):
        newdata.append(dataT[i])
    #converting quasi-identifiers to numbers  
    result = mondrian(map(list, zip(*newdata)), k, IsRelaxedMondrian, QI_num = len(Quasi))[0]
    
    resultT = Transpose(result)
    for i in range(len(Quasi)):
        translator = reverseDict[i]
        for j in range(len(resultT[i])):
            row = resultT[i][j]
            if type(row) == int:
                dataT[i][j]=translator[row]
            else:
                dataT[i][j] = [translator[x] for x in row]
    
    for i in range(len(Quasi),len(attrList)):
        for j in range(len(resultT[i])):
            dataT[i][j] = resultT[i][j]

        
    return dataT   
            
            
    
def finalJson(dataT):
    final_json = []
    for i in range(len(Transpose(dataT))):
        final_json.append(OrderedDict(zip(attrList, Transpose(dataT)[i])))
    with open('Anonymity.json', 'w') as j:
        json.dump(final_json, j)
    final = pd.DataFrame(final_json)
    final.to_csv('Anonymity.csv', encoding='utf-8')

