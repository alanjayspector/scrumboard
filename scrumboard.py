__author__ = 'alan'

from UserDict import UserDict


class ScrumBoard(UserDict):
    def __init__(self):
        UserDict.__init__(self)
        self["cards"] = []
        self["people"] = []
        self["startDate"] = None
        self["endDate"] = None
        self["HoursPerDay"] = 4


    def placeCard(self, card, location):
        pass


    def totalQAHours(self):
        pass


    def totalDevHours(self):
        pass



