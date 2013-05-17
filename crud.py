__author__ = 'alan'

from utils import toDict


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
    cursor.close()
    if returnValue is not None:
        for key,value in zip(params,returnValue):
            setattr(obj,key,value)
        return obj
    else:
        return None



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
    connection.commit()
    cursor.close()

def delete(connection,obj):
    cursor = connection.cursor()
    SQL = 'DELETE FROM {} where "ID"=%s'.format(obj.TABLE)
    cursor.execute(SQL,(obj.ID,))
    connection.commit()
    cursor.close()