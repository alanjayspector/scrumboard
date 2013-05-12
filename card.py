__author__ = 'alan'

import datetime
import pytz
from string import Template


class CardError(Exception): pass


class NotADeveloperError(CardError): pass


class NotQAError(CardError): pass


class InvalidPlaceOnBoardError(CardError): pass


class NoQAAssignedError(CardError): pass


class NoDeveloperAssignedError(CardError): pass


class InvalidHourError(CardError): pass


class InvalidStoryPointError(CardError): pass


class NeedsPOReviewError(CardError): pass


class NeedsCodeReviewError(CardError): pass


class NeedsQAError(CardError): pass


class InvalidValueError(CardError): pass


class InvalidPOReviewValueError(CardError): pass


class InvalidCardAttribute(CardError): pass


class InvalidAccessOfDict(CardError): pass


class InvalidConstructorParams(CardError): pass


class Card(object):
    cardDataMap = {
        "storyPoints": ( 1, 2, 3, 5, 13, 40, 100 ),
        "placeOnBoard": ["Backlog", "Research", "Development", "CodeReview", "POReview", "QA", "Done"],
        "QAArgs": ( "QA", "needsQA", "hadQA", NeedsQAError),
        "POReviewArgs": ( "POReview", "needsPOReview", "hadPOReview", NeedsPOReviewError),
        "CodeReviewArgs": ( "CodeReview", "needsCodeReview", "hadCodeReview", NeedsCodeReviewError),
        "defaultParams": {
            "storyPoints": 1,
            "completedDate": None,
            "estimatedDevHours": 0,
            "needsPOReview": True,
            "hadPOReview": False,
            "hadCodeReview": False,
            "needsCodeReview": True,
            "hadQA": False,
            "needsQA": True,
            "description": None,
            "spentDevHours": 0,
            "spentQAHours": 0,
            "placeOnBoard": "Backlog",
            "qa": None,
            "developer": None
        }
    }
    STATE_NAME = 0
    NEEDS_STATE_NAME = 1
    HAD_STATE_NAME = 2
    STATE_EXCEPTION = 3
    IDctr = 0
    DATE_FORMAT = "%Y/%m/%d"
    __printTemplate = Template("""
--------------------------------
ID:$cardID
$description
Dev:$developer, $spentDevHours/$estimatedDevHours hours
QA:$qa, $estimatedQAHours hours
In:$placeOnBoard, $storyPoints SP
--------------------------------
""")

    def __init__(self, params=None):

        self.__cardID = Card.getNextID()
        self.__createdDate = datetime.datetime.now().strftime(Card.DATE_FORMAT)
        self.__storyPoints = 1
        self.startDate = None
        self.completedDate = None
        self.__estimatedQAHours = 0
        self.__estimatedDevHours = 0
        self.__needsPOReview = True
        self.__hadPOReview = False
        self.__hadCodeReview = False
        self.__needsCodeReview = True
        self.__hadQA = False
        self.__needsQA = True
        self.description = None
        self.__spentDevHours = 0
        self.__spentQAHours = 0
        self.__developer = None
        self.__qa = None
        self.__placeOnBoard = "Backlog"

        if isinstance(params, dict):
            placeOnBoard = params.pop("placeOnBoard", None)
            for key in params:
                if hasattr(self, key):
                    setattr(self, key, params[key])
            if placeOnBoard:
                self.placeOnBoard = placeOnBoard

    @property
    def developer(self):
        return self.__developer

    @developer.setter
    def developer(self, person):
        if not hasattr(person, "isADeveloper") or not person.isADeveloper:
            raise NotADeveloperError
        else:
            self.__developer = person

    @property
    def qa(self):
        return self.__qa

    @qa.setter
    def qa(self, person):
        if not hasattr(person, "isADeveloper") or person.isADeveloper:
            raise NotQAError
        else:
            self.__qa = person

    def __eq__(self, other):
        return self.cardID == other.cardID

    @property
    def createdDate(self):
        return self.__createdDate

    @createdDate.setter
    def createdDate(self, value):
        pass

    @staticmethod
    def getNextID():
        Card.IDctr += 1
        return Card.IDctr

    def __str__(self):
        developerName = "not assigned"
        qaName = "not assigned"
        if self.developer:
            developerName = self.developer.fullName
        if self.qa:
            qaName = self.qa.fullName

        cardInfo = {"storyPoints": self.storyPoints, "description": self.description, \
                    "estimatedDevHours": self.estimatedDevHours, "estimatedQAHours": self.estimatedQAHours, \
                    "qa": qaName, "developer": developerName, "spentDevHours": self.spentDevHours, \
                    "placeOnBoard": self.placeOnBoard, "cardID": self.cardID
        }
        return Card.__printTemplate.substitute(cardInfo)


    @property
    def storyPoints(self):
        return self.__storyPoints

    @storyPoints.setter
    def storyPoints(self, value):
        if value in Card.cardDataMap["storyPoints"]:
            self.__storyPoints = value
        else:
            raise InvalidStoryPointError, \
                "Valid story point sizes are:%s" % \
                ",".join([str(points) for points in Card.cardDataMap["storyPoints"]])

    @property
    def estimatedQAHours(self):
        return self.__estimatedQAHours

    @estimatedQAHours.setter
    def estimatedQAHours(self, value):
        if isinstance(value, int) is True and value >= 0:
            self.__estimatedQAHours = value
        else:
            raise InvalidHourError, \
                "Value must be an positive int not '%s'" % value

    @property
    def estimatedDevHours(self):
        return self.__estimatedDevHours


    @estimatedDevHours.setter
    def estimatedDevHours(self, value):
        if isinstance(value, int) is True and value >= 0:
            self.__estimatedDevHours = value
        else:
            raise InvalidHourError, \
                "Value must be an positive int not '%s'" % value

    @property
    def spentDevHours(self):
        return self.__spentDevHours

    @spentDevHours.setter
    def spentDevHours(self, value):
        if not self.developer:
            raise NoDeveloperAssignedError
        elif isinstance(value, int) is True and value >= 0:
            self.__spentDevHours = value
            self.developer.spentSprintHours += value
        else:
            raise InvalidHourError, \
                "Value must be an positive int not '%s'" % value


    @property
    def spentQAHours(self):
        return self.__spentQAHours

    @spentQAHours.setter
    def spentQAHours(self, value):
        if not self.qa:
            raise NoQAAssignedError
        elif isinstance(value, int) is True and value >= 0:
            self.__spentQAHours = value
            self.qa.spentSprintHours += value
        else:
            raise InvalidHourError, \
                "Value must be an positive int not '%s'" % value

    @property
    def needsPOReview(self):
        return self.__needsPOReview

    @needsPOReview.setter
    def needsPOReview(self, value):
        if isinstance(value, bool):
            self.__needsPOReview = value
        else:
            raise InvalidValueError, \
                "needsPOReview must be a bool not '%s" % value

    @property
    def hadPOReview(self):
        return self.__hadPOReview

    @hadPOReview.setter
    def hadPOReview(self, value):
        if isinstance(value, bool):
            self.__hadPOReview = value
        else:
            raise InvalidValueError, \
                "hadPOReview must be a bool not '%s" % value

    @property
    def needsQA(self):
        return self.__needsQA

    @needsQA.setter
    def needsQA(self, value):
        if isinstance(value, bool):
            self.__needsQA = value
        else:
            raise InvalidValueError, \
                "needsQA must be a bool not '%s" % value

    @property
    def hadQA(self):
        return self.__hadQA

    @hadQA.setter
    def hadQA(self, value):
        if isinstance(value, bool):
            self.__hadQA = value
        else:
            raise InvalidValueError, \
                "hadQA must be a bool not '%s" % value

    @property
    def needsCodeReview(self):
        return self.__needsCodeReview

    @needsCodeReview.setter
    def needsCodeReview(self, value):
        if isinstance(value, bool):
            self.__needsCodeReview = value
        else:
            raise InvalidValueError, \
                "needsCodeReview must be a bool not '%s" % value

    @property
    def hadCodeReview(self):
        return self.__hadCodeReview

    @hadCodeReview.setter
    def hadCodeReview(self, value):
        if isinstance(value, bool):
            self.__hadCodeReview = value
        else:
            raise InvalidValueError, \
                "hadCodeReview must be a bool not '%s" % value

    @property
    def cardID(self):
        return self.__cardID

    @cardID.setter
    def cardID(self, value):
        pass

    @property
    def placeOnBoard(self):
        return self.__placeOnBoard

    @placeOnBoard.setter
    def placeOnBoard(self, value):
        current_place = self.__placeOnBoard
        if value in Card.cardDataMap["placeOnBoard"]:
            if value == self.placeOnBoard:
                return None
            elif value == "QA" and not self.qa:
                raise NoQAAssignedError
            elif value != "Backlog" and not self.developer:
                raise NoDeveloperAssignedError
            else:
                self.__CodeReviewCheck(current_place, value)
                self.__QACheck(current_place, value)
                self.__POReviewCheck(current_place, value)
                self.__placeOnBoard = value
        else:
            raise InvalidPlaceOnBoardError, \
                "Valid placements are:%s" % ",".join(Card.cardDataMap["placeOnBoard"])
        return None


    def __CodeReviewCheck(self, previousPlaceOnBoard, newPlaceOnBoard):
        self.__stateCheck(Card.cardDataMap["CodeReviewArgs"], \
                          previousPlaceOnBoard, newPlaceOnBoard)

    def __stateCheck(self, stateArgs, previousPlaceOnBoard, newPlaceOnBoard):
        condition = getattr(self, stateArgs[Card.NEEDS_STATE_NAME])
        if condition:
            stateIndex = Card.cardDataMap["placeOnBoard"].index(stateArgs[Card.STATE_NAME])
            previousIndex = Card.cardDataMap["placeOnBoard"].index(previousPlaceOnBoard)
            newIndex = Card.cardDataMap["placeOnBoard"].index(newPlaceOnBoard)

            if newIndex < previousIndex:
                setattr(self, stateArgs[Card.HAD_STATE_NAME], False)
            elif newIndex > previousIndex and \
                            stateIndex < newIndex and not getattr(self, stateArgs[Card.HAD_STATE_NAME]):
                raise stateArgs[Card.STATE_EXCEPTION]
            elif newIndex == stateIndex:
                setattr(self, stateArgs[Card.HAD_STATE_NAME], True)

    def __POReviewCheck(self, previousPlaceOnBoard, newPlaceOnBoard):
        self.__stateCheck(Card.cardDataMap["POReviewArgs"], \
                          previousPlaceOnBoard, newPlaceOnBoard)

    def __QACheck(self, previousPlaceOnBoard, newPlaceOnBoard):
        self.__stateCheck(Card.cardDataMap["QAArgs"], \
                          previousPlaceOnBoard, newPlaceOnBoard)

    def isCardUnderestimated(self):
        if self.spentDevHours > self.estimatedDevHours:
            return True
        else:
            return False

    def isCardRed(self, timeLeftInSprint):
        if self.placeOnBoard == "Done":
            return False

        evaluatedHours = ( self.estimatedDevHours - self.spentDevHours ) \
            if self.estimatedDevHours > self.spentDevHours else self.spentDevHours

        if timeLeftInSprint <= evaluatedHours:
            return True
        else:
            return False

    def isCardYellow(self, timeLeftInSprint):
        if self.placeOnBoard == "Done":
            return False
        elif self.spentDevHours >= self.estimatedDevHours:
            return True
        else:
            return False

    def status(self, timeLeftInSprint):
        if self.isCardRed(timeLeftInSprint):
            return "Red"
        elif self.isCardYellow(timeLeftInSprint):
            return "Yellow"
        elif self.isCardGreen(timeLeftInSprint):
            return "Green"

    def isCardGreen(self, timeLeftInSprint):
        if self.placeOnBoard == "Done":
            return True
        elif self.isCardYellow(timeLeftInSprint):
            return False
        elif self.isCardRed(timeLeftInSprint):
            return False
        else:
            return True














