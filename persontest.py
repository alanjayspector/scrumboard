__author__ = 'alanspector'

import unittest
import person
from person import *
import card
from card import *
import random


def generateCard(personID):
    card = Card()
    card.storyPoints = Card.cardDataMap["storyPoints"][random.randint(0,5)]
    card.estimatedDevHours = random.randint(1,16)
    card.estimatedQAHours= random.randint(2,6)
    card.description = "Random Description:%d" % random.randint(1,375)
    card.personID = personID
    return card

def generatePerson():
    person = Person({ "firstName":"Alan", "lastName": "Spector", \
                      "currentSprintID":1, "estimatedSprintHours":32 })

    for i in range(random.randint(2,10)):
        card = generateCard(person.personID)
        person.addCardToCurrentSprint(card)

    return person

class personHourChecks(unittest.TestCase):
    def setUp(self):
        self.person = generatePerson()


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

    def testDevAllocatedHours(self):
        totalEstimatedDevHours = 0
        for card in self.person.getCurrentSprintCards() :
            totalEstimatedDevHours += card.estimatedDevHours
        self.assertEqual(totalEstimatedDevHours,self.person.getAllocatedHoursInSprint())

    def testQAAllocatedHours(self):
        totalEstimatedQAHours = 0
        for card in self.person.getCurrentSprintCards() :
            totalEstimatedQAHours += card.estimatedQAHours
        self.person.isADeveloper = False
        self.assertEqual(totalEstimatedQAHours, self.person.getAllocatedHoursInSprint())


class personVelocityChecks(unittest.TestCase):
    def setUp(self):
        self.person = generatePerson()
        cards = self.person.getCurrentSprintCards()
        self.totalStoryPoints = 0;
        for card in cards:
            self.totalStoryPoints += card.storyPoints
            card.placeOnBoard = "CodeReview"

        cards[random.randint(0,cards.len())].placeOnBoard = "CodeReview"



    def testVelocityInCurrentSprint(self):
        pass


class personColorCardChecks(unittest.TestCase):
    def setUp(self):
        self.person = generatePerson()


    def testRedCards(self):
        pass

    def testGreenCards(self):
        pass

    def testYellowCards(self):
        pass




if __name__ == "__main__":
    unittest.main()
