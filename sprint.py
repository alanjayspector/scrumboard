__author__ = 'alanspector'

import datetime
from scrumboard import Scrumboard


class Sprint(object):
    IDctr = 0
    DATE_FORMAT = "%Y/%m/%d"

    def __init__(self, params = None):
        self.__sprintID = Sprint.getNextID()
        self.startDate = None
        self.endDate = None
        self.hoursPerDay = 4
        self.codeFreezeDate = None
        self.endQADate = None
        self.name = None
        self.team = None
        self.scrumBoard = Scrumboard(self.sprintID)

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

    def getDevTimeLeftInSprint(self,dateToCalculateFrom = datetime.datetime.today()):
        codeFreezeDate = datetime.datetime.strptime(self.codeFreezeDate,Sprint.DATE_FORMAT)
        return self.getTimeLeftInSprint(dateToCalculateFrom,codeFreezeDate)

    def getQATimeLeftInSprint(self,dateToCalculateFrom = datetime.datetime.today()):
        endQADate = datetime.datetime.strptime(self.endQADate,Sprint.DATE_FORMAT)
        return self.getTimeLeftInSprint(dateToCalculateFrom,endQADate)

    def getTimeLeftInSprint(self, currentDate, endDate):
        delta = endDate - currentDate
        return delta.days * self.hoursPerDay




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

    sprint = Sprint()
    sprint.codeFreezeDate = "2013/05/11"
    print sprint.getDevTimeLeftInSprint()

