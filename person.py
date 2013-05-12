__author__ = 'alan'

from card import Card
from string import Template


class PersonError(Exception): pass


class PersonInvalidHour(PersonError): pass


class PersonInvalidCard(PersonError): pass


class PersonInvalidCardsParam(PersonError): pass


class Person(object):
    IDctr = 0
    __printTemplate = Template("""
--------------------------------
ID:$personID
$firstName $lastName
Developer: $isADeveloper
$spentSprintHours/$estimatedSprintHours hours
--------------------------------
    """)

    def __init__(self, params=None):
        self.__personID = Person.getNextID()
        self.isADeveloper = True
        self.firstName = None
        self.lastName = None
        self.avatar = None
        self.currentSprintID = "currentSprint"
        #keys will be sprintIDs, values will be lists of cards
        self.cards = {}
        self.__estimatedSprintHours = 0
        self.__spentSprintHours = 0
        if isinstance(params, dict):
            for key in params:
                if key != "cards" and hasattr(self, key):
                    setattr(self, key, params[key])


    def __str__(self):
        personInfo = {"personID": self.personID, "firstName": self.firstName, \
                      "lastName": self.lastName, "isADeveloper": self.isADeveloper, \
                      "spentSprintHours": self.spentSprintHours, "estimatedSprintHours": self.estimatedSprintHours
        }
        return Person.__printTemplate.substitute(personInfo)

    @staticmethod
    def getNextID():
        Person.IDctr += 1
        return Person.IDctr

    @property
    def personID(self):
        return self.__personID

    @personID.setter
    def personID(self, value):
        return self.__personID

    @property
    def estimatedSprintHours(self):
        return self.__estimatedSprintHours

    @estimatedSprintHours.setter
    def estimatedSprintHours(self, value):
        if not isinstance(value, int) or value <= 0:
            raise PersonInvalidHour, "estimatedSprintHours must be greater than 0"
        self.__estimatedSprintHours = value

    @property
    def fullName(self):
        return "{} {}".format(self.firstName, self.lastName)

    @fullName.setter
    def fullName(self, value):
        return "{} {}".format(self.firstName, self.lastName)

    @property
    def spentSprintHours(self):
        return self.__spentSprintHours

    @spentSprintHours.setter
    def spentSprintHours(self, value):
        if not isinstance(value, int) or value <= 0:
            raise PersonInvalidHour, "spentSprintHours must be greater than 0"

        self.__spentSprintHours = value

    def getUnallocatedHoursInSprint(self):
        totalEstimatedHours = self.getAllocatedHoursInSprint()
        return self.estimatedSprintHours - totalEstimatedHours

    def getAllocatedHoursInSprint(self):
        cards = self.cards[self.currentSprintID]
        totalEstimatedHours = 0
        if self.isADeveloper:
            for card in cards:
                totalEstimatedHours += card.estimatedDevHours
        else:
            for card in cards:
                totalEstimatedHours += card.estimatedQAHours

        return totalEstimatedHours

    def getCurrentRedCards(self, timeLeftInSprint):
        cards = self.cards[self.currentSprintID]
        return [card for card in cards if card.isCardRed(timeLeftInSprint)]

    def getCurrentGreenCards(self, timeLeftInSprint):
        cards = self.cards[self.currentSprintID]
        return [card for card in cards if card.isCardGreen(timeLeftInSprint)]

    def getCurrentYellowCards(self, timeLeftInSprint):
        cards = self.cards[self.currentSprintID]
        return [card for card in cards if card.isCardYellow(timeLeftInSprint)]

    def getVelocityForCurrentSprint(self):
        return self.getVelocityForSprint(self.currentSprintID)

    def getVelocityForSprint(self, sprintID):
        cards = self.cards[sprintID]
        doneStoryPoints = 0
        outstandingStoryPoints = 0
        totalStoryPoints = 0

        for card in cards:
            totalStoryPoints += card.storyPoints
            if card.placeOnBoard == "Done":
                doneStoryPoints += card.storyPoints
            else:
                outstandingStoryPoints += card.storyPoints

        return (doneStoryPoints, outstandingStoryPoints, totalStoryPoints )


    def assignCardToSelf(self, card):
        if not isinstance(card, Card):
            raise PersonInvalidCard, "addCardToCurrentSprint must take a Card instance"
        if not self.cards.has_key(self.currentSprintID):
            self.cards[self.currentSprintID] = []
        self.cards[self.currentSprintID].append(card)
        if self.isADeveloper:
            card.developer = self
        else:
            card.qa = self

    def getCurrentSprintCards(self):
        return self.cards[self.currentSprintID]

















