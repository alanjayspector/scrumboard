__author__ = 'alan'

import unittest
from scrumboard import Scrumboard
from person import Person
from card import Card
import datetime


class scrumboardTests(unittest.TestCase):
    def setUp(self):
        self.scrumboard = Scrumboard()
        self.developer = Person({"firstName": "Alan", "lastName": "Spector", "estimatedSprintHours": 32})
        self.qa = Person({"firstName": "Bob", "lastName": "Smith", "estimatedSprintHours": 16})
        self.cards = [
            Card({
                "description": "As a user I want to fly.", "storyPoints": 5, "estimatedDevHours": 18,
                "estimatedQAHours": 4
            }),
            Card({
                "description": "As a user I want to dance.", "storyPoints": 20, "estimatedDevHours": 12,
                "estimatedQAHours": 5
            })
        ]
        self.scrumboard.assignPersonToScrumboard(self.developer)
        self.scrumboard.assignPersonToScrumboard(self.qa)
        for card in self.cards:
            self.developer.assignCardToSelf(card)
            self.qa.assignCardToSelf(card)


    def testTotalStoryPoints(self):
        pass


suite = unittest.TestLoader().loadTestsFromTestCase(scrumboardTests)
unittest.TextTestRunner(verbosity=2).run(suite)
