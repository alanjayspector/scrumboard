__author__ = 'alan'

import psycopg2
import sys


con = None

try:

    con = psycopg2.connect(database=raw_input("database:"), password=raw_input("password:"), user=raw_input("user:"))
    cur = con.cursor()
    cur.execute('SELECT version()')
    ver = cur.fetchone()
    print ver


except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)


finally:

    if con:
        con.close()
