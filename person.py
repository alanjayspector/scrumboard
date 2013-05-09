__author__ = 'alan'


from card import Card


class PersonError(Exception): pass
class PersonInvalidHour(PersonError) : pass
class PersonInvalidCard(PersonError) : pass
class PersonInvalidCardsParam(PersonError) : pass


class Person(object):
    IDctr = 0

    def __init__(self, params = None):
        self.__personID = Person.getNextID()
        self.isADeveloper = True
        self.firstName = None
        self.lastName = None
        self.avatar = None
        self.currentSprintID = None
        #keys will be sprintIDs, values will be lists of cards
        self.cards = {}
        self.__estimatedSprintHours = 0
        self.__spentSprintHours = 0
        if isinstance(params,dict) :
            for key in params:
                if key != "cards" and hasattr(self,key):
                    setattr(self,key,params[key])


    @staticmethod
    def getNextID():
        Person.IDctr += 1
        return Person.IDctr

    @property
    def personID(self):
        return self.__personID

    @personID.setter
    def personID(self,value):
        return self.__personID
    @property
    def estimatedSprintHours(self):
        return self.__estimatedSprintHours

    @estimatedSprintHours.setter
    def estimatedSprintHours(self,value):
        if not isinstance(value,int) or value <= 0:
            raise PersonInvalidHour, "estimatedSprintHours must be greater than 0"
        self.__estimatedSprintHours = value

    @property
    def spentSprintHours(self):
        return self.__spentSprintHours

    @spentSprintHours.setter
    def spentSprintHours(self,value):
        if not isinstance(value,int) or value <= 0:
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

    def getCurrentRedCards(self,timeLeftInSprint):
        cards = self.cards[self.currentSprintID]
        return [ card for card in cards if card.isCardRed(timeLeftInSprint)]

    def getCurrentGreenCards(self,timeLeftInSprint):
        cards = self.cards[self.currentSprintID]
        return [ card for card in cards if card.isCardGreen(timeLeftInSprint)]

    def getCurrentYellowCards(self, timeLeftInSprint):
        cards = self.cards[self.currentSprintID]
        return [ card for card in cards if card.isCardYellow(timeLeftInSprint)]

    def getVelocityForCurrentSprint(self):
        return self.getVelocityForSprint(self.currentSprintID)

    def getVelocityForSprint(self,sprintID):
        cards = self.cards[sprintID]
        doneStoryPoints = 0
        outstandingStoryPoints = 0

        for card in cards:
            if card.placeOnBoard == "Done":
                doneStoryPoints += card.storyPoints
            else:
                outstandingStoryPoints += cards.storyPoints

        return (doneStoryPoints, outstandingStoryPoints )


    def addCardToCurrentSprint(self,card):
        return self.addCardToSprint(card,self.currentSprintID)

    def addCardToSprint(self,card,sprintID):
        if not isinstance(card, Card ):
            raise PersonInvalidCard, "addCardToCurrentSprint must take a Card instance"
        if not self.cards.has_key(sprintID):
            self.cards[sprintID] = []
        self.cards[sprintID].append(card)

    def getCurrentSprintCards(self):
        return self.cards[self.currentSprintID]

















