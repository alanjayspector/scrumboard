__author__ = 'alan'

from UserDict import UserDict


class Person(UserDict):
    def __init__(self):
        UserDict.__init__(self)
        self["name"] = None
        self["availableHoursInSprint"] = 0
        self["cardsAssignedTo"] = []






