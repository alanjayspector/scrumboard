__author__ = 'alan'

import card
from card import Card
import scrumboard
from scrumboard import Scrumboard
import sprint
from sprint import Sprint
import person
from person import Person


class ScrumboardError(Exception): pass


class PersonNotFoundOnScrumboard(ScrumboardError): pass


class CardNotFoundOnScrumboard(ScrumboardError): pass


class NotValidSprint(ScrumboardError): pass


class NotValidPerson(ScrumboardError): pass


class NotValidCard(ScrumboardError): pass


class Scrumboard(object):
    IDctr = 0

    def __init__(self, sprint=None):
        self.scrumBoardID = Scrumboard.getNextID()
        self.cards = {}
        self.people = {}
        if not isinstance(sprint, Sprint):
            raise NotValidSprint
        else:
            self.sprint = sprint

    @staticmethod
    def getNextID():
        Scrumboard.IDctr += 1
        return Scrumboard.IDctr

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

    def getCard(self, cardID):
        if not self.cards.has_key(cardID):
            raise CardNotFoundOnScrumboard
        return self.cards[cardID]

    def getTotalStoryPoints(self):
        totalStoryPoints = 0
        for cards in self.cards.values():
            totalStoryPoints += card.storyPoints

    def getVelocity(self):
        doneStoryPoints = 0
        outstandingStoryPoints = 0
        for card in self.cards.values():
            if card.isCardGreen():
                doneStoryPoints += card.storyPoints
            else:
                outstandingStoryPoints += card.storyPoints

        return (doneStoryPoints, outstandingStoryPoints)

    def assignPersonToScrumboard(self, person):
        if not isinstance(person, Person):
            raise NotValidPerson
        self.people[person.personID] = person

    def assignCardToScrumboard(self, card):
        if not isinstance(card, Card):
            raise NotValidCard
        self.cards[card.cardID] = card








