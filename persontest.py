__author__ = 'alanspector'

import unittest
from person import *
from card import Card
from utils import generateCard,generatePerson
import random





class personHourChecks(unittest.TestCase):
    def setUp(self):
        self.person = generatePerson()
        print self.person.fullName


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

        cards[random.randint(0,(len(cards)-1))].placeOnBoard = "CodeReview"



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
