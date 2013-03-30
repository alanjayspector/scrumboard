__author__ = 'alan'

import unittest
import card
from card import *




class cardPlacementChecks(unittest.TestCase) :


    def testDoneWithoutPoReview(self):
        testCard = Card()
        self.assertRaises(NeedsPOReviewError,testCard.moveCard, "Done")

    def testDoneWithoutQA(self):
        testCard = Card()
        self.assertRaises(NeedsQAError,testCard.moveCard, "Done")


    def testInvalidPlacement(self) :
        testCard = Card()
        self.assertRaises(InvalidPlaceOnBoardError,testCard.moveCard, "HappyTown")






if __name__ == "__main__":
    unittest.main()
