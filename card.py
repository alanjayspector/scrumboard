__author__ = 'alan'


class CardError(Exception) : pass
class InvalidPlaceOnBoardError(CardError) : pass
class InvalidHourError(CardError) : pass
class InvalidStoryPointError(CardError) : pass
class NeedsPOReviewError(CardError) : pass
class NeedsCodeReviewError(CardError) : pass
class InvalidPOReviewValueError(CardError) : pass
class InvalidCardAttribute(CardError) : pass
class InvalidAccessOfDict(CardError) : pass


class Card(dict):
    cardDataMap = {
        "storyPoints"  : ( 1,2,3,5,13,40,100 ),
        "placeOnBoard" : [ "Backlog", "Research", "Development", "CodeReview", "POReview", "QA", "Done"]
    }
    def __init__(self):
        dict.__init__(self)
        self["storyPoints"] = 1
        self["estimatedQAHours"] = 0
        self["estimatedDevHours"] = 0
        self["needsPOReview"] = True
        self["hadPOReview"] = False
        self["hadCodeReview"] = False
        self["needsCodeReview"] = True
        self["needsQA"] = True
        self["assignedTo"] = None
        self["description"] = None
        self["QAHoursSpent"] = 0
        self["DevHoursSpent"] = 0
        self["placeOnBoard"] = "Backlog"
        self["notes"] = []


    def __setitem__(self, key, value):

        if key == "storyPoints":
            if value in Card.cardDataMap[key]:
                    dict.__setitem__(self,key,value)
            else:
                raise InvalidStoryPointError, \
                    "Invalid %s" % key, "Valid story point sizes are:%s" % ",".join(Card.cardDataMap[key])

        elif key in ( "estimatedQAHours", "estimatedDevHours", "QAHoursSpent", "DevHoursSpent"):
            if isinstance(value, int) is True and value >= 0:
                dict.__setitem__(self,key,value)
            else:
                raise InvalidHourError, \
                        "Value must be an int not '%s'" % value
        elif key in ( "needsPOReview", "needsQA", "needsCodeReview" ):
            if isinstance(value, bool):
                dict.__setitem__(self,key,value)
            else:
                raise InvalidPOReviewValueError ,\
                    "%s must be a bool not '%s" % (key,value)
        elif key == "placeOnBoard":
            self.moveCard(value)
        elif key in ( "description", "assignedTo", "hadPOReview", \
                      "notes", "hadQA", "hadCodeReview"):
            dict.__setitem__(self,key,value)
        else:
            raise InvalidCardAttribute


    def __CodeReviewCheck(self,previousPlaceOnBoard, newPlaceOnBoard):
        if self["needsCodeReview"] :
            stateIndex = Card.cardDataMap["placeOnBoard"].index("CodeReview")
            previousIndex = Card.cardDataMap["placeOnBoard"].index(previousPlaceOnBoard)
            newIndex = Card.cardDataMap["placeOnBoard"].index(newPlaceOnBoard)

            if newIndex < previousIndex :
                self["hadCodeReview"] = False




    def __POReviewCheck(self,previousPlaceOnBoard, newPlaceOnBoard):
        if self["needsPOReview"] and previousPlaceOnBoard == "POReview" :
            previousIndex = Card.cardDataMap["placeOnBoard"].index(previousPlaceOnBoard)
            newIndex = Card.cardDataMap["placeOnBoard"].index(newPlaceOnBoard)
            if newIndex < previousIndex :
                self["hadPOReview"] = False



    def __QACheck(self,previousPlaceOnBoard, newPlaceOnBoard):
        if self["needsQA"] and previousPlaceOnBoard == "QA" :
            previousIndex = Card.cardDataMap["placeOnBoard"].index(previousPlaceOnBoard)
            newIndex = Card.cardDataMap["placeOnBoard"].index(newPlaceOnBoard)
            if newIndex < previousIndex :
                self["hadQA"] = False


    def __moveCardToBacklog(self,previousPlaceOnBoard):
        dict.__setitem__(self,"placeOnBoard", "Backlog")

    def __moveCardToResearch(self,previousPlaceOnBoard):
        dict.__setitem__(self,"placeOnBoard", "Research")

    def __moveCardToDevelopment(self,previousPlaceOnBoard):
        dict.__setitem__(self,"placeOnBoard", "Development")

    def __moveCardToCodeReview(self,previousPlaceOnBoard):
        dict.__setitem__(self,"placeOnBoard", "CodeReview")
        pass

    def __moveCardToPOReview(self,previousPlaceOnBoard):
        dict.__setitem__(self,"placeOnBoard", "POReview")

    def __moveCardToQA(self,previousPlaceOnBoard):
        dict.__setitem__(self,"placeOnBoard", "QA")

    def __moveCardToDone(self,previousPlaceOnBoard):
        dict.__setitem__(self,"placeOnBoard", "Done")


    def moveCard(self,place=None):
        if place in Card.cardDataMap["placeOnBoard"]:
            move_card_function = getattr(self,"__moveCardTo%s" % place)
            self.__CodeReviewCheck(self["placeOnBoard"],place)
            self.__QA(self["placeOnBoard"],place)
            self.__POReviewCheck(self["placeOnBoard"],place)
            return move_card_function(self["placeOnBard"])
        else :
            raise InvalidPlaceOnBoardError, \
                "Valid placements are:%s" % ",".join(Card.cardDataMap["placeOnBoard"])


#                if value == "Done" and self["needsPOReview"] and not self["hadPOReview"]:
#                    raise NeedsPOReviewError, \
#                         "This card can not be moved to Done till it has had a PO Review"
#                elif value == "Done" and not self["hadCodeReview"]:
#                    raise NeedsCodeReviewError, \
#                         "This card can not be moved to Done till it has had a Code Review"


    def addANote(self,note,noteWriter):
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









