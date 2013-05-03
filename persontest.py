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
    return card

class personHourChecks(unittest.TestCase):
    def setUp(self):
        self.person = Person()
        self.person.firstName = "Alan"
        self.person.lastName = "Spector"
        self.person.currentSprintID = 1
        self.person.estimatedSprintHours = 32
        self.cards = []

        for i in range(random.randint(2,10)):
            card = generateCards(self.person.personID)
            self.person.addCardToCurrentSprint(card)
            self.cards.append(card)

        self.totalEstimatedDevHours = 0
        for card in self.cards:
            self.totalEstimatedDevHours += card.estimatedDevHours

    def testValidEstimatedHours(self):
        with self.assertRaises(PersonInvalidHour):
            self.person.estimatedSprintHours = "Foo"

    def testValidValidSpentHours(self):
        with self.assertRaises(PersonInvalidHour):
            self.person.spentSprintHours = -5

    def testIncrementingValidSpentHours(self):
        currentSpentHours = self.person.spentSprintHours
        self.person.spentSprintHours = 5
        self.assertEqual((currentSpentHours+5),self.person.spentSprintHours)

    def testAllocatedHours(self):
       self.assertEqual(self.totalEstimatedDevHours,self.person.getAllocatedHoursInSprint())

    def testUnallocatedHours(self):
        pass

class personVelocityChecks(unittest.TestCase):

    def testVelocityInCurrentSprint(self):
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
