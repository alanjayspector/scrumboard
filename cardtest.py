__author__ = 'alan'

import unittest
import card
from card import *
import pytz
import utils


class cardColorChecks(unittest.TestCase):

    def testYellowCards(self):
        pass

    def testGreenCards(self):
        pass

    def testRedCards(self):
        pass



class datetimeChecks(unittest.TestCase):
    #need to turn this into an actual test... first must sleeeeeeeep

    def testCreatedDate(self):
        testCard = Card()
        dateString = testCard["createdDate"]
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
        testCard = Card()
        testCard["estimatedDevHours"] = 8
        testCard["spentDevHours"] = 4
        self.assertEqual(True, testCard.isCardRed(6), "Card should be red")

    def isCardGreen(self):
        testCard = Card()
        testCard["estimatedDevHours"] = 8
        testCard["spentDevHours"] = 4
        self.assertEqual(True, self.isCardGreen(10), "Card should be green")

    def isCardYellow(self):
        testCard = Card()
        testCard["estimatedDevHours"] = 4
        testCard["spentDevHours"] = 9
        self.assertEqual(True, self.isCardGreen(10), "Card should be yellow")

    def checkThatDoneCardsAreGreen(self):
        testCard = Card()
        testCard.moveCard("QA")
        testCard.moveCard("POReview")
        testCard.moveCard("Done")
        testCard["estimatedDevHours"] = 4
        testCard["spentDevHours"] = 32
        self.assertEqual(True, testCard.isCardGreen(0), "Card should be green")


class cardPlacementChecks(unittest.TestCase):
    def testDoneWithoutPoReview(self):
        testCard = Card()
        testCard["needsCodeReview"] = False
        testCard["needsQA"] = False
        self.assertRaises(NeedsPOReviewError, testCard.moveCard, "Done")

    def testDoneWithoutQA(self):
        testCard = Card()
        testCard["needsCodeReview"] = False
        self.assertRaises(NeedsQAError, testCard.moveCard, "Done")


    def testInvalidPlacement(self):
        testCard = Card()
        self.assertRaises(InvalidPlaceOnBoardError, testCard.moveCard, "HappyTown")

    def testCardHadQA(self):
        testCard = Card()
        testCard["needsPOReview"] = False
        testCard["needsCodeReview"] = False
        testCard.moveCard("QA")
        self.assertEqual(True, testCard["hadQA"], "hadQA was not set to True")

    def testCardIsInResearch(self):
        testCard = Card()
        testCard.moveCard("Research")
        self.assertEqual("Research", testCard["placeOnBoard"], "Card is not in Research")


    def testCardBeingSentBackToDevelopment(self):
        testCard = Card()
        testCard.moveCard("Research")
        testCard.moveCard("Development")
        testCard.moveCard("CodeReview")
        self.assertEqual(True, testCard["hadCodeReview"], "hadCodeReview was not set to True")
        testCard.moveCard("Development")
        self.assertEqual(False, testCard["hadCodeReview"], "hadCodeReview was not set to False")


if __name__ == "__main__":
    unittest.main()
