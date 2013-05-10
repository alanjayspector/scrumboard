__author__ = 'alan'


from card import Card
from person import Person
from string import Template
from sprint import Sprint
import copy

class CLI(object):
    createSprintMenuStr = Template("""
Welcome to the Scrumboard Project
---------------------------------
You have the following options:
1) Create a person
2) Create a card
4) Enter Sprint's start date ($startDate)
5) Enter Sprint's end date ($endDate)
6) Enter Sprint's code freeze date ($codeFreezeDate)
7) Enter Sprint's QA's end date ($endQADate)
8) Enter the sprint name ($name)
9) Assign a developer to a card
10) Assign QA to a card
11) Begin Sprint
$message
        """)

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
                    return


        print CLI.createPersonMenuSTR.substitute(self.workingPerson)
        self.workingPerson["message"] = ""


    def createCardMenu(self,option = None):
        pass

    def selectCardToMoveMenu(self, option = None):
        pass

    def assignPersonToCardMenu(self, option = None):
        pass

    def createSprintMenu(self, option = None ):
        workingSprint = { "endDate": self.sprint.endDate, "endQADate": self.sprint.endQADate, \
                          "codeFreezeDate": self.sprint.codeFreezeDate, "startDate": self.sprint.startDate, \
                          "name": self.sprint.name, "message":""
            }
        if not option:
            print CLI.createSprintMenuStr.substitute(workingSprint)
        else:
            if option == 11:
                self.menuStr = "mainMenu"
            elif option == 1:
                self.menuStr = "createPersonMenu"
            elif option == 4:
                pass
            elif option == 5:
                pass
            elif option == 6:
                pass
            elif option == 7:
                pass


    def mainMenu(self, option = None):
        if not option:
            print CLI.mainMenuStr
        else:
            if option == 5:
                self.termination_condition = True
                print "Thank you for trying the Scrumboard Project. exiting...."

if __name__ == "__main__":

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