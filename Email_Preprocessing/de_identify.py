#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
De-indentification of Letters

STEPS:
    
1. Remove words (ie. strings) contains special characters from each message, for example
  (1) Website addresses 
  (2) Email addresses
  (3) other cases, like an account name "@mondrian", or a hash tag "#mondrian"
  
2. Remove strings with number formats

3. Remove all proper nouns

4. Remove all Capitalized words (include accented words, exclude words from safeWords.txt)
  
"""

import os.path
import re
import nltk
from nltk.tag import pos_tag
import csv
import pandas as pd  
import unidecode
import string


#list of replacements
rep={}
#list of punctuations
punctList = '!"\'(),-./:;=?[\\]^_`{|}' 
#list of special characters
specchars=['#','@','$','%','*','<','>','&','+','~', '/','\\']
#safe words list: words which don't have to be removed 
#(avoid removing during proper nouns deletion and capitalized words deletion)
safeWords =[]
with open ("safeWords.txt", "r") as myfile:
        safeWords = myfile.read().splitlines()

def replace(match):
    return rep[match.group(0)]

def remSpecChar(messages):
    """
    Remove email address with "_EMAIL_"
    Remove website address with "_WEB_"
    Convert words containing special characters to "_SP_", like #UCSB or @UCSB
    """
    
    for j in range(len(messages)):
        message = messages[j]
        
        for string in message.split():
            while len(string)>0 and string[0] in punctList:
                string = string[1:]
            while len(string)>0 and string[-1] in punctList:
                string = string[:-1]
            #reduce the effect on punctuations when replacing spec-char strings      
            if re.findall(r'[\w\.-]+@[\w\.-]+', string):
                message = message.replace(string,'_EMAIL_')
            
        for string in message.split():
            string1 = re.sub(r'^https?:\/\/.*[\r\n]*', '_WEB_', string, flags=re.MULTILINE)
            string0 = re.sub(r'\s*(?:https?://)?www\.\S*\.[A-Za-z]{2,5}\s*', '_WEB_', string, flags=re.MULTILINE)
            string2 = re.sub(r'^[a-zA-Z0-9\-\.]+\.(com|cn|org|net|mil|edu|COM|CN|ORG|NET|MIL|EDU).*[\r\n]*', '_WEB_', string, flags=re.MULTILINE)
            # three types of web address format
            message = message.replace(string,string0)
            message = message.replace(string,string1)
            message = message.replace(string,string2)
        
        splitList = message.split()
        for i in range(len(splitList)):
            while len(splitList[i])>0 and splitList[i][0] in punctList:
                splitList[i] = splitList[i][1:]
            while len(splitList[i])>0 and splitList[i][-1] in punctList:
                splitList[i] = splitList[i][:-1]
            for word in splitList:
                for char in specchars:
                    if char in word:
                        message = message.replace(word,'_SP_')
        
        messages[j] = message 
    

def remNum(messages):
    """
    convert all numbers to #
    """
    for i in range(len(messages)):
        message = messages[i]
        messages[i] = re.sub(r'\d+', '#', message)
    
def remPN(messages):
    """
    De-identify all proper nouns (converted to "_PN_")
    """
    for i in range(len(messages)):
        message = messages[i]
        global rep
        rep = {} #collection of all replacements
        splitList = message.split()
        for k in range(len(splitList)):
            for punctuation in re.findall('[^A-Za-z0-9]',splitList[k]):
                splitList[k] = splitList[k].replace(punctuation, "")
        splitList0 = list(set(splitList))
        while '' in splitList0:
            splitList0.remove('')
        
        #using nltk package to tag proper nouns
        tagged_message = list(set([nltk.pos_tag([word])[0] for word in splitList0]))
        
        pn = [word for word,tag in tagged_message if tag == 'NNP' or tag == 'NNPS']
        for j in range(len(pn)):
            for punctuation in re.findall('[^A-Za-z0-9]',pn[j]):
                pn[j] = pn[j].replace(punctuation, "")
        
        splitList = message.split()
        
        #remove blank splitted words
        while '' in splitList:
            splitList.remove('')
        #avoid removing safewords
        for word in safeWords:
            while word in pn:
                pn.remove(word)     
        for word in pn:
                rep.update({word: '_PN_'})
        if not pn==[]:
            message = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in rep), replace, message)
        
        messages[i] = message 
        
def remCAP(messages):
    """
    De-identify all capitalized words (converted to "_CP_")
    excluding words from safelist
    """
    for j in range(len(messages)):
        message = messages[j]
        splitL = message.split()
        splitList = list(set(splitL))
        splitList = [e for e in splitList if e not in ('_PN_', '_SP_','_CP_','_WEB_','_EMAIL_','#')]
        for i in range(len(splitList)): 
        #assume there are at most three continues punctuations in any splited string
        #a while loop here may slow down the running process, so three if loops is used 
            word = splitList[i]
            if len(word)>0 and word[0] in punctList:
                splitList[i] = splitList[i][1:]
            word = splitList[i]
            if len(word)>0 and word[0] in punctList:
                splitList[i] = splitList[i][1:]
            word = splitList[i]
            if len(word)>0 and word[0] in punctList:
                splitList[i] = splitList[i][1:]
            word = splitList[i]
            if len(word)>0 and word[-1] in punctList:
                splitList[i] = splitList[i][:-1]
            word = splitList[i]
            if len(word)>0 and word[-1] in punctList:
                splitList[i] = splitList[i][:-1]
            word = splitList[i]
            if len(word)>0 and word[-1] in punctList:
                splitList[i] = splitList[i][:-1]
        global rep
        rep = {}
        for k in range(len(splitList)):
            word = splitList[k]
            if len(word)>0:
                #non-ascii words are considered as capitalized words
                if not re.match('[\x00-\x7F]', word):  
                    message = message.replace(word,"_CP_")
                if word[0].isupper() == True and word not in safeWords:
                    rep.update({word: '_CP_'})
        if not rep =={}:
            message = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in rep), replace, message)
    
        messages[j] = message
        
    

def de_identify(messages):    
    remSpecChar(messages);
    remNum(messages);
    remPN(messages);
    remCAP(messages);
    
    
    
      
