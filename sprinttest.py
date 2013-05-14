__author__ = 'alan'

import unittest
from sprint import *


class sprintTests(unittest.TestCase):
    def setUp(self):
        self.sprint = Sprint()
        self.sprint.startDate = '2013/6/02'
        self.sprint.codeFreezeDate = '2013/6/15'
        self.sprint.endQADate = '2013/6/19'
        self.sprint.endDate = '2013/6/21'

    def testFormatOfStartDate(self):
        with self.assertRaises(InvalidSprintDateFormat):
            self.sprint.startDate = "foobar"


    def testFormatOfEndDate(self):
        with self.assertRaises(InvalidSprintDateFormat):
            self.sprint.endDate = "1-15-2013"


    def testFormatOfEndQADate(self):
        with self.assertRaises(InvalidSprintDateFormat):
            self.sprint.endQADate = "2013/42/12"

    def testFormatOfCodeFreezeDate(self):
        with self.assertRaises(InvalidSprintDateFormat):
            self.sprint.codeFreezeDate = "Dec 20th 2001"

    def testStartDatesAreAppropriate(self):
        with self.assertRaises(InvalidSprintDate):
            self.sprint.startDate = '2013/6/21'

        with self.assertRaises(InvalidSprintDate):
            self.sprint.startDate = '2013/6/16'

        with self.assertRaises(InvalidSprintDate):
            self.sprint.startDate = '2013/6/20'

    def testEndDatesAreAppropriate(self):
        with self.assertRaises(InvalidSprintDate):
            self.sprint.endDate = '2013/6/1'

        with self.assertRaises(InvalidSprintDate):
            self.sprint.endDate = '2013/6/14'

        with self.assertRaises(InvalidSprintDate):
            self.sprint.endDate = '2013/6/18'

    def testEndQADatesAreAppropriate(self):
        with self.assertRaises(InvalidSprintDate):
            self.sprint.endQADate = '2013/6/1'

        with self.assertRaises(InvalidSprintDate):
            self.sprint.endQADate = '2013/6/14'

        with self.assertRaises(InvalidSprintDate):
            self.sprint.endQADate = '2013/6/22'

    def testCodeFreezeDatesAreAppropriate(self):
        with self.assertRaises(InvalidSprintDate):
            self.sprint.codeFreezeDate = '2013/6/1'

        with self.assertRaises(InvalidSprintDate):
            self.sprint.codeFreezeDate = '2013/6/20'

        with self.assertRaises(InvalidSprintDate):
            self.sprint.codeFreezeDate = '2013/6/22'

    def testTimeLeftInSprintCalculations(self):
        devTimeLeftInSprint = self.sprint.getDevTimeLeftInSprint("2013/6/2")

        self.assertEquals(52, devTimeLeftInSprint,
                          "Dev Time left in sprint was {} it should had been 52".format(devTimeLeftInSprint))

        with self.assertRaises(InvalidSprintDate):
            self.sprint.getDevTimeLeftInSprint("2013/1/2")


suite = unittest.TestLoader().loadTestsFromTestCase(sprintTests)
unittest.TextTestRunner(verbosity=2).run(suite)



