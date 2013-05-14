__author__ = 'alan'

import unittest
from sprint import *


class sprintTests(unittest.TestCase):
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

    def testDatesAreInAppropriateOrder(self):
        sprint = Sprint()
        sprint.endDate = '2013/6/02'
        with self.assertRaises(InvalidSprintDate):
            sprint.startDate = '2013/6/03'

        sprint.endDate = None
        sprint.startDate = '2013/6/02'

        with self.assertRaises(InvalidSprintDate):
            sprint.endDate = '2013/6/01'


    def testTimeLeftInSprintCalculations(self):
        pass


suite = unittest.TestLoader().loadTestsFromTestCase(sprintTests)
unittest.TextTestRunner(verbosity=2).run(suite)



