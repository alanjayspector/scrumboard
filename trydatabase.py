__author__ = 'alan'

import psycopg2
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

def setupCards(connection,user):
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
CONSTRAINT cards_pkey PRIMARY KEY ("ID"),
CONSTRAINT qa_people_fk FOREIGN KEY ("qa")
      REFERENCES people ("ID") MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
CONSTRAINT developer_people_fk FOREIGN KEY ("developer")
      REFERENCES people ("ID") MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
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
    cursor.close()


def setupPeople(connection,user):
    SQL = """CREATE TABLE people
(
"ID" serial NOT NULL,
"firstName" text,
"lastName" text,
"estimatedSprintHours" integer DEFAULT 0,
"spentSprintHours" integer DEFAULT 0,
"isADeveloper" boolean DEFAULT true,
"avatar" text,
CONSTRAINT people_pkey PRIMARY KEY ("ID")
)
WITH (
OIDS=FALSE
);
ALTER TABLE people
OWNER TO %s;
""" % user

    print "Creating People table."
    try:
        cursor = connection.cursor()
        cursor.execute(SQL)
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)
    cursor.close()


def setupTables(connection, user):
    connection.autocommit = True
    setupPeople(connection,user)
    setupCards(connection,user)


def crudToCard():
    createCard = Card({
        "description": "As user I want to fly.",
        "storyPoints": 1,
        "estimatedDevHours": 18,
        "estimatedQAHours": 4,
    })

    createCard.create(connection)
    print "Create a card"
    print createCard

    readCard = Card({"ID":createCard.ID})
    readCard.read(connection)
    print "Read a card"
    print readCard

    readCard.description = "As a user I want to dance!"

    readCard.update(connection)

    readCardAfterUpdate = Card({"ID":createCard.ID})
    readCardAfterUpdate.read(connection)
    print "Update a card"
    print readCardAfterUpdate
    return

    readCardAfterUpdate.delete(connection)


    readCardAfterDelete = Card({"ID":createCard.ID})
    successfulDelete = readCardAfterDelete.read(connection)
    print "Delete a card"
    if successfulDelete is False:
        print "Delete Successful."
    else:
        print "Delete Failed."


connection = None
user = raw_input("Please input db user:")
password = raw_input("please input password:")

try:

    connection = psycopg2.connect(database='postgres', password=password, user=user)
    setupDatabase(connection)
    connection = psycopg2.connect(database='scrumboard_test', password=password, user=user)
    setupTables(connection,user)
    crudToCard()


    connection.close()

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)



