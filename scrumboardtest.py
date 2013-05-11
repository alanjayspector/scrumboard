__author__ = 'alan'


import unittest
from scrumboard import Scrumboard
from utils import generateCard,generatePerson
import datetime

class checkScrumboardColors(unittest.TestCase):
    def setUp(self):
        self.scrumboard = Scrumboard(1)
        self.person = generatePerson()
        for card in self.person.getCurrentSprintCards():
            self.scrumboard.assignCardToScrumboard(card)


    def testRedCards(self):
        for card in self.scrumboard.reportRedCards(1):
            print card




if __name__ == "__main__":
    unittest.main()
