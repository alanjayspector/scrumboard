__author__ = 'alanspector'

import unittest
import person
from person import *
import card
from card import *
import random


def generateCards(personID):
    card = Card()
    card.storyPoints = Card.cardDataMap["storyPoints"][random.randint(0,5)]
    card.estimatedDevHours = random.randint(1,16)
    card.description = "Random Description:%d" % random.randint(1,375)
    card.personID = personID

class personHourChecks(unittest.TestCase):
    def setUp(self):
        self.person = Person()
        self.person.firstName = "Alan"
        self.person.lastName = "Spector"
        self.person.currentSprintID = 1
        self.person.estimatedSprintHours = 32




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
