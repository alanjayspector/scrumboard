__author__ = 'alan'

from card import Card
from person import Person
from string import Template
from sprint import Sprint
import datetime
import copy


def generateSprintDates():
    startDate = datetime.datetime.now()
    endDate = startDate + datetime.timedelta(days=13)
    codeFreezeDate = startDate + datetime.timedelta(days=7)
    endQADate = startDate + datetime.timedelta(days=12)
    return {
        "startDate": startDate.strftime(Sprint.DATE_FORMAT),
        "endDate": endDate.strftime(Sprint.DATE_FORMAT),
        "codeFreezeDate": codeFreezeDate.strftime(Sprint.DATE_FORMAT),
        "endQADate": endQADate.strftime(Sprint.DATE_FORMAT)
    }


class CLI(object):
    __createSprintMenuStr = Template("""
Welcome to the Scrumboard Project
---------------------------------
You have the following options:
1) Create a person
2) Create a card
4) Set Sprint's start date ($startDate)
5) Set Sprint's end date ($endDate)
6) Set Sprint's code freeze date ($codeFreezeDate)
7) Set Sprint's QA's end date ($endQADate)
8) Set Sprint's name ($name)
9) Set Hours/Day in Sprint ($hoursPerDay)
10) Begin Sprint
$message""")

    __moveCardOnBoardMenuStr = Template("""
Move a Card on the Board Menu
---------------------------------
Card Selected:$selectedCard
Card Location:$placeOnBoard
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

    __assignPersonToCardMenuStr = Template("""
Assign a Person to a Card
---------------------------------
Card Selected:$selectedCard
1) Select a card
2) Assign QA ($qa)
3) Assign a Developer ($developer)
4) Back to Main Menu
$message""")

    __updateSpentDevHoursMenuStr = Template("""
Update spent dev hours on Card Menu
---------------------------------
Card Selected:$selectedCard
1) Select a card
2) Add spent dev hours ($spentDevHours)
3) Back to Main Menu
$message""")

    __mainMenuStr = Template("""
