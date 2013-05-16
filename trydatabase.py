__author__ = 'alan'

import psycopg2
import utils
import sys
from card import Card



con = None

try:

    con = psycopg2.connect(database=raw_input("database:"), password=raw_input("password:"), user=raw_input("user:"))
    cur = con.cursor()


except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)



def createCard(con, params):
    pass

def readCard(con,ID):
    pass

def updateCard(con,ID,params):
    pass

def deleteCard(con,ID):
    pass


exampleCard = Card({
    "description": "As user I want to fly.",
    "storyPoints": 1,
    "estimatedDevHours": 18,
    "estimatedQAHours": 4,
})

createCard(con,exampleCard)

print exampleCard

con.close()
