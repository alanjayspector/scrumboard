__author__ = 'alan'

import unittest
from sprint import *


class dateFormatChecks(unittest.TestCase):

    def testFormatOfStartDate(self):
        sprint = Sprint()
        with self.assertRaises(InvalidSprintDateFormat):
            sprint.startDate = "foobar"



    def testFormatOfEndDate(self):
        sprint = Sprint()
        with self.assertRaises(InvalidSprintDateFormat):
            sprint.endDate = "1-15-2013"


    def testFormatOfEndQADate(self):
        sprint = Sprint()
        with self.assertRaises(InvalidSprintDateFormat):
            sprint.endQADate = "2013/42/12"

    def testFormatOfCodeFreezeDate(self):
        sprint = Sprint()
        with self.assertRaises(InvalidSprintDateFormat):
            sprint.codeFreezeDate = "Dec 20th 2001"






if __name__ == "__main__":
    unittest.main()
