__author__ = 'alanspector'

import datetime
from scrumboard import Scrumboard

class SprintException(Exception) : pass
class InvalidSprintDateFormat(SprintException) : pass
class InvalidSprintDate(SprintException) : pass

class Sprint(object):
    IDctr = 0
    DATE_FORMAT = "%Y/%m/%d"


    def __init__(self, params = None):
        startDate = datetime.datetime.now()
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
        newDate = None
        try:
            newDate = datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "startDate must be in format:%s" % Sprint.DATE_FORMAT

        codeFreezeDate = datetime.datetime.strptime(self.codeFreezeDate,Sprint.DATE_FORMAT)
        endDate = datetime.datetime.strptime(self.endDate,Sprint.DATE_FORMAT)
        endQADate = datetime.datetime.strptime(self.endQADate,Sprint.DATE_FORMAT)

        if newDate >= codeFreezeDate:
            raise InvalidSprintDate, "{} is greater than or equal to code freeze of {}".format(value,self.codeFreezeDate)
        elif newDate >= endDate:
            raise InvalidSprintDate, "{} is greater than or equal to end date of {}".format(value,self.endDate)
        elif newDate >= endQADate:
            raise InvalidSprintDate, "{} is greater than or equal to end QA date of {}".format(value,self.endQADate)
        else:
            self.__startDate = value


    @property
    def endDate(self):
        return self.__endDate

    @endDate.setter
    def endDate(self,value):
        newDate = None
        try:
            newDate = datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "endDate must be in format:%s" % Sprint.DATE_FORMAT

        codeFreezeDate = datetime.datetime.strptime(self.codeFreezeDate,Sprint.DATE_FORMAT)
        startDate = datetime.datetime.strptime(self.startDate,Sprint.DATE_FORMAT)
        endQADate = datetime.datetime.strptime(self.endQADate,Sprint.DATE_FORMAT)

        if newDate <= codeFreezeDate:
            raise InvalidSprintDate, "{} is less than than or equal to code freeze of {}".format(value,self.codeFreezeDate)
        elif newDate <= startDate:
            raise InvalidSprintDate, "{} is less than or equal to start date of {}".format(value,self.startDate)
        elif newDate <= endQADate:
            raise InvalidSprintDate, "{} is less than or equal to QA's end date of {}".format(value,self.endQADate)
        else:
            self.__endDate = value


    @property
    def endQADate(self):
        return self.__endQADate

    @endQADate.setter
    def endQADate(self,value):
        newDate = None
        try:
            newDate = datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "endQADate must be in format:%s" % Sprint.DATE_FORMAT

        codeFreezeDate = datetime.datetime.strptime(self.codeFreezeDate,Sprint.DATE_FORMAT)
        startDate = datetime.datetime.strptime(self.startDate,Sprint.DATE_FORMAT)
        endDate = datetime.datetime.strptime(self.endDate,Sprint.DATE_FORMAT)

        if newDate <= codeFreezeDate:
            raise InvalidSprintDate, "{} is less than than or equal to code freeze of {}".format(value,self.codeFreezeDate)
        elif newDate <= startDate:
            raise InvalidSprintDate, "{} is less than or equal to start date of {}".format(value,self.startDate)
        elif newDate >= endDate:
            raise InvalidSprintDate, "{} is great than or equal to QA's end date of {}".format(value,self.endDate)
        else:
            self.__endQADate = value

    @property
    def codeFreezeDate(self):
        return self.__codeFreezeDate

    @codeFreezeDate.setter
    def codeFreezeDate(self,value):
        newDate = None
        try:
            datetime.datetime.strptime(value,Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "codeFreezeDate must be in format:%s" % Sprint.DATE_FORMAT


        startDate = datetime.datetime.strptime(self.startDate,Sprint.DATE_FORMAT)
        endDate = datetime.datetime.strptime(self.endDate,Sprint.DATE_FORMAT)
        endQADate = datetime.datetime.strptime(self.endQADate,Sprint.DATE_FORMAT)

        if newDate >= endQADate:
            raise InvalidSprintDate, "{} is greater than than or equal to QA's end date of {}".format(value,self.endQADate)
        elif newDate <= startDate:
            raise InvalidSprintDate, "{} is less than or equal to start date of {}".format(value,self.startDate)
        elif newDate >= endDate:
            raise InvalidSprintDate, "{} is great than or equal to end date of {}".format(value,self.endDate)
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










