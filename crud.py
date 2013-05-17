__author__ = 'alan'


class CRUD(object):
    def __init__(self):
        pass


    def create(self):
        params = self.toDict()
        keys = params.keys()
        SQL = 'INSERT INTO {} ("ID",{}) VALUES (DEFAULT,{}) RETURNING "ID";'.format(
            self.TABLE,
            ",".join(['"{}"'.format(attr) for attr in keys]),
            ",".join(['%({})s'.format(attr) for attr in keys])
        )
        cursor = self.connection.cursor()
        cursor.execute(SQL, params)
        newID = cursor.fetchone()[0]
        self.ID = newID
        self.connection.commit()
        cursor.close()

    def read(self):
        cursor = self.connection.cursor()
        params = self.toDict()
        keys = params.keys()
        SQL = 'SELECT {} from {} where "ID"=%s'.format(
            ",".join(['"{}"'.format(attr) for attr in keys]),
            self.TABLE)
        cursor.execute(SQL, (self.ID,))
        returnValue = cursor.fetchone()
        cursor.close()
        if returnValue is not None:
            for key, value in zip(keys, returnValue):
                setattr(self, key, value)
            return True
        else:
            return False


    def toDict(self):
        ourDict = {}
        for k in self.db_columns():
            ourDict[k] = getattr(self, k)
        for k in self.db_objects():
            obj = getattr(self, k)
            if obj:
                ourDict[k] = obj.ID
            else:
                ourDict[k] = None
        return ourDict


    def update(self):
        cursor = self.connection.cursor()
        params = self.toDict()
        keys = params.keys()
        values = [params[attr] for attr in keys]
        values.append(self.ID)
        SQL = 'UPDATE {} SET {} WHERE "ID"= %s'.format(
            self.TABLE,
            ",".join(['"{}"=%s'.format(attr) for attr in keys])
        )
        cursor.execute(SQL, values)
        self.connection.commit()
        cursor.close()

    def delete(self):
        cursor = self.connection.cursor()
        SQL = 'DELETE FROM {} where "ID"=%s'.format(self.TABLE)
        cursor.execute(SQL, (self.ID,))
        self.connection.commit()
        cursor.close()