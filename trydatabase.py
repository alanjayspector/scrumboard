__author__ = 'alan'

import psycopg2
from utils import toDict
import sys
from card import Card



con = None

try:

    connection = psycopg2.connect(database=raw_input("database:"), password=raw_input("password:"), user=raw_input("user:"))
    cur = connection.cursor()


except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)



def createCard(connection, card):
    params = toDict(card)
    keys = params.keys()
    SQL = 'INSERT INTO cards ("cardID",{}) VALUES (DEFAULT,{}) RETURNING "cardID";'.format(
        ",".join(['"{}"'.format(attr) for attr in keys]),
        ",".join(['%({})s'.format(attr)  for attr in keys])
    )
    print SQL
    cursor = connection.cursor()
    cursor.execute(SQL, params)
    newID = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    return newID

def readCard(connection,ID):
    pass

def updateCard(connection,ID,params):
    pass

def deleteCard(connection,ID):
    pass


exampleCard = Card({
    "description": "As user I want to fly.",
    "storyPoints": 1,
    "estimatedDevHours": 18,
    "estimatedQAHours": 4,
})

cardID = createCard(connection,exampleCard)

print exampleCard

connection.close()
