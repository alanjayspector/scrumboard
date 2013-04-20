__author__ = 'alan'


class Person(object):
    IDctr = 0

    def __init__(self):
        self.personID = Person.getNextID()
        self.firstName = None
        self.lastName = None
        self.avatar = None
        self.currentSprint = None
        self.pastCards = []
        self.currentCards = []
        self.estimatedSprintHours = 0
        self.availableSprintHoursLeft = 0
        self.notes = []

    @staticmethod
    def getNextID():
        Person.IDctr += 1
        return Person.IDctr














