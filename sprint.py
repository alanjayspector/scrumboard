__author__ = 'alanspector'

from datetime import date
from scrumboard import Scrumboard


class Sprint(object):
    IDctr = 0

    def __init__(self, params = None):
        self.__sprintID = Sprint.getNextID()
        self.startDate = None
        self.endDate = None
        self.hoursPerDay = 4
        self.name = None
        self.team = None
        self.scrumBoard = Scrumboard({"sprintID":self.sprintID})

    @property
    def sprintID(self):
        return self.__sprintID

    @sprintID.setter
    def sprintID(self, value):
        return self.__sprintID

    @staticmethod
    def getNextID():
        Sprint.IDctr += 1
        return Sprint.IDctr

    def getTimeLeftInSprint(self,dateToCalculateFrom):
        pass



if __name__ == "__main__":
    def createPersonMenu():
        pass

    def createCardMenu():
        pass

    def selectCardToMoveMenu():
        pass

    def assignPersonToCardMenu():
        pass

    def mainMenu():
        pass

    def reportMenu():
        pass

