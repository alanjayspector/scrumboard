__author__ = 'alan'


class ScrumBoard(object):
    IDctr = 0

    def __init__(self):
        self.scrumBoardID = ScrumBoard.getNextID()
        self.cards = []
        self.people = []
        self.sprintID = None

    @staticmethod
    def getNextID():
        ScrumBoard.IDctr += 1
        return ScrumBoard.IDctr

    def reportGreenCards(self,timeLeftInSprint):
        return [ card for card in self.cards if card.isCardGreen(timeLeftInSprint) ]

    def reportYellowCards(self,timeLeftInSprint):
        return [ card for card in self.cards if card.isCardYellow(timeLeftInSprint) ]

    def reportRedCards(self,timeLeftInSprint):
        return [ card for card in self.cards if card.isCardRed(timeLeftInSprint) ]

    def getCardsInPlace(self,place):
        pass

    def getCardsAssignedToPerson(self,personID):
        pass

    def getPerson(self,personID):
        pass

    def getCard(self,cardID):
        pass

    def getTotalStoryPoints(self):
        pass

    def getVelocity(self):
        pass









