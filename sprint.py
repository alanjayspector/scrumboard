__author__ = 'alanspector'

import datetime
from scrumboard import Scrumboard

class InvalidSprintDateFormat(Exception) : pass

class Sprint(object):
    IDctr = 0
    DATE_FORMAT = "%Y/%m/%d"


    def __init__(self, params = None):
        self.__sprintID = Sprint.getNextID()
        self.__startDate = None
        self.__endDate = None
        self.hoursPerDay = 4
        self.__codeFreezeDate = None
        self.__endQADate = None
        self.name = None
        self.team = None
        self.scrumBoard = Scrumboard(self.sprintID)

    @property
    def startDate(self):
        return self.__startDate

    @startDate.setter
    def startDate(self,value):
        try:
            datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "startDate must be in format:%s" % Sprint.DATE_FORMAT
        else:
            self.__startDate = value


    @property
    def endDate(self):
        return self.__endDate

    @endDate.setter
    def endDate(self,value):
        try:
            datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "endDate must be in format:%s" % Sprint.DATE_FORMAT
        else:
            self.__endDate = value


    @property
    def endQADate(self):
        return self.__endQADate

    @endQADate.setter
    def endQADate(self,value):
        try:
            datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "endQADate must be in format:%s" % Sprint.DATE_FORMAT
        else:
            self.__endQADate = value

    @property
    def codeFreezeDate(self):
        return self.__codeFreezeDate

    @codeFreezeDate.setter
    def codeFreezeDate(self,value):
        try:
            datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "codeFreezeDate must be in format:%s" % Sprint.DATE_FORMAT
        else:
            self.__codeFreezeDate = value

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
        return self.__getTimeLeftInSprint(dateToCalculateFrom,codeFreezeDate)

    def getQATimeLeftInSprint(self,dateToCalculateFrom = datetime.datetime.today()):
        endQADate = datetime.datetime.strptime(self.endQADate,Sprint.DATE_FORMAT)
        return self.__getTimeLeftInSprint(dateToCalculateFrom,endQADate)

    def __getTimeLeftInSprint(self, currentDate, endDate):
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



    def createSprintMenu():
        print """
Welcome to the Scrumboard Project
---------------------------------
You have the following options:
1) Create a person
2) Create a card
3) Enter the team name
4) Enter the sprint name
5) Assign a developer to a card
6) Assign QA to a card
7) Exit to main Menu
        """

    def mainMenu():
        print """
Scrumboard Main Menu
--------------------------------
You have the following options:
1) Iterate a day
2) Status Report
3) Move card on board
4) End Sprint and Exit the Scrumboard
            """


    sprint = Sprint()
    scrumboard = sprint.scrumBoard

    createSprintMenu()

    option = None
    while not termination_condition:
        input = raw_input("Please input the number of an option:")
        try:
            option = int(input)
        except ValueError:
            print "{} is not a valid choice.".format(input)
        else:
            print "You selected {}.".format(input)



