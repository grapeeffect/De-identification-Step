#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import unittest
from K_Anonymity import Transpose, inputAttr, Order_Data, DOB_To_Year, Perturb, KAnonymity
from itertools import groupby
#Sample Lists
"""
Quasi = ['Gender', 'Category','Major1']
Safe = ['Application Quarter', 'ID']   
perturbList = ['DOB', 'UG1 GPA', 'GRE Q']
attrList =Quasi+Safe+perturbList
"""

inputAttr('TestPerturb.txt', 'TestSafe.txt', 'TestQuasi.txt')

#Sample Data
#we keep IDs here for comparison
Sample = [{'Application Quarter': 'Winter 2019',
  'Category': 'White',
  'DOB': '7/27/98',
  'ID': '0',
  'GRE Q': '110',
  'Gender': 'F',
  'Major1': 'Math',
  'UG1 GPA': '1.00'},
 {'Application Quarter': 'Fall 2019',
  'Category': 'White',
  'DOB': '1/27/97',
  'ID': '1',
  'GRE Q': '120',
  'Gender': 'M',
  'Major1': 'Math',
  'UG1 GPA': '2.00'},
 {'Application Quarter': 'Spring 2019',
  'Category': 'Black',
  'DOB': '7/27/96',
  'ID': '2',
  'GRE Q': '130',
  'Gender': 'M',
  'Major1': 'Chemistry',
  'UG1 GPA': '3.00'},
 {'Application Quarter': 'Winter 2019',
  'Category': 'White',
  'DOB': '7/27/95',
  'ID': '3',
  'GRE Q': '140',
  'Gender': 'F',
  'Major1': 'Chemistry',
  'UG1 GPA': '4.00'},
 {'Application Quarter': 'Winter 2019',
  'Category': 'Asian',
  'DOB': '7/27/94',
  'ID': '4',
  'GRE Q': '150',
  'Gender': 'M',
  'Major1': 'Physics',
  'UG1 GPA': '5.00'},
 {'Application Quarter': 'Winter 2019',
  'Category': 'Asian',
  'DOB': '7/27/93',
  'ID': '5',
  'GRE Q': '160',
  'Gender': 'M',
  'Major1': 'Chemistry',
  'UG1 GPA': '6.00'},
 {'Application Quarter': 'Fall 2019',
  'Category': 'White',
  'DOB': '7/27/92',
  'ID': '6',
  'GRE Q': '170',
  'Gender': 'F',
  'Major1': 'Physics',
  'UG1 GPA': '7.00'},
  {'Application Quarter': 'Spring 2019',
  'Category': 'Black',
  'DOB': '7/27/91',
  'ID': '7',
  'GRE Q': '180',
  'Gender': 'F',
  'Major1': 'Physics',
  'UG1 GPA': '8.00'}
 ]

class K_Anonymity_Test(unittest.TestCase):
    def test_Order_Data(self):
        """
        Test the function Order_Data()
        """
        result = Transpose(Order_Data(Sample))
        
        self.assertTrue(any(elm in ['F', 'M'] for elm in result[0]))
        self.assertTrue(any(elm in ['White', 'Black', 'Asian'] for elm in result[1]))
        self.assertTrue(any(elm in ['Math', 'Chemistry', 'Physics'] for elm in result[2]))
        self.assertTrue(any(elm in ['Winter 2019', 'Spring 2019', 'Fall 2019'] for elm in result[3]))
        self.assertTrue(any(elm in [str(n) for n in range(0,8)] for elm in result[4]))
    
    def test_DOB_To_Year(self):
        """
        Test the conversion from DOB to years
        """
        result = DOB_To_Year(Transpose((Order_Data(Sample))))
        self.assertTrue(any(elm in range(1991,1999) for elm in result[5]))

    def test_Perturb(self):
        """
        Test the perturbation function
        """
        result = Perturb(DOB_To_Year(Transpose((Order_Data(Sample)))))
        
        preYear = DOB_To_Year(Transpose((Order_Data(Sample))))[5]
        preYear = [int(n) for n in preYear]
        postYear = result[5]
        
        preGPA = Transpose((Order_Data(Sample)))[6]
        preGPA = [float(n) for n in preGPA]
        postGPA = result[6]
        
        preGRE = Transpose((Order_Data(Sample)))[7]
        preGRE = [int(n) for n in preGRE]
        postGRE = result[7]
        
        self.assertTrue(all(abs(preYear[i]-postYear[i])<=1 for i in range(0,8)))
        self.assertTrue(all(abs(preGPA[i]-postGPA[i])<=0.2 for i in range(0,8)))
        self.assertTrue(all(abs(preGRE[i]-postGRE[i])<=5 for i in range(0,8)))

    def test_KAnonymity(self):
        """
        Test the modified Mondiran Algorithm
        """
        result0 = KAnonymity(2,Transpose((Order_Data(Sample))))
        self.assertTrue(all(min([len(list(group)) for key, group in groupby(result0[i])])>=2 for i in range(0,3)))
        result = KAnonymity(3,Transpose((Order_Data(Sample))))
        self.assertTrue(all(min([len(list(group)) for key, group in groupby(result[i])])>=3 for i in range(0,3)))
        
  

if __name__ == '__main__':
    unittest.main()
