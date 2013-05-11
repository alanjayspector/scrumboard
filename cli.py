__author__ = 'alan'


from card import Card
from person import Person
from string import Template
from sprint import Sprint
import datetime
import copy

class CLI(object):
    __createSprintMenuStr = Template("""
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
9) Begin Sprint
$message""")

    __moveCardOnBoardMenu = Template("""
Move a Card on the Board Menu
---------------------------------
Card Selected:$cardSelected
1) Select a card
2) Move card to Backlog
3) Move card to Research
4) Move card to Development
5) Move card to Code Review
6) Move card to PO Review
7) Move card to QA
8) Move card to Done
9) Back to Main Menu
$message""")

    __assignPersonToCardMenu = Template("""
Assign a Person to a Card
---------------------------------
Card Selected:$cardSelected
1) Select a card
2) Assign QA
3) Assign a Developer
4) Back to Main Menu
$message""")

    __updateSpentDevHoursMenu = Template("""
Update spent dev hours on Card Menu
---------------------------------
Card Selected:$cardSelected
1) Select a card
2) Add spent dev hours ($spentDevHours)
3) Back to Main Menu
    """)

    __mainMenuStr = Template("""
Scrumboard Main Menu
--------------------------------
Current Sprint Date:$currentDate
You have the following options:
1) Iterate a day
2) Status Report
3) Move card on board
4) Add dev hours spent on card
5) Assign person to a card
6) End Sprint and Exit the Scrumboard""")

    __createPersonMenuStr = Template("""
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
$message""")


    __createCardMenuStr = Template("""
Create a Card Menu
--------------------------------
You have the following options:
1) Set Description ($description)
2) Set Story Points ($storyPoints)
3) Set Estimated Dev Hours ($estimatedDevHours)
4) Set Estimated QA Hours ($estimatedQAHours)
5) Toggle Code Review Required ($needsCodeReview)
6) Toggle PO Review Required ($needsPOReview)
7) Save and return to Sprint Menu
8) Cancel and return to Sprint Menu
$message""")

    __statusReportMenuStr = Template("""
Status Report Menu
--------------------------------
$completedPoints/$totalPoints completed SP
1) Show Red Cards
2) Show Yellow Cards
3) Show Green Cards
4) Show All Cards
5) Main Menu""")


    defaultWorkingPerson = {"firstName":"unset", "lastName":"unset", \
            "estimatedSprintHours":"unset", "isADeveloper":True,
            "isQA": False, "message": ""
                            }
    defaultWorkingCard = {"description":"unset", "storyPoints":"unset", \
                          "estimatedDevHours":"unset", "estimatedQAHours":"unset", \
                          "needsCodeReview":True, "needsPOReview":True, "message":""
                          }

    def __init__(self):
        self.termination_condition = False
        self.menuStr = "createSprintMenu"
        self.sprint = Sprint()
        self.scrumboard = self.sprint.scrumBoard
        self.option = None
        self.workingSprint = None
        self.workingPerson = None
        self.workingCard = None
        self.selectedCard = None
        self.currentDate= self.sprint.startDate

    def iterateDay(self):
            currentDate = datetime.datetime.strptime(self.currentDate,Sprint.DATE_FORMAT)
            self.currentDate = (currentDate + datetime.timedelta(days=1)).strftime(Sprint.DATE_FORMAT)

    def createCardMenu(self, option = None):
        if not option:
            if not self.workingCard:
                self.workingCard= copy.copy(CLI.defaultWorkingCard)
        else:
                if option == 1:
                    self.workingCard["description"] = raw_input("Please enter the card's description:")
                elif option == 2:
                    print
                    try:
                        self.workingCard["storyPoints"] \
                            = int(raw_input("Please enter story points({}):".format(\
                            ",".join([str(points) for points in Card.cardDataMap["storyPoints"]]))))
                    except:
                        self.workingCard["message"] = "*****Invalid story points"
                    return
                elif option == 3:
                    try:
                        self.workingCard["estimatedDevHours"] \
                             = int(raw_input("Please enter the card's estimated dev hours:"))
                    except:
                        self.workingCard["message"] = "*****Estimated dev hours must be a 1 or greater."
                    return
                elif option == 4:
                    try:
                        self.workingCard["estimatedQAHours"] \
                             = int(raw_input("Please enter the card's estimated QA hours:"))
                    except:
                        self.workingCard["message"] = "*****Estimated QA hours must be a 1 or greater."
                    return
                elif option == 5:
                    self.workingCard["needsCodeReview"] = not self.workingCard["needsCodeReview"]
                elif option == 6:
                    self.workingCard["needsPOReview"] = not self.workingCard["needsPOReview"]
                elif option == 7:
                    try:
                        card = Card(self.workingCard)
                        self.scrumboard.assignCardToScrumboard(card)
                        self.workingCard = None
                        self.menuStr = "createSprintMenu"
                    except:
                        self.workingCard = copy.copy(CLI.defaultWorkingCard)
                        self.workingCard["message"] = "*****There was an error saving your card please try again."
                    return
                elif option == 8:
                    self.workingCard = None
                    self.menuStr = "createSprintMenu"
                    return

        print CLI.__createCardMenuStr.substitute(self.workingCard)
        self.workingCard["message"] = ""

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


        print CLI.__createPersonMenuStr.substitute(self.workingPerson)
        self.workingPerson["message"] = ""

    def statusReportMenu(self, option = None ):
        if option:
            if option == 1:
                self.generateCardStatuses("reportRedCards")
            elif option == 2:
                self.generateCardStatuses("reportYellowCards")
            elif option == 3:
                self.generateCardStatuses("reportGreenCards")
            elif option == 4:
                for card in self.scrumboard.cards.values():
                    print card
                    raw_input("Press any key to continue:")
            elif option == 5:
                self.menuStr = "mainMenu"
        else:
            completed, outstanding, total = self.scrumboard.getVelocity(self.sprint.getDevTimeLeftInSprint(self.currentDate))
            print CLI.__statusReportMenuStr.substitute({"completedPoints":completed, "totalPoints":total})

    def generateCardStatuses(self, cardColor = "reportRedCards"):
        scrumboardMethod = getattr(self.scrumboard, cardColor)
        if callable(scrumboardMethod):
            for card in scrumboardMethod(self.sprint.getDevTimeLeftInSprint(self.currentDate)):
                print card
                raw_input("Press any key to continue:")

    def moveCardOnBoardMenu(self, option = None):
        pass

    def assignPersonToCardMenu(self, option = None):
        pass

    def addSpentDevHoursToCardMenu(self, option = None):
        pass

    def createSprintMenu(self, option = None ):
        if not self.workingSprint:
            self.workingSprint = { "endDate": self.sprint.endDate, "endQADate": self.sprint.endQADate, \
                          "codeFreezeDate": self.sprint.codeFreezeDate, "startDate": self.sprint.startDate, \
                          "name": self.sprint.name, "message":""
            }
        if option:
            if option == 9:
                self.menuStr = "mainMenu"
            elif option == 1:
                self.menuStr = "createPersonMenu"
            elif option == 4:
                try:
                    self.sprint.startDate = raw_input("Please enter start date in format YYYY/MM/DD:")
                    self.workingSprint["startDate"] = self.sprint.startDate
                    self.currentDate = self.sprint.startDate
                except:
                    self.workingSprint["message"] = "*****Invalid date"
                return
            elif option == 5:
                try:
                    self.sprint.endDate = raw_input("Please enter end date in format YYYY/MM/DD:")
                    self.workingSprint["endDate"] = self.sprint.endDate
                except:
                    self.workingSprint["message"] = "*****Invalid date"
                return
            elif option == 6:
                try:
                    self.sprint.codeFreezeDate = raw_input("Please enter code freeze date in format YYYY/MM/DD:")
                    self.workingSprint["codeFreezeDate"] = self.sprint.codeFreezeDate
                except:
                    self.workingSprint["message"] = "*****Invalid date"
                return
            elif option == 7:
                try:
                    self.sprint.endQADate = raw_input("Please enter QA's end date in format YYYY/MM/DD:")
                    self.workingSprint["endQADate"] = self.sprint.endQADate
                except:
                    self.workingSprint["message"] = "*****Invalid date"
                return
            elif option == 8:
                self.sprint.name = raw_input("Please enter the name for this sprint:")
                self.workingSprint["name"] = self.sprint.name
            elif option == 2:
                self.menuStr ="createCardMenu"

        print CLI.__createSprintMenuStr.substitute(self.workingSprint)
        self.workingSprint["message"] = ""


    def mainMenu(self, option = None):
        if not option:
            print CLI.__mainMenuStr.substitute({"currentDate":self.currentDate})
        else:
            if option == 6:
                self.termination_condition = True
                print "Thank you for trying the Scrumboard Project. exiting...."
            elif option == 2:
                self.menuStr = "statusReportMenu"
            elif option == 3:
                self.menuStr = "moveCardOnBoardMenu"
            elif option == 5:
                self.menuStr = "assignCardToPersonMenu"
            elif option == 4:
                self.menuStr = "addSpentDevHoursToCardMenu"
            elif option == 1:
                self.iterateDay()





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