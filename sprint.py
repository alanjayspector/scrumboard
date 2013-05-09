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

    class CLI(object):
        createSprintMenuStr = """
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
        mainMenuStr = """
Scrumboard Main Menu
--------------------------------
You have the following options:
1) Iterate a day
2) Status Report
3) Move card on board
4) Add dev hours spent on card
5) End Sprint and Exit the Scrumboard
        """

        def __init__(self):
            self.termination_condition = False
            self.menuStr = "createSprintMenu"
            self.sprint = Sprint()
            self.scrumboard = self.sprint.scrumBoard
            self.option = None


        def createPersonMenu(self, option = None):
            pass

        def createCardMenu(self,option = None):
            pass

        def selectCardToMoveMenu(self, option = None):
            pass

        def assignPersonToCardMenu(self, option = None):
            pass

        def createSprintMenu(self, option = None ):
            if not option:
                print CLI.createSprintMenuStr
            else:
                if option == 7:
                    return "mainMenu"

        def mainMenu(self, option = None):
            if not option:
                print CLI.mainMenuStr
            else:
                if option == 5:
                    self.termination_condition = True
                    print "Thank you for trying the Scrumboard Project. exiting...."

    cli = CLI()
    menuFunc = None

    while not cli.termination_condition:

        menuFunc = getattr(cli,cli.menuStr)
        menuFunc()
        input = raw_input("Please input the number of an option:")
        try:
            cli.option = int(input)
        except ValueError:
            print "{} is not a valid choice.".format(input)
        else:
            print "You selected {}.".format(input)
            cli.menuStr = menuFunc(cli.option)



