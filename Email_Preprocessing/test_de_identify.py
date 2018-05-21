#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import unittest
from de_identify import de_identify, remSpecChar, remNum, remPN, remCAP

TestMessages0 = ["Contact me at @ucsb",
                "Contact me at mondrian@ucsb.edu",
                "website: www.mondrian.com",
                "Please visit http://sec.org",
                "Her website is echo.net",
                "GPA is around 4.0",
                "They are from France and Germany.",
                "What happened to Batme and ATM?",
                "This is 'UCSB CORP'.",
                "I attend the École of Awesome. All écoles are awesome."
        ]


class de_identify_Test(unittest.TestCase):
    def test_remSpecChar(self):
        """
        Test whether the remSpecChar() function works for detecting special character strings,
        email addresses and web addresses.
        """
        TestMessages = TestMessages0[0:5]
        remSpecChar(TestMessages)
        result = TestMessages
        self.assertEqual(result[0], 'Contact me at _SP_')
        self.assertEqual(result[1], 'Contact me at _EMAIL_')
        self.assertEqual(result[2], 'website: _WEB_')
        self.assertEqual(result[3], 'Please visit _WEB_')
        self.assertEqual(result[4], 'Her website is _WEB_')
    
    def test_remNum(self):
        """
        Test the removal of number-format strings
        """
        TestMessages = [TestMessages0[5]]
        remNum(TestMessages)
        result = TestMessages
        self.assertEqual(result[0], 'GPA is around #.#')

    def test_remPN(self):
        """
        Test the removal of proper nouns
        """
        TestMessages = [TestMessages0[6]]
        remPN(TestMessages)
        result = TestMessages
        self.assertEqual(result[0], 'They are from _PN_ and _PN_.')

    def test_remCAP(self):
        """
        Test the removal of capitalized words
        Test the exception of 'safeWords' list 
        Test the removal of accented words (which are considered as capitalized words)
        """
        TestMessages = TestMessages0[7:10]
        remCAP(TestMessages)
        result = TestMessages
        self.assertEqual(result[0], 'What happened to _CP_ and _CP_?')
        self.assertEqual(result[1], "This is '_CP_ _CP_'.")
        self.assertEqual(result[2], 'I attend the _CP_ of _CP_. All _CP_ are awesome.')

  

if __name__ == '__main__':
    unittest.main()
