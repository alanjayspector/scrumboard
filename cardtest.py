__author__ = 'alan'

import unittest
import card
from card import *




class cardPlacementChecks(unittest.TestCase) :


    def testDoneWithoutPoReview(self):
        testCard = Card()
        testCard["needsCodeReview"] = False
        testCard["needsQA"]  = False
        self.assertRaises(NeedsPOReviewError,testCard.moveCard, "Done")

    def testDoneWithoutQA(self):
        testCard = Card()
        testCard["needsCodeReview"] = False
        self.assertRaises(NeedsQAError,testCard.moveCard, "Done")


    def testInvalidPlacement(self) :
        testCard = Card()
        self.assertRaises(InvalidPlaceOnBoardError,testCard.moveCard, "HappyTown")

    def testCardHadQA(self):
        testCard = Card()
        testCard["needsPOReview"] = False
        testCard["needsCodeReview"] = False
        testCard.moveCard("QA")
        self.assertEqual(True,testCard["hadQA"], "hadQA was not set to True")

    def testCardIsInResearch(self):
        testCard = Card()
        testCard.moveCard("Research")
        self.assertEqual("Research", testCard["placeOnBoard"], "Card is not in Research")


    def testCardBeingSentBackToDevelopment(self):
        testCard = Card()
        testCard.moveCard("Research")
        testCard.moveCard("Development")
        testCard.moveCard("CodeReview")
        self.assertEqual(True,testCard["hadCodeReview"], "hadCodeReview was not set to True")
        testCard.moveCard("Development")
        self.assertEqual(False,testCard["hadCodeReview"], "hadCodeReview was not set to False")





if __name__ == "__main__":
    unittest.main()
