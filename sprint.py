__author__ = 'alanspector'

import datetime
from scrumboard import Scrumboard


class SprintException(Exception): pass


class InvalidSprintDateFormat(SprintException): pass


class InvalidSprintDate(SprintException): pass


class InvalidHoursPerDay(SprintException): pass


class Sprint(object):
    IDctr = 0
    DATE_FORMAT = "%Y/%m/%d"


    def __init__(self, params=None):
        startDate = datetime.datetime.now()
        self.__sprintID = Sprint.getNextID()
        self.__startDate = startDate.strftime(Sprint.DATE_FORMAT)
        self.__endDate = (startDate + datetime.timedelta(days=13)).strftime(Sprint.DATE_FORMAT)
        self.__hoursPerDay = 4
        self.__codeFreezeDate = (startDate + datetime.timedelta(days=7)).strftime(Sprint.DATE_FORMAT)
        self.__endQADate = (startDate + datetime.timedelta(days=12)).strftime(Sprint.DATE_FORMAT)
        self.name = None
        self.scrumBoard = Scrumboard(self)
        if isinstance(params, dict):
            params.pop("scrumBoard", None)
            for key in params:
                if hasattr(self, key):
                    setattr(self, key, params[key])

    @property
    def hoursPerDay(self):
        return self.__hoursPerDay

    @hoursPerDay.setter
    def hoursPerDay(self, value):
        if isinstance(value, int) is True and value >= 1 and value <= 24:
            self.__hoursPerDay = value
        else:
            raise InvalidHoursPerDay, "{} must be between 1 and 24.".format(value)

    @property
    def startDate(self):
        return self.__startDate

    @startDate.setter
    def startDate(self, value):
        newDate = None
        try:
            newDate = datetime.datetime.strptime(value, Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "startDate must be in format:%s" % Sprint.DATE_FORMAT

        if self.codeFreezeDate:
            codeFreezeDate = datetime.datetime.strptime(self.codeFreezeDate, Sprint.DATE_FORMAT)
            if newDate >= codeFreezeDate:
                raise InvalidSprintDate, "{} is greater than or equal to code freeze of {}".format(value,
                                                                                                   self.codeFreezeDate)
        if self.endDate:
            endDate = datetime.datetime.strptime(self.endDate, Sprint.DATE_FORMAT)
            if newDate >= endDate:
                raise InvalidSprintDate, "{} is greater than or equal to end date of {}".format(value, self.endDate)
        if self.endQADate:
            endQADate = datetime.datetime.strptime(self.endQADate, Sprint.DATE_FORMAT)
            if newDate >= endQADate:
                raise InvalidSprintDate, "{} is greater than or equal to end QA date of {}".format(value,
                                                                                                   self.endQADate)

        self.__startDate = value


    @property
    def endDate(self):
        return self.__endDate

    @endDate.setter
    def endDate(self, value):
        newDate = None
        try:
            newDate = datetime.datetime.strptime(value, Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "endDate must be in format:%s" % Sprint.DATE_FORMAT

        if self.codeFreezeDate:
            codeFreezeDate = datetime.datetime.strptime(self.codeFreezeDate, Sprint.DATE_FORMAT)
            if newDate <= codeFreezeDate:
                raise InvalidSprintDate, "{} is less than than or equal to code freeze of {}".format(value,
                                                                                                     self.codeFreezeDate)
        if self.startDate:
            startDate = datetime.datetime.strptime(self.startDate, Sprint.DATE_FORMAT)
            if newDate <= startDate:
                raise InvalidSprintDate, "{} is less than or equal to start date of {}".format(value, self.startDate)

        if self.endQADate:
            endQADate = datetime.datetime.strptime(self.endQADate, Sprint.DATE_FORMAT)
            if newDate <= endQADate:
                raise InvalidSprintDate, "{} is less than or equal to QA's end date of {}".format(value, self.endQADate)

        self.__endDate = value


    @property
    def endQADate(self):
        return self.__endQADate

    @endQADate.setter
    def endQADate(self, value):
        newDate = None
        try:
            newDate = datetime.datetime.strptime(value, Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "endQADate must be in format:%s" % Sprint.DATE_FORMAT

        if self.codeFreezeDate:
            codeFreezeDate = datetime.datetime.strptime(self.codeFreezeDate, Sprint.DATE_FORMAT)
            if newDate <= codeFreezeDate:
                raise InvalidSprintDate, "{} is less than than or equal to code freeze of {}".format(value,
                                                                                                     self.codeFreezeDate)
        if self.startDate:
            startDate = datetime.datetime.strptime(self.startDate, Sprint.DATE_FORMAT)
            if newDate <= startDate:
                raise InvalidSprintDate, "{} is less than or equal to start date of {}".format(value, self.startDate)

        if self.endDate:
            endDate = datetime.datetime.strptime(self.endDate, Sprint.DATE_FORMAT)
            if newDate >= endDate:
                raise InvalidSprintDate, "{} is great than or equal to QA's end date of {}".format(value, self.endDate)

        self.__endQADate = value

    @property
    def codeFreezeDate(self):
        return self.__codeFreezeDate

    @codeFreezeDate.setter
    def codeFreezeDate(self, value):
        newDate = None
        try:
            newDate = datetime.datetime.strptime(value, Sprint.DATE_FORMAT)
        except ValueError:
            raise InvalidSprintDateFormat, "codeFreezeDate must be in format:%s" % Sprint.DATE_FORMAT

        startDate = datetime.datetime.strptime(self.startDate, Sprint.DATE_FORMAT)
        endDate = datetime.datetime.strptime(self.endDate, Sprint.DATE_FORMAT)
        endQADate = datetime.datetime.strptime(self.endQADate, Sprint.DATE_FORMAT)

        if newDate >= endQADate:
            raise InvalidSprintDate, "{} is greater than than or equal to QA's end date of {}".format(value,
                                                                                                      self.endQADate)
        elif newDate <= startDate:
            raise InvalidSprintDate, "{} is less than or equal to start date of {}".format(value, self.startDate)
        elif newDate >= endDate:
            raise InvalidSprintDate, "{} is great than or equal to end date of {}".format(value, self.endDate)
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

    def getDevTimeLeftInSprint(self, dateToCalculateFrom=datetime.datetime.today()):
        codeFreezeDate = datetime.datetime.strptime(self.codeFreezeDate, Sprint.DATE_FORMAT)
        return self.__getTimeLeftInSprint(dateToCalculateFrom, codeFreezeDate)

    def getQATimeLeftInSprint(self, dateToCalculateFrom=datetime.datetime.today()):
        endQADate = datetime.datetime.strptime(self.endQADate, Sprint.DATE_FORMAT)
        return self.__getTimeLeftInSprint(dateToCalculateFrom, endQADate)

    def __getTimeLeftInSprint(self, currentDate, endDate):
        delta = endDate - currentDate
        return delta.days * self.hoursPerDay










