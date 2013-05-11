__author__ = 'alanspector'

import datetime
from person import Person
from card import Card
from sprint import Sprint
from scrumboard import Scrumboard
import random
import pytz


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def getLocalizeDateTime(date_string, tz):
    utc_dt = datetime.datetime.strptime(date_string, DATE_FORMAT)
    utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    loc_dt = utc_dt.astimezone(tz)
    return loc_dt.strftime(DATE_FORMAT)



def timeZoneChangeExample():
        dateString = None
        easternTZ = pytz.timezone("US/Eastern")
        westernTZ = pytz.timezone("US/Pacific")
        centralTZ = pytz.timezone("US/Central")
        utcTZ = pytz.timezone("UTC")
        print dateString
        print getLocalizeDateTime(dateString, easternTZ)
        print getLocalizeDateTime(dateString, westernTZ)
        print getLocalizeDateTime(dateString, centralTZ)
        print getLocalizeDateTime(dateString, utcTZ)

        return True


def generateCard(person):
    card = Card()
    card.storyPoints = Card.cardDataMap["storyPoints"][random.randint(0,5)]
    card.estimatedDevHours = random.randint(1,16)
    card.estimatedQAHours= random.randint(2,6)
    card.description = "Random Description:%d" % random.randint(1,375)
    card.person = person
    return card

def generatePerson(sprintID = 1):
    person = Person({ "firstName":"Alan", "lastName": "Spector", \
                      "currentSprintID":1, "estimatedSprintHours":32 })

    for i in range(random.randint(2,10)):
        card = generateCard(person)
        person.addCardToCurrentSprint(card)

    return person

def generateSprint():
    sprint = Sprint()
    scrumboard = Scrumboard(sprint)



