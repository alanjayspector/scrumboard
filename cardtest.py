__author__ = 'alan'

import unittest
import card
from card import *
from person import Person
import pytz
import utils


class cardColorChecks(unittest.TestCase):
    def isCardRed(self):
        testCard = Card({"estimatedDevHours": 8, "spentDevHours": 4})
        self.assertEqual(True, testCard.isCardRed(6), "Card should be red")

    def isCardGreen(self):
        testCard = Card({"estimatedDevHours": 8, "spentDevHours": 4})
        self.assertEqual(True, self.isCardGreen(10), "Card should be green")

    def isCardYellow(self):
        testCard = Card({"estimatedDevHours": 4, "spentDevHours": 9})
        self.assertEqual(True, self.isCardGreen(10), "Card should be yellow")

    def checkThatDoneCardsAreGreen(self):
        testCard = Card({"estimatedDevHours": 4, "spentDevHours": 32, "placeOnBoard": "QA"})
        testCard.placeOnBoard = "POReview"
        testCard.placeOnBoard = "Done"
        self.assertEqual(True, testCard.isCardGreen(0), "Card should be green")


class cardPlacementChecks(unittest.TestCase):
    def setUp(self):
        qa = Person({"firstName": "Bob", "lastName": "Smith", "isADeveloper": False})
        developer = Person({"firstName": "Alan", "lastName": "Spector"})
        self.card = Card({"description": "My Test Card", "qa": qa, "developer": developer})

    def testDoneWithoutPoReview(self):
        self.card.needsCodeReview = False
        self.card.needsQA = False
        with self.assertRaises(NeedsPOReviewError):
            self.card.placeOnBoard = "Done"

    def testDoneWithoutQA(self):
        self.card.needsCodeReview = False
        with self.assertRaises(NeedsQAError):
            self.card.placeOnBoard = "Done"

    def testInvalidPlacement(self):
        testCard = self.card
        with self.assertRaises(InvalidPlaceOnBoardError):
            testCard.placeOnBoard = "HappyTown"

    def testCardHadQA(self):
        self.card.needsCodeReview = False
        self.card.needsPOReview = False
        self.card.placeOnBoard = "QA"
        self.assertEqual(True, self.card.hadQA, "hadQA was not set to True")

    def testCardIsInResearch(self):
        self.card.placeOnBoard = "Research"
        self.assertEqual("Research", self.card.placeOnBoard,
                         "Card is in {} not Research".format(self.card.placeOnBoard))

    def testCardBeingSentBackToDevelopment(self):
        testCard = self.card
        testCard.placeOnBoard = "Research"
        testCard.placeOnBoard = "Development"
        testCard.placeOnBoard = "CodeReview"
        self.assertEqual(True, testCard.hadCodeReview, "hadCodeReview was not set to True")
        testCard.placeOnBoard = "Development"
        self.assertEqual(False, testCard.hadCodeReview, "hadCodeReview was not set to False")


if __name__ == "__main__":
    unittest.main()
