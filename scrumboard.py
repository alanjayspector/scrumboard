__author__ = 'alan'


class ScrumBoard(object):
    IDctr = 0

    def __init__(self):
        self.scrumBoardID = ScrumBoard.getNextID()
        self.cards = []
        self.people = []
        self.sprint = None

    @staticmethod
    def getNextID():
        ScrumBoard.IDctr += 1
        return ScrumBoard.IDctr

    def reportGreenCards(self,timeLeftInSprint):
        pass

    def reportYellowCards(self,timeLeftInSprint):
        pass

    def reportRedCards(self,timeLeftInSprint):
        pass



