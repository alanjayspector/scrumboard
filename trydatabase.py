__author__ = 'alan'

import psycopg2
from utils import toDict
import sys
from card import Card



def setupDatabase(connection):

    cursor = None
    connection.autocommit = True

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1 from pg_database WHERE datname=%s", ("scrumboard_test",))
        if cursor.fetchone():
            print "Found old scrumboard_test table. Dropping..."
            cursor.execute("DROP DATABASE scrumboard_test")
        print "Creating scrumboard_test table."
        cursor.execute("CREATE DATABASE scrumboard_test")
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)
    finally:
        cursor.close()
        connection.close()

def setupTables(connection, user):
    connection.autocommit = True
    cursor = None

#cards
    SQL = """CREATE TABLE cards
(
  "ID" serial NOT NULL,
  description text,
  "storyPoints" integer,
  "completedDate" date,
  "estimatedDevHours" integer DEFAULT 0,
  "needsPOReview" boolean DEFAULT true,
  "hadPOReview" boolean DEFAULT false,
  "needsQA" boolean DEFAULT true,
  "hadQA" boolean DEFAULT false,
  "needsCodeReview" boolean DEFAULT true,
  "hadCodeReview" boolean DEFAULT false,
  "spentDevHours" integer DEFAULT 0,
  "spentQAHours" integer DEFAULT 0,
  qa integer,
  developer integer,
  "startDate" date,
  "estimatedQAHours" integer,
  "placeOnBoard" text,
  "createdDate" date,
  CONSTRAINT cards_pkey PRIMARY KEY ("ID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE cards
  OWNER TO %s;
    """ % user

    print "Creating Cards table."
    try:
        cursor = connection.cursor()
        cursor.execute(SQL)
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


#people
#boards
#sprints

    cursor.close()




def create(connection, obj):
    params = toDict(obj)
    keys = params.keys()
    SQL = 'INSERT INTO {} ("ID",{}) VALUES (DEFAULT,{}) RETURNING "ID";'.format(
        obj.TABLE,
        ",".join(['"{}"'.format(attr) for attr in keys]),
        ",".join(['%({})s'.format(attr)  for attr in keys])
    )
    cursor = connection.cursor()
    cursor.execute(SQL, params)
    newID = cursor.fetchone()[0]
    obj.ID = newID
    connection.commit()
    cursor.close()

def read(connection,obj):
    cursor = connection.cursor()
    params = toDict(obj)
    keys = params.keys()
    SQL = 'SELECT {} from {} where "ID"=%s'.format(
        ",".join(['"{}"'.format(attr) for attr in keys]),
        obj.TABLE)
    cursor.execute(SQL,(obj.ID,))
    returnValue = cursor.fetchone()
    for key,value in zip(params,returnValue):
        setattr(obj,key,value)

    connection.commit()
    cursor.close()


def update(connection,obj):
    cursor = connection.cursor()
    params = toDict(obj)
    keys = params.keys()
    values = [ params[attr] for attr in keys]
    values.append(obj.ID)
    SQL = 'UPDATE {} SET {} WHERE "ID"= %s'.format(
        obj.TABLE,
        ",".join(['"{}"=%s'.format(attr) for attr in keys ])
    )
    cursor.execute(SQL,values)
    cursor.close()

def delete(connection,ID):
    pass


connection = None
user = raw_input("Please input db user:")
password = raw_input("please input password:")

try:

    connection = psycopg2.connect(database='postgres', password=password, user=user)
    setupDatabase(connection)
    connection = psycopg2.connect(database='scrumboard_test', password=password, user=user)
    setupTables(connection,user)



except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)


createCard = Card({
    "description": "As user I want to fly.",
    "storyPoints": 1,
    "estimatedDevHours": 18,
    "estimatedQAHours": 4,
})

create(connection,createCard)
print "Create a card"
print createCard

readCard = Card({"ID":createCard.ID})
read(connection,readCard)
print "Read a card"
print readCard

readCard.description = "As a user I want to dance!"

update(connection,readCard)

readCardAfterUpdate = Card({"ID":createCard.ID})
read(connection,readCardAfterUpdate)
print "Update a card"
print readCardAfterUpdate



connection.close()
