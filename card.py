__author__ = 'alan'


class CardError(Exception) : pass
class InvalidPlaceOnBoardError(CardError) : pass
class InvalidHourError(CardError) : pass
class InvalidStoryPointError(CardError) : pass
class NeedsPOReviewError(CardError) : pass
class NeedsCodeReviewError(CardError) : pass
class NeedsQAError(CardError) : pass
class InvalidValueError(CardError) : pass
class InvalidPOReviewValueError(CardError) : pass
class InvalidCardAttribute(CardError) : pass
class InvalidAccessOfDict(CardError) : pass


class Card(dict):
    cardDataMap = {
        "storyPoints"  : ( 1,2,3,5,13,40,100 ),
        "placeOnBoard" : [ "Backlog", "Research", "Development", "CodeReview", "POReview", "QA", "Done"],
        "QAArgs"       : ( "QA", "needsQA", "hadQA", NeedsQAError),
        "POReviewArgs"       : ( "POReview", "needsPOReview", "hadPOReview", NeedsPOReviewError),
        "CodeReviewArgs"     : ( "CodeReview", "needsCodeReview", "hadCodeReview", NeedsCodeReviewError),
        "hourArgs" : ( "estimatedQAHours", "estimatedDevHours", "spentQAHours", "spentDevHours"),
        "boolArgs" : ( "needsPOReview", "hadPOReview", "needsQA", "hadQA", \
                       "needsCodeReview", "hadCodeReview")

    }
    STATE_NAME = 0
    NEEDS_STATE_NAME = 1
    HAD_STATE_NAME = 2
    STATE_EXCEPTION = 3

    def __init__(self):
        dict.__init__(self)
        self["storyPoints"] = 1
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
        self["spentQAHours"] = 0
        self["spentDevHours"] = 0
        #use dict _setitem_ since this is an __init__ and doesnt need to follow our workflow
        dict.__setitem__(self,"placeOnBoard","Backlog")
        self["notes"] = []


    def __setitem__(self, key, value):

        if key == "storyPoints":
            if value in Card.cardDataMap[key]:
                    dict.__setitem__(self,key,value)
            else:
                raise InvalidStoryPointError, \
                    "Invalid %s" % key, "Valid story point sizes are:%s" % ",".join(Card.cardDataMap[key])
        elif key in Card.cardDataMap["hourArgs"] :
            if isinstance(value, int) is True and value >= 0:
                dict.__setitem__(self,key,value)
            else:
                raise InvalidHourError, \
                        "Value must be an int not '%s'" % value
        elif key in Card.cardDataMap["boolArgs"] :
            if isinstance(value, bool):
                dict.__setitem__(self,key,value)
            else:
                raise InvalidValueError ,\
                    "%s must be a bool not '%s" % (key,value)
        elif key == "placeOnBoard":
            self.moveCard(value)
        elif key in ( "description", "assignedTo", "notes" ) :
            dict.__setitem__(self,key,value)
        else:
            raise InvalidCardAttribute


    def __CodeReviewCheck(self,previousPlaceOnBoard, newPlaceOnBoard):
            self.__stateCheck(Card.cardDataMap["CodeReviewArgs"], \
                            previousPlaceOnBoard, newPlaceOnBoard)

    def __stateCheck(self,stateArgs, previousPlaceOnBoard, newPlaceOnBoard):
        if self[stateArgs[Card.NEEDS_STATE_NAME]] :
            stateIndex = Card.cardDataMap["placeOnBoard"].index(stateArgs[Card.STATE_NAME])
            previousIndex = Card.cardDataMap["placeOnBoard"].index(previousPlaceOnBoard)
            newIndex = Card.cardDataMap["placeOnBoard"].index(newPlaceOnBoard)

            if newIndex < previousIndex :
                self[stateArgs[Card.HAD_STATE_NAME]] = False
            elif newIndex > previousIndex and \
                            stateIndex < newIndex and not self[stateArgs[Card.HAD_STATE_NAME]] :
                raise stateArgs[Card.STATE_EXCEPTION]
            elif newIndex == stateIndex :
                self[stateArgs[Card.HAD_STATE_NAME]] = True

    def __POReviewCheck(self,previousPlaceOnBoard, newPlaceOnBoard):
        self.__stateCheck(Card.cardDataMap["POReviewArgs"], \
            previousPlaceOnBoard, newPlaceOnBoard)

    def __QACheck(self,previousPlaceOnBoard, newPlaceOnBoard):
        self.__stateCheck(Card.cardDataMap["QAArgs"], \
            previousPlaceOnBoard, newPlaceOnBoard)

    def moveCard(self,place):
        if place in Card.cardDataMap["placeOnBoard"]:
            self.__CodeReviewCheck(self["placeOnBoard"],place)
            self.__QACheck(self["placeOnBoard"],place)
            self.__POReviewCheck(self["placeOnBoard"],place)
            dict.__setitem__(self, "placeOnBoard", place)
        else :
            raise InvalidPlaceOnBoardError, \
                "Valid placements are:%s" % ",".join(Card.cardDataMap["placeOnBoard"])

    def addANote(self,note,noteWriter):
        pass

    def assignPerson(self,person):
        pass

# timeLeftInSprint < (EstimatedDevHours - DevHoursSpent)
    def isCardRed(self,timeLeftInSprint):
        pass

# (DevHoursSpent > EstimatedDevHours)
    def isCardYellow(self):
        pass

#timeLeftInSprint >= ( EstimatedDevHours - DevHoursSpent)
    def isCardGreen(self, timeLeftInSprint):
        pass









