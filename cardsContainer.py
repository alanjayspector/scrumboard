__author__ = 'alan'

from crud import CRUD


class cardContainer(CRUD):
    TABLE = "cardsOwnedByPeople"

    def __init__(self):
        self.__containedByPerson = True
        self.__containedByScrumboard = False
        self.cards = {}

