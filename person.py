__author__ = 'alan'


class Person(object):
    IDctr = 0

    def __init__(self):
        self.personID = Person.getNextID()
        self.isADeveloper = True
        self.firstName = None
        self.lastName = None
        self.avatar = None
        self.currentSprintID = None
        #keys will be sprintIDs, values will be lists of cards
        self.cards = {}
        self.estimatedSprintHours = 0
        self.spentSprintHours = 0

    @staticmethod
    def getNextID():
        Person.IDctr += 1
        return Person.IDctr

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


















