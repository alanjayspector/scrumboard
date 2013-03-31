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
        self.assertEqual(True,testCard["hadQA"], "hadQA was not set")





if __name__ == "__main__":
    unittest.main()
