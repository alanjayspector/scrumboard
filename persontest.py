__author__ = 'alanspector'

import unittest
import person
from person import *
import card
from card import *

class personHourChecks(unittest.TestCase):
    def setUp(self):
        self.person = Person()
        cards = [Card() for x in range(0,3)]

    def testValidEstimatedHours(self):
        pass

    def testValidValidSpentHours(self):
        pass

    def testAllocatedHours(self):
        pass

    def testUnallocatedHours(self):
        pass

class personVelocityChecks(unittest.TestCase):

    def testVelocityInCurrentSprint(self):
        pass

    def testVelocityInPastSprint(self):
        pass

class personColorCardChecks(unittest.TestCase):

    def testRedCards(self):
        pass

    def testGreenCards(self):
        pass

    def testYellowCards(self):
        pass




if __name__ == "__main__":
    unittest.main()
