__author__ = 'alan'

import unittest
from card import *
from person import Person


class cardChecks(unittest.TestCase):
    def setUp(self):
        qa = Person({"firstName": "Bob", "lastName": "Smith", "isADeveloper": False})
        developer = Person({"firstName": "Alan", "lastName": "Spector"})
        self.card = Card({"description": "My Test Card", "qa": qa, "developer": developer})

    def testPrint(self):
        pass

    def testIsCardRed(self):
        self.card.estimatedDevHours = 8
        self.card.spentDevHours = 4
        self.assertEqual(True, self.card.isCardRed(2), "Card should be red")

    def testIsCardGreen(self):
        self.card.estimatedDevHours = 8
        self.card.spentDevHours = 4
        self.assertEqual(True, self.card.isCardGreen(10), "Card should be green")

    def testIsCardYellow(self):
        self.card.estimatedDevHours = 4
        self.card.spentDevHours = 9
        self.assertEqual(True, self.card.isCardYellow(10), "Card should be yellow")

    def testThatDoneCardsAreGreen(self):
        self.card.placeOnBoard = "CodeReview"
        self.card.placeOnBoard = "POReview"
        self.card.placeOnBoard = "QA"
        self.card.placeOnBoard = "Done"
        self.assertEqual(True, self.card.isCardGreen(0), "Card should be green")

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


suite = unittest.TestLoader().loadTestsFromTestCase(cardChecks)
unittest.TextTestRunner(verbosity=2).run(suite)