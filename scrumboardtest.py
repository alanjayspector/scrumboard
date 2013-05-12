__author__ = 'alan'

import unittest
from scrumboard import Scrumboard
import datetime


class scrumboardTests(unittest.TestCase):
    def setUp(self):
        self.scrumboard = Scrumboard()


    def testRedCards(self):
        for card in self.scrumboard.reportRedCards(1):
            print card


suite = unittest.TestLoader().loadTestsFromTestCase(scrumboardTests)
unittest.TextTestRunner(verbosity=2).run(suite)
