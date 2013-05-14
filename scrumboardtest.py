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
                "description": "As a user I want to dance.", "storyPoints": 13, "estimatedDevHours": 12,
                "estimatedQAHours": 5
            })
        ]
        self.scrumboard.assignPersonToScrumboard(self.developer)
        self.scrumboard.assignPersonToScrumboard(self.qa)
        for card in self.cards:
            self.scrumboard.assignCardToScrumboard(card)
            self.developer.assignCardToSelf(card)
            self.qa.assignCardToSelf(card)


    def testTotalStoryPoints(self):
        totalStoryPoints = self.scrumboard.getTotalStoryPoints()
        self.assertEqual(18, self.scrumboard.getTotalStoryPoints(), "Story points 18 vs {}".format(totalStoryPoints))

    def testGetCard(self):
        cardID = self.cards[0].cardID
        self.assertEqual(self.scrumboard.getCard(cardID), self.cards[0], \
                         "Card[{}] does not match Card[{}]".format(cardID, self.cards[0].cardID))

    def testVelocity(self):
        velocity = self.scrumboard.getVelocity()[0]
        self.assertEqual(0, velocity, "Velocity should be 0 not {}".format(velocity))
        self.cards[0].placeOnBoard = "Research"
        self.cards[0].needsCodeReview = False
        self.cards[0].needsPOReview = False
        self.cards[0].needsQA = False
        self.cards[0].placeOnBoard = "Done"
        velocity = self.scrumboard.getVelocity()[0]
        self.assertEqual(5, velocity, "Velocity should be 5 not {}".format(velocity))


suite = unittest.TestLoader().loadTestsFromTestCase(scrumboardTests)
unittest.TextTestRunner(verbosity=2).run(suite)
