__author__ = 'alan'

import unittest
import card
from card import *
import pytz
import utils


class datetimeChecks(unittest.TestCase):
    #need to turn this into an actual test... first must sleeeeeeeep

    def testCreatedDate(self):
        testCard = Card()
        dateString = testCard.createdDate
        easternTZ = pytz.timezone("US/Eastern")
        westernTZ = pytz.timezone("US/Pacific")
        centralTZ = pytz.timezone("US/Central")
        utcTZ = pytz.timezone("UTC")
        print dateString
        print utils.getLocalizeDateTime(dateString, easternTZ)
        print utils.getLocalizeDateTime(dateString, westernTZ)
        print utils.getLocalizeDateTime(dateString, centralTZ)
        print utils.getLocalizeDateTime(dateString, utcTZ)

        return True


class cardColorChecks(unittest.TestCase):
    def isCardRed(self):
        testCard = Card({ "estimatedDevHours" : 8, "spentDevHours": 4})
        self.assertEqual(True, testCard.isCardRed(6), "Card should be red")

    def isCardGreen(self):
        testCard = Card({ "estimatedDevHours" : 8, "spentDevHours": 4})
        self.assertEqual(True, self.isCardGreen(10), "Card should be green")

    def isCardYellow(self):
        testCard = Card({ "estimatedDevHours" : 4, "spentDevHours": 9})
        self.assertEqual(True, self.isCardGreen(10), "Card should be yellow")

    def checkThatDoneCardsAreGreen(self):
        testCard = Card({ "estimatedDevHours" : 4, "spentDevHours": 32, "placeOnBoard": "QA"})
        testCard.placeOnBoard = "POReview"
        testCard.placeOnBoard = "Done"
        self.assertEqual(True, testCard.isCardGreen(0), "Card should be green")


class cardPlacementChecks(unittest.TestCase):
    def testDoneWithoutPoReview(self):
        testCard = Card({"needsCodeReview":False, "needsQA":False})
        with self.assertRaises(NeedsPOReviewError):
            testCard.placeOnBoard = "Done"


    def testDoneWithoutQA(self):
        testCard = Card({"needsCodeReview":False})
        with self.assertRaises(NeedsQAError):
            testCard.placeOnBoard = "Done"


    def testInvalidPlacement(self):
        testCard = Card()
        with self.assertRaises(InvalidPlaceOnBoardError):
            testCard.placeOnBoard = "HappyTown"

    def testCardHadQA(self):
        #note since dicts aren't ordered if I included placeOnBoard this could potentially raise an exception since the
        #the needs* attributes need to be set first
        testCard = Card({"needsCodeReview":False, "needsPOReview":False})
        testCard.placeOnBoard = "QA"
        self.assertEqual(True, testCard.hadQA, "hadQA was not set to True")

    def testCardIsInResearch(self):
        testCard = Card({"placeOnBoard":"Research"})
        self.assertEqual("Research", testCard.placeOnBoard, "Card is not in Research")


    def testCardBeingSentBackToDevelopment(self):
        testCard = Card()
        testCard.placeOnBoard = "Research"
        testCard.placeOnBoard = "Development"
        testCard.placeOnBoard = "CodeReview"
        self.assertEqual(True, testCard.hadCodeReview, "hadCodeReview was not set to True")
        testCard.placeOnBoard = "Development"
        self.assertEqual(False, testCard.hadCodeReview, "hadCodeReview was not set to False")


if __name__ == "__main__":
    unittest.main()
