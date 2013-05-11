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
9) Begin Sprint
$message""")

    mainMenuStr = """
Scrumboard Main Menu
--------------------------------
You have the following options:
1) Iterate a day
2) Status Report
3) Move card on board
4) Add dev hours spent on card
5) Assign developer to a card
6) Assign QA to a card
7) End Sprint and Exit the Scrumboard"""

    createPersonMenuStr = Template("""
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


    createCardMenuStr = Template("""
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

    __statusReportMenuStr = """
Status Report Menu
--------------------------------
1) Show Red Cards
2) Show Yellow Cards
3) Show Green Cards
4) Show Current Velocity
5) Show All Cards
6) Main Menu"""

    __cardStatusTemplate = Template("""
--------------------------------
    description:$description
    status:$status story points:$storyPoints
developer:$developer estimated hours:$estimatedDevHours spent hours:$spentDevHours
qa:$qa  estimated hours:$estimatedQAHours
    place on board:$placeOnBoard""")

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

        print CLI.createCardMenuStr.substitute(self.workingCard)
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


        print CLI.createPersonMenuStr.substitute(self.workingPerson)
        self.workingPerson["message"] = ""

    def statusReportMenu(self, option = None ):
        if option:
            if option == 1:
                self.generateCardStatuses("reportRedCards")
        else:
            print CLI.__statusReportMenuStr

    def generateCardStatuses(self, cardColor = "reportRedCards"):
        scrumboardMethod = getattr(self.scrumboard, cardColor)
        if callable(scrumboardMethod):
            for card in scrumboardMethod(self.sprint.getDevTimeLeftInSprint()):
                cardInfo = { "storyPoints":card.storyPoints, "description":card.description, \
                             "estimatedDevHours":card.estimatedDevHours, "estimatedQAHours":card.estimatedQAHours, \
                            "qa":"{} {}".format(card.qa.firstName, card.qa.lastName), \
                            "developer":"{} {}".format(card.developer.firstName,card.developer.lastName), \
                            "placeOnBoard" : card.placeOnBoard, "status":card.status
                }
                print CLI.__cardStatusTemplate.substitute(cardInfo)



    def selectCardToMoveMenu(self, option = None):
        pass

    def assignPersonToCardMenu(self, option = None):
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

        print CLI.createSprintMenuStr.substitute(self.workingSprint)
        self.workingSprint["message"] = ""


    def mainMenu(self, option = None):
        if not option:
            print CLI.mainMenuStr
        else:
            if option == 7:
                self.termination_condition = True
                print "Thank you for trying the Scrumboard Project. exiting...."
            if option == 2:
                self.menuStr = "statusReportMenu"

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