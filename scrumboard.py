__author__ = 'alan'

from UserDict import UserDict


class ScrumBoard(UserDict):

    def __init__(self):
        UserDict.__init__(self)
        self["cards"] = []
        self["people"] = []
        self["sprintStartDate"] = None
        self["sprintEndDate"] = None
        self["sprintHoursPerDay"] = 4



    def placeCard(self,card,location):


    def totalQAHours(self):


    def totalDevHours(self):



