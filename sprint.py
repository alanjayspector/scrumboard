__author__ = 'alanspector'

import card
import person
import scrumboard


class Sprint(object):
    IDctr = 0

    def __init__(self):
        self.sprintID = Sprint.getNextID()
        self.startDate = None
        self.endDate = None
        self.hoursPerDay = 4
        self.name = None
        self.team = None

        pass


    def getNextID():
        Sprint.IDctr += 1
        return Sprint.IDctr


    def iterateDay(self):
        pass

    def assignPersonToCard(self):
        pass

    def createCard(self):
        pass

    def createScrumboard(self):
        pass

    def createPerson(self):
        pass

    def startSprint(self):
        pass

    def endSprint(self):
        pass



