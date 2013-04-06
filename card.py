__author__ = 'alan'

import datetime
import pytz
import utils


class CardError(Exception): pass


class InvalidPlaceOnBoardError(CardError): pass


class InvalidHourError(CardError): pass


class InvalidStoryPointError(CardError): pass


class NeedsPOReviewError(CardError): pass


class NeedsCodeReviewError(CardError): pass


class NeedsQAError(CardError): pass


class InvalidValueError(CardError): pass


class InvalidPOReviewValueError(CardError): pass


class InvalidCardAttribute(CardError): pass


class InvalidAccessOfDict(CardError): pass


class Card(dict):
    cardDataMap = {
        "storyPoints": ( 1, 2, 3, 5, 13, 40, 100 ),
        "placeOnBoard": ["Backlog", "Research", "Development", "CodeReview", "POReview", "QA", "Done"],
        "QAArgs": ( "QA", "needsQA", "hadQA", NeedsQAError),
        "POReviewArgs": ( "POReview", "needsPOReview", "hadPOReview", NeedsPOReviewError),
        "CodeReviewArgs": ( "CodeReview", "needsCodeReview", "hadCodeReview", NeedsCodeReviewError),
        "hourArgs": ( "estimatedQAHours", "estimatedDevHours", "spentDevHours"),
        "boolArgs": ( "needsPOReview", "hadPOReview", "needsQA", "hadQA", \
                      "needsCodeReview", "hadCodeReview"),
        "dateArgs": ( "createdDate", "startDate", "completedDate")

    }
    STATE_NAME = 0
    NEEDS_STATE_NAME = 1
    HAD_STATE_NAME = 2
    STATE_EXCEPTION = 3

    def __init__(self):
        dict.__init__(self)
        self["storyPoints"] = 1
        self["createdDate"] = datetime.datetime.now(pytz.utc).strftime(utils.DATE_FORMAT)
        self["startDate"] = ""
        self["completedDate"] = ""
        self["estimatedQAHours"] = 0
        self["estimatedDevHours"] = 0
        self["needsPOReview"] = True
        self["hadPOReview"] = False
        self["hadCodeReview"] = False
        self["needsCodeReview"] = True
        self["hadQA"] = False
        self["needsQA"] = True
        self["assignedTo"] = None
        self["description"] = None
        self["spentDevHours"] = 0
        #use dict _setitem_ since this is an __init__ and doesnt need to follow our workflow
        dict.__setitem__(self, "placeOnBoard", "Backlog")

    def __setitem__(self, key, value):

        if key == "storyPoints":
            if value in Card.cardDataMap[key]:
                dict.__setitem__(self, key, value)
            else:
                raise InvalidStoryPointError, \
                    "Invalid %s" % key, "Valid story point sizes are:%s" % ",".join(Card.cardDataMap[key])
        elif key in Card.cardDataMap["hourArgs"]:
            if isinstance(value, int) is True and value >= 0:
                dict.__setitem__(self, key, value)
            else:
                raise InvalidHourError, \
                    "Value must be an int not '%s'" % value
        elif key in Card.cardDataMap["boolArgs"]:
            if isinstance(value, bool):
                dict.__setitem__(self, key, value)
            else:
                raise InvalidValueError, \
                    "%s must be a bool not '%s" % (key, value)
        elif key == "placeOnBoard":
            self.moveCard(value)
        elif key in ( "description", "assignedTo"  ):
            dict.__setitem__(self, key, value)
        elif key in Card.cardDataMap["dateArgs"]:
            dict.__setitem__(self, key, value)
        else:
            raise InvalidCardAttribute


    def __CodeReviewCheck(self, previousPlaceOnBoard, newPlaceOnBoard):
        self.__stateCheck(Card.cardDataMap["CodeReviewArgs"], \
                          previousPlaceOnBoard, newPlaceOnBoard)

    def __stateCheck(self, stateArgs, previousPlaceOnBoard, newPlaceOnBoard):
        if self[stateArgs[Card.NEEDS_STATE_NAME]]:
            stateIndex = Card.cardDataMap["placeOnBoard"].index(stateArgs[Card.STATE_NAME])
            previousIndex = Card.cardDataMap["placeOnBoard"].index(previousPlaceOnBoard)
            newIndex = Card.cardDataMap["placeOnBoard"].index(newPlaceOnBoard)

            if newIndex < previousIndex:
                self[stateArgs[Card.HAD_STATE_NAME]] = False
            elif newIndex > previousIndex and \
                            stateIndex < newIndex and not self[stateArgs[Card.HAD_STATE_NAME]]:
                raise stateArgs[Card.STATE_EXCEPTION]
            elif newIndex == stateIndex:
                self[stateArgs[Card.HAD_STATE_NAME]] = True

    def __POReviewCheck(self, previousPlaceOnBoard, newPlaceOnBoard):
        self.__stateCheck(Card.cardDataMap["POReviewArgs"], \
                          previousPlaceOnBoard, newPlaceOnBoard)

    def __QACheck(self, previousPlaceOnBoard, newPlaceOnBoard):
        self.__stateCheck(Card.cardDataMap["QAArgs"], \
                          previousPlaceOnBoard, newPlaceOnBoard)

    def moveCard(self, place):
        if place in Card.cardDataMap["placeOnBoard"]:
            self.__CodeReviewCheck(self["placeOnBoard"], place)
            self.__QACheck(self["placeOnBoard"], place)
            self.__POReviewCheck(self["placeOnBoard"], place)
            dict.__setitem__(self, "placeOnBoard", place)
        else:
            raise InvalidPlaceOnBoardError, \
                "Valid placements are:%s" % ",".join(Card.cardDataMap["placeOnBoard"])

    def isCardRed(self, timeLeftInSprint):
        if self["placeOnBoard"] == "Done":
            return False

        evaluatedHours = ( self["estimatedDevHours"] - self["spentDevHours"]) \
            if self["estimatedDevHours"] > self["spentDevHours"] else self["spentDevHours"]

        if timeLeftInSprint <= evaluatedHours:
            return True
        else:
            return False

    def isCardYellow(self, timeLeftInSprint):
        if self["placeOnBoard"] == "Done":
            return False
        elif self["spentDevHours"] >= self["estimatedDevHours"]:
            return True


    def isCardGreen(self, timeLeftInSprint):
        if self["placeOnBoard"] == "Done":
            return True
        elif self.isCardYellow(timeLeftInSprint):
            return False
        elif self.isCardRed(timeLeftInSprint):
            return False
        else:
            return True