Scrumboard Main Menu
--------------------------------
Current Sprint Date:$currentDate
Sprint Completed: $isSprintOver
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

    defaultWorkingPerson = {"firstName": "unset", "lastName": "unset", \
                            "estimatedSprintHours": "unset", "isADeveloper": True,
                            "isQA": False, "message": ""
    }
    defaultWorkingCard = {"description": "unset", "storyPoints": "unset", \
                          "estimatedDevHours": "unset", "estimatedQAHours": "unset", \
                          "needsCodeReview": True, "needsPOReview": True, "message": ""
    }

    def __init__(self):
        self.termination_condition = False
        self.menuStr = "createSprintMenu"
        self.menuBuffer = None
        self.sprint = Sprint(generateSprintDates())
        self.scrumboard = self.sprint.scrumBoard
        self.option = None
        self.workingSprint = None
        self.workingPerson = None
        self.workingCard = None
        self.selectedCard = None
        self.currentDate = self.sprint.startDate
        self.isSprintOver = False

    def iterateDay(self):
        if self.isSprintOver:
            return
        currentDate = datetime.datetime.strptime(self.currentDate, Sprint.DATE_FORMAT)
        newDate = (currentDate + datetime.timedelta(days=1)).strftime(Sprint.DATE_FORMAT)
        endDate = datetime.datetime.strptime(self.sprint.endDate, Sprint.DATE_FORMAT)
        if endDate <= newDate:
            self.isSprintOver = True
            self.currentDate = self.sprint.endDate
            return
        else:
            self.currentDate = (currentDate + datetime.timedelta(days=1)).strftime(Sprint.DATE_FORMAT)

    def createCardMenu(self, option=None):
        if not option:
            if not self.workingCard:
                self.workingCard = copy.copy(CLI.defaultWorkingCard)
        else:
            if option == 1:
                self.workingCard["description"] = raw_input("Please enter the card's description:")
            elif option == 2:
                print
                try:
                    self.workingCard["storyPoints"] \
                        = int(raw_input("Please enter story points({}):".format( \
                        ",".join([str(points) for points in Card.cardDataMap["storyPoints"]]))))
                except Exception as message:
                    self.workingCard["message"] = "*****{}".format(message)
                return
            elif option == 3:
                try:
                    self.workingCard["estimatedDevHours"] \
                        = int(raw_input("Please enter the card's estimated dev hours:"))
                except Exception as message:
                    self.workingCard["message"] = "*****{}".format(message)
                return
            elif option == 4:
                try:
                    self.workingCard["estimatedQAHours"] \
                        = int(raw_input("Please enter the card's estimated QA hours:"))
                except Exception as message:
                    self.workingCard["message"] = "*****{}".format(message)
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
                except Exception as message:
                    self.workingCard = copy.copy(CLI.defaultWorkingCard)
                    self.workingCard["message"] = "*****{}".format(message)
                return
            elif option == 8:
                self.workingCard = None
                self.menuStr = "createSprintMenu"
                return

        print CLI.__createCardMenuStr.substitute(self.workingCard)
        self.workingCard["message"] = ""

    def createPersonMenu(self, option=None):
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
                except Exception as message:
                    self.workingPerson["message"] = "*****{}".format(message)
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
                except Exception as message:
                    self.workingPerson = copy.copy(CLI.defaultWorkingPerson)
                    self.workingPerson["currentSprintID"] = self.sprint.sprintID
                    self.workingPerson["message"] = "*****{}".format(message)
                return
            elif option == 7:
                self.workingPerson = None
                self.menuStr = "createSprintMenu"
                return

        print CLI.__createPersonMenuStr.substitute(self.workingPerson)
        self.workingPerson["message"] = ""

    def statusReportMenu(self, option=None):
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
                return
        else:
            completed, outstanding, total = self.scrumboard.getVelocity()
            print CLI.__statusReportMenuStr.substitute({"completedPoints": completed, "totalPoints": total})

    def generateCardStatuses(self, cardColor="reportRedCards"):
        scrumboardMethod = getattr(self.scrumboard, cardColor)
        if callable(scrumboardMethod):
            for card in scrumboardMethod(self.sprint.getDevTimeLeftInSprint(self.currentDate)):
                print card
                raw_input("Press any key to continue:")

    def selectACard(self):
        selectCard = None
        for card in self.scrumboard.cards.values():
            print card
            selectCard = raw_input('Enter "Y" to select this card or hit any key to continue:').lower()
            if selectCard == "y":
                self.selectedCard = card
                return


    def selectAPersonForSelectedCard(self, isADeveloper=True):
        selectPerson = None
        for person in self.scrumboard.getAllPeople(isADeveloper):
            print person
            selectPerson = raw_input('Enter "Y" to select this person or hit any key to continue:').lower()
            if selectPerson == "y":
                person.assignCardToSelf(self.selectedCard)
                allocated_hours = person.getAssignedHoursInSprint()
                if person.estimatedSprintHours < allocated_hours:
                    difference = allocated_hours - person.estimatedSprintHours
                    self.menuBuffer["message"] = "*****Warning selecting {} will exceed {} hours by {} hour(s)" \
                        .format(person.fullName, person.estimatedSprintHours, difference)
                return person

    def moveCard(self, placeOnBoard):
        message = None
        try:
            self.selectedCard.placeOnBoard = placeOnBoard
        except Exception as error:
            message = error

        return message

    def moveCardOnBoardMenu(self, option=None):
        message = None
        if not self.menuBuffer:
            self.menuBuffer = {"selectedCard": "unset", "message": "", "placeOnBoard": "unset"}
        if self.selectedCard:
            self.menuBuffer["selectedCard"] = self.selectedCard.description
            self.menuBuffer["placeOnBoard"] = self.selectedCard.placeOnBoard
        if option:
            if option == 1:
                self.selectACard()
                if self.selectedCard:
                    self.menuBuffer["selectedCard"] = self.selectedCard.description
                    self.menuBuffer["placeOnBoard"] = self.selectedCard.placeOnBoard
            elif option >= 2 and option <= 8 and not self.selectedCard:
                message = "*****Please select a card first."
            elif option == 2:
                message = self.moveCard("Backlog")
            elif option == 3:
                message = self.moveCard("Research")
            elif option == 4:
                message = self.moveCard("Development")
            elif option == 5:
                message = self.moveCard("PO Review")
            elif option == 6:
                message = self.moveCard("Code Review")
            elif option == 7:
                message = self.moveCard("QA")
            elif option == 8:
                message = self.moveCard("Done")
            elif option == 9:
                self.menuStr = "mainMenu"

            if message:
                self.menuBuffer["message"] = message
            else:
                self.menuBuffer["placeOnBoard"] = self.selectedCard.placeOnBoard
            return

        print CLI.__moveCardOnBoardMenuStr.substitute(self.menuBuffer)

    def addSpentDevHoursToCardMenu(self, option=None):
        if not self.menuBuffer:
            self.menuBuffer = {"selectedCard": "unset", "message": "", "spentDevHours": "unset"}
        if self.selectedCard:
            self.menuBuffer["selectedCard"] = self.selectedCard.description
            self.menuBuffer["spentDevHours"] = self.selectedCard.spentDevHours
        if option:
            if option == 1:
                self.selectACard()
                if self.selectedCard:
                    self.menuBuffer["selectedCard"] = self.selectedCard.description
            elif option == 2 and not self.selectedCard:
                self.menuBuffer["message"] = "*****Please select a card first."
            elif option == 2:
                try:
                    self.selectedCard.spentDevHours += int(raw_input("Please enter a positive whole number:"))
                    self.menuBuffer["spentDevHours"] = self.selectedCard.spentDevHours
                except Exception as message:
                    self.menuBuffer["message"] = message
            elif option == 3:
                self.menuStr = "mainMenu"
            return

        print CLI.__updateSpentDevHoursMenuStr.substitute(self.menuBuffer)

    def assignPersonToCardMenu(self, option=None):
        if not self.menuBuffer:
            self.menuBuffer = {"selectedCard": "unset", "message": "", "qa": "unset", "developer": "unset"}
        if self.selectedCard:
            qa = "unset"
            developer = "unset"

            if self.selectedCard.qa:
                qa = self.selectedCard.qa.fullName
            if self.selectedCard.developer:
                developer = self.selectedCard.developer.fullName
                self.menuBuffer = {"selectedCard": self.selectedCard.description, "qa": qa, "developer": developer,
                                   "message": ""}
        if option:
            if option == 1:
                self.selectACard()
            elif (option == 2 or option == 3) and not self.selectedCard:
                self.menuBuffer["message"] = "*****Please select a card first."
            elif option == 2:
                person = self.selectAPersonForSelectedCard(False)
                self.menuBuffer["qa"] = person.fullName
            elif option == 3:
                person = self.selectAPersonForSelectedCard()
                self.menuBuffer["developer"] = person.fullName
            elif option == 4:
                self.menuStr = "mainMenu"
            return

        print CLI.__assignPersonToCardMenuStr.substitute(self.menuBuffer)


    def createSprintMenu(self, option=None):
        if not self.workingSprint:
            self.workingSprint = {"endDate": self.sprint.endDate, "endQADate": self.sprint.endQADate, \
                                  "codeFreezeDate": self.sprint.codeFreezeDate, "startDate": self.sprint.startDate, \
                                  "name": self.sprint.name, "message": "", "hoursPerDay": self.sprint.hoursPerDay
            }
        if option:
            if option == 10:
                self.menuStr = "mainMenu"
                return
            elif option == 9:
                try:
                    self.sprint.hoursPerDay = int(raw_input("Please enter a positive whole number between 1 and 24:"))
                    self.workingSprint["hoursPerDay"] = self.sprint.hoursPerDay
                except Exception as message:
                    self.workingSprint["message"] = message
            elif option == 1:
                self.menuStr = "createPersonMenu"
                return
            elif option == 4:
                try:
                    self.sprint.startDate = raw_input("Please enter start date in format YYYY/MM/DD:")
                    self.workingSprint["startDate"] = self.sprint.startDate
                    self.currentDate = self.sprint.startDate
                except Exception as message:
                    self.workingSprint["message"] = "*****{}".format(message)
                return
            elif option == 5:
                try:
                    self.sprint.endDate = raw_input("Please enter end date in format YYYY/MM/DD:")
                    self.workingSprint["endDate"] = self.sprint.endDate
                except Exception as message:
                    self.workingSprint["message"] = "*****{}".format(message)
                return
            elif option == 6:
                try:
                    self.sprint.codeFreezeDate = raw_input("Please enter code freeze date in format YYYY/MM/DD:")
                    self.workingSprint["codeFreezeDate"] = self.sprint.codeFreezeDate
                except Exception as message:
                    self.workingSprint["message"] = "*****{}".format(message)
                return
            elif option == 7:
                try:
                    self.sprint.endQADate = raw_input("Please enter QA's end date in format YYYY/MM/DD:")
                    self.workingSprint["endQADate"] = self.sprint.endQADate
                except Exception as message:
                    self.workingSprint["message"] = "*****{}".format(message)
                return
            elif option == 8:
                self.sprint.name = raw_input("Please enter the name for this sprint:")
                self.workingSprint["name"] = self.sprint.name
            elif option == 2:
                self.menuStr = "createCardMenu"
                return

        print CLI.__createSprintMenuStr.substitute(self.workingSprint)
        self.workingSprint["message"] = ""


    def mainMenu(self, option=None):
        if not option:
            print CLI.__mainMenuStr.substitute({"currentDate": self.currentDate, "isSprintOver": self.isSprintOver})
        else:
            if option == 6:
                self.termination_condition = True
                print "Thank you for trying the Scrumboard Project. exiting...."
            elif option == 2:
                self.menuStr = "statusReportMenu"
            elif option == 3:
                self.menuStr = "moveCardOnBoardMenu"
            elif option == 5:
                self.menuStr = "assignPersonToCardMenu"
            elif option == 4:
                self.menuStr = "addSpentDevHoursToCardMenu"
            elif option == 1:
                self.iterateDay()


if __name__ == "__main__":

    cli = CLI()
    menuFunc = None

    while not cli.termination_condition:

        menuFunc = getattr(cli, cli.menuStr)
        menuFunc()
        cli.menuBuffer = None
        input = raw_input("Please input the number of an option:")
        try:
            cli.option = int(input)
        except ValueError:
            print "{} is not a valid choice.".format(input)
        else:
            print "You selected {}.".format(input)
            menuFunc(cli.option)