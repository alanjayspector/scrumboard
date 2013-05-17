__author__ = 'alan'

from crud import CRUD


class Container(CRUD):
    def __init__(self):
        self.__ = True
        self.__contained
        self.cards = {}

    @property
    def TABLE(self):
        if self.__containedByPerson:
            return "cardsToPeople"
        else:
            return "cardsToScrumBoard"


