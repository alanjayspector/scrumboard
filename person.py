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
        pass

    def getAllocatedHoursInSprint(self):
        pass

    def getCurrentRedCards(self,timeLeftInSprint):
        pass

    def getCurrentGreenCards(self,timeLeftInSprint):
        pass

    def getCurrentYellowCards(self, timeLeftInSprint):
        pass

    def getVelocityForCurrentSprint(self):
        pass

    def getVelocityForPastSprint(self,sprintID):
        pass


















