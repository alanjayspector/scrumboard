__author__ = 'alan'

import re


class CRUD(object):
    def __init__(self):
        pass


    def create(self):
        params = self.toDict()
        keys = params.keys()
        SQL = 'INSERT INTO {} ("ID",{}) VALUES (DEFAULT,{}) RETURNING "ID";'.format(
            self.TABLE,
            ",".join(['"{}"'.format(attr) for attr in keys]),
            ",".join(['%({})s'.format(attr)  for attr in keys])
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
        cursor.execute(SQL,(self.ID,))
        returnValue = cursor.fetchone()
        cursor.close()
        if returnValue is not None:
            for key,value in zip(params,returnValue):
                setattr(self,key,value)
            return True
        else:
            return False


    def toDict(self):
        ourDict = {}
        for k,v in self.__dict__.items():
            if re.search("__ID$", k):
                continue
            if re.match("^connection$",k):
                continue
            protected_attr_check = re.search("__(\w+)$", k)
            if protected_attr_check:
                groups = protected_attr_check.groups()
                if len(groups) > 1:
                    raise Exception,\
                        "atttribute {} breaks toDict() check _<CLASS>__attribute".format(k)
                ourDict[groups[0]] = v
            else:
                if hasattr(v,"ID"):
                    ourDict[k] = v.ID
                elif isinstance(v, dict):
                    ourDict[k] = v.keys()
                else:
                    ourDict[k] = v
        return ourDict


    def update(self):
        cursor = self.connection.cursor()
        params = self.toDict()
        keys = params.keys()
        values = [ params[attr] for attr in keys]
        values.append(self.ID)
        SQL = 'UPDATE {} SET {} WHERE "ID"= %s'.format(
            self.TABLE,
            ",".join(['"{}"=%s'.format(attr) for attr in keys ])
        )
        cursor.execute(SQL,values)
        self.connection.commit()
        cursor.close()

    def delete(self):
        cursor = self.connection.cursor()
        SQL = 'DELETE FROM {} where "ID"=%s'.format(self.TABLE)
        cursor.execute(SQL,(self.ID,))
        self.connection.commit()
        cursor.close()