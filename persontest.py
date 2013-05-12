__author__ = 'alanspector'

import unittest
from person import *
from card import Card
import random


class personHourChecks(unittest.TestCase):
    def setUp(self):
        self.developer = Person({"firstName": "Alan", "lastName": "Spector", "estimatatedSprintHours": 32})
        self.developer.addCardToCurrentSprint(Card({
            "description": "As a user I want to fly.", "storyPoints": 5, "estimatedDevHours": 18
        }))


    def testValidEstimatedHours(self):
        with self.assertRaises(PersonInvalidHour):
            self.developer.estimatedSprintHours = "Foo"

    def testValidValidSpentHours(self):
        with self.assertRaises(PersonInvalidHour):
            self.developer.spentSprintHours = -5

    def testDevAllocatedHours(self):
        totalEstimatedDevHours = 0
        for card in self.developer.getCurrentSprintCards():
            totalEstimatedDevHours += card.estimatedDevHours
        self.assertEqual(totalEstimatedDevHours, self.developer.getAllocatedHoursInSprint())

    def testQAAllocatedHours(self):
        totalEstimatedQAHours = 0
        for card in self.developer.getCurrentSprintCards():
            totalEstimatedQAHours += card.estimatedQAHours
        self.developer.isADeveloper = False
        self.assertEqual(totalEstimatedQAHours, self.developer.getAllocatedHoursInSprint())


class personVelocityChecks(unittest.TestCase):
    def setUp(self):
        self.developer = Person({"firstName": "Alan", "lastName": "Spector", "estimatatedSprintHours": 32})
        self.developer.addCardToCurrentSprint(Card({
            "description": "As a user I want to fly.", "storyPoints": 5, "estimatedDevHours": 18
        }))


    def testVelocityInCurrentSprint(self):
        pass


class personColorCardChecks(unittest.TestCase):
    def setUp(self):
        self.developer = Person({"firstName": "Alan", "lastName": "Spector", "estimatatedSprintHours": 32})
        self.developer.addCardToCurrentSprint(Card({
            "description": "As a user I want to fly.", "storyPoints": 5, "estimatedDevHours": 18
        }))


    def testRedCards(self):
        pass

    def testGreenCards(self):
        pass

    def testYellowCards(self):
        pass


if __name__ == "__main__":
    unittest.main()
