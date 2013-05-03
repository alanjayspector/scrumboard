__author__ = 'alanspector'

import scrumboard
from scrumboard import *


class Sprint(object):
    IDctr = 0

    def __init__(self):
        self.sprintID = Sprint.getNextID()
        self.startDate = None
        self.endDate = None
        self.hoursPerDay = 4
        self.name = None
        self.team = None
        self.scrumBoard = None

        pass


    def getNextID():
        Sprint.IDctr += 1
        return Sprint.IDctr


    def iterateDay(self):
        pass

    def assignPersonToScrumboard(self):
        pass

    def assignPersonToCard(self):
        pass

    def startSprint(self):
        pass

    def endSprint(self):
        pass


if __name__ == "__main__":
    pass

