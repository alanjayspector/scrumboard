__author__ = 'alan'

from person import Person
from card import Card


class ScrumboardError(Exception): pass


class PersonNotFoundOnScrumboard(ScrumboardError): pass


class CardNotFoundOnScrumboard(ScrumboardError): pass


class NotValidSprint(ScrumboardError): pass


class NotValidPerson(ScrumboardError): pass


class NotValidCard(ScrumboardError): pass


class Scrumboard(object):
    IDctr = 0

    def __init__(self, sprint=None):
        self.__scrumboardID = Scrumboard.getNextID()
        self.cards = {}
        self.people = {}
        if sprint:
            self.sprint = sprint


    @staticmethod
    def getNextID():
        Scrumboard.IDctr += 1
        return Scrumboard.IDctr

    @property
    def scrumboardID(self):
        return self.__scrumboardID

    @scrumboardID.setter
    def scrumboardID(self, value):
        return self.__scrumboardID


    def reportGreenCards(self, timeLeftInSprint):
        return [card for card in self.cards.values() if card.isCardGreen(timeLeftInSprint)]

    def reportYellowCards(self, timeLeftInSprint):
        return [card for card in self.cards.values() if card.isCardYellow(timeLeftInSprint)]

    def reportRedCards(self, timeLeftInSprint):
        return [card for card in self.cards.values() if card.isCardRed(timeLeftInSprint)]

    def getCardsInPlace(self, place):
        return [card for card in self.cards.values() if card.placeOnBoard == place]

    def getCardsAssignedToPerson(self, personID):
        person = self.getPerson(personID)
        return person.getCurrentSprintCards()

    def getPerson(self, personID):
        if not self.people.has_key(personID):
            raise PersonNotFoundOnScrumboard
        return self.people[personID]

    def getAllPeople(self, isADeveloper=True):
        people = []
        for person in self.people.values():
            if person.isADeveloper == isADeveloper:
                people.append(person)
        return people


    def getCard(self, cardID):
        if not self.cards.has_key(cardID):
            raise CardNotFoundOnScrumboard
        return self.cards[cardID]

    def getTotalStoryPoints(self):
        totalStoryPoints = 0
        for card in self.cards.values():
            totalStoryPoints += card.storyPoints
        return totalStoryPoints

    def getVelocity(self):
        doneStoryPoints = 0
        outstandingStoryPoints = 0
        for card in self.cards.values():
            if card.placeOnBoard == "Done":
                doneStoryPoints += card.storyPoints
            else:
                outstandingStoryPoints += card.storyPoints
        return doneStoryPoints, outstandingStoryPoints, self.getTotalStoryPoints()

    def assignPersonToScrumboard(self, person):
        if not isinstance(person, Person):
            raise NotValidPerson
        self.people[person.personID] = person

    def assignCardToScrumboard(self, card):
        if not isinstance(card, Card):
            raise NotValidCard
        self.cards[card.cardID] = card

    def getTotalEstimatedDevHoursFromPeople(self):
        totalHours = 0
        for person in self.people.values():
            if person.isADeveloper:
                totalHours += person.estimatedSprintHours
        return totalHours

    def getTotalEstimatedQAHoursFromPeople(self):
        totalHours = 0
        for person in self.people.values():
            if not person.isADeveloper:
                totalHours += person.estimatedSprintHours
        return totalHours

    def getTotalEstimatedDevHoursForCards(self):
        totalHours = 0
        for card in self.cards.values():
            totalHours += card.estimatedDevHours
        return totalHours

    def getTotalEstimatedQAHoursForCards(self):
        totalHours = 0
        for card in self.cards.values():
            totalHours += card.estimatedQAHours
        return totalHours

    def getTotalAssigned(self, isADeveloper=True):
        totalHours = 0
        for person in self.people.values():
            if person.isADeveloper == isADeveloper:
                totalHours += person.getAssignedHoursInSprint()
        return totalHours














