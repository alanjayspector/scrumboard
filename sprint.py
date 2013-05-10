__author__ = 'alanspector'

import datetime
from scrumboard import Scrumboard

class InvalidSprintDateFormat(Exception) : pass

class Sprint(object):
    IDctr = 0
    DATE_FORMAT = "%Y/%m/%d"


    def __init__(self, params = None):
        startDate = datetime.datetime.now() + datetime.timedelta(days=1)
        self.__sprintID = Sprint.getNextID()
        self.__startDate = startDate.strftime(Sprint.DATE_FORMAT)
        self.__endDate = (startDate + datetime.timedelta(days=13)).strftime(Sprint.DATE_FORMAT)
        self.hoursPerDay = 4
        self.__codeFreezeDate = (startDate + datetime.timedelta(days=7)).strftime(Sprint.DATE_FORMAT)
        self.__endQADate =  (startDate + datetime.timedelta(days=12)).strftime(Sprint.DATE_FORMAT)
        self.name = None
        self.scrumBoard = Scrumboard(self.sprintID)

    @property
    def startDate(self):
        return self.__startDate

    @startDate.setter
    def startDate(self,value):
        try:
            datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "startDate must be in format:%s" % Sprint.DATE_FORMAT
        else:
            self.__startDate = value


    @property
    def endDate(self):
        return self.__endDate

    @endDate.setter
    def endDate(self,value):
        try:
            datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "endDate must be in format:%s" % Sprint.DATE_FORMAT
        else:
            self.__endDate = value


    @property
    def endQADate(self):
        return self.__endQADate

    @endQADate.setter
    def endQADate(self,value):
        try:
            datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "endQADate must be in format:%s" % Sprint.DATE_FORMAT
        else:
            self.__endQADate = value

    @property
    def codeFreezeDate(self):
        return self.__codeFreezeDate

    @codeFreezeDate.setter
    def codeFreezeDate(self,value):
        try:
            datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "codeFreezeDate must be in format:%s" % Sprint.DATE_FORMAT
        else:
            self.__codeFreezeDate = value

    @property
    def sprintID(self):
        return self.__sprintID

    @sprintID.setter
    def sprintID(self, value):
        return self.__sprintID

    @staticmethod
    def getNextID():
        Sprint.IDctr += 1
        return Sprint.IDctr

    def getDevTimeLeftInSprint(self,dateToCalculateFrom = datetime.datetime.today()):
        codeFreezeDate = datetime.datetime.strptime(self.codeFreezeDate,Sprint.DATE_FORMAT)
        return self.__getTimeLeftInSprint(dateToCalculateFrom,codeFreezeDate)

    def getQATimeLeftInSprint(self,dateToCalculateFrom = datetime.datetime.today()):
        endQADate = datetime.datetime.strptime(self.endQADate,Sprint.DATE_FORMAT)
        return self.__getTimeLeftInSprint(dateToCalculateFrom,endQADate)

    def __getTimeLeftInSprint(self, currentDate, endDate):
        delta = endDate - currentDate
        return delta.days * self.hoursPerDay










