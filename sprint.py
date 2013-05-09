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

    from card import Card
    from person import Person
    from string import Template
    import copy

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

        createPersonMenuSTR = Template("""
Create a Person Menu
--------------------------------
You have the following options:
1) Set First Name ($firstName)
2) Set Last Name ($lastName)
3) Set Estimated Sprint Hours ($estimatedSprintHours)
4) Set Person as a developer ($isADeveloper)
5) Set Person as QA ($isQA)
6) Save and return to Sprint Menu
7) Cancel and return to Sprint Menu
$message
        """)

        defaultWorkingPerson = {"firstName":"unset", "lastName":"unset", \
            "estimatedSprintHours":"unset", "isADeveloper":True,
            "isQA": False, "message": ""
                            }

        def __init__(self):
            self.termination_condition = False
            self.menuStr = "createSprintMenu"
            self.sprint = Sprint()
            self.scrumboard = self.sprint.scrumBoard
            self.option = None
            self.workingPerson = None
            self.workingCard = None


        def createPersonMenu(self, option = None):
            if not option:
                if not self.workingPerson:
                    self.workingPerson = copy.copy(CLI.defaultWorkingPerson)
                    self.workingPerson["currentSprintID"] = self.sprint.sprintID
            else:
                    if option == 1:
                        self.workingPerson["firstName"] = raw_input("Please enter the Person's first name:")
                    elif option == 2:
                        self.workingPerson["lastName"] = raw_input("Please enter the Person's last name:")
                    elif option == 3:
                        try:
                            self.workingPerson["estimatedSprintHours"] \
                                 = int(raw_input("Please enter the Person's estimated sprint hours:"))
                        except:
                            self.workingPerson["message"] = "*****Estimated sprint hours must be a 1 or greater."
                            return
                    elif option == 4:
                        self.workingPerson["isADeveloper"] = True
                        self.workingPerson["isQA"] = False
                    elif option == 5:
                        self.workingPerson["isADeveloper"] = False
                        self.workingPerson["isQA"] = True
                    elif option == 6:
                        try:
                            person = Person(self.workingPerson)
                            self.scrumboard.assignPersonToScrumboard(person)
                            self.workingPerson = None
                            self.menuStr = "createSprintMenu"
                        except:
                            self.workingPerson = copy.copy(CLI.defaultWorkingPerson)
                            self.workingPerson["currentSprintID"] = self.sprint.sprintID
                            self.workingPerson["message"] = "*****There was an error saving your person please try again."
                        return
                    elif option == 7:
                        self.workingPerson = None
                        self.menuStr = "createSprintMenu"


            print CLI.createPersonMenuSTR.substitute(self.workingPerson)
            self.workingPerson["message"] = ""


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
                    self.menuStr = "mainMenu"
                if option == 1:
                    self.menuStr = "createPersonMenu"

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
            menuFunc(cli.option)



