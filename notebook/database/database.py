import sqlite3

class Database:
    """docstring for Database"""
    def __init__(self):
        self.connection = sqlite3.connect('knowlegde.db')
        self.c = self.connection.cursor()
        self.createTables()
    def createTables(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS entidade(id text, name text, desc text, pageid text, url text)')
        self.c.execute('CREATE TABLE IF NOT EXISTS relation(id text, desc text)')
        self.connection.commit()
    def insertEntitie(self, entitie):
        insert = "INSERT INTO entitie VALUES('" + entitite[0] + "','" + entitite[1] + '","' + entitite[2]+ "','" + entitite[3] +"','" + entitite[1] +"')"
        self.c.execute(insert)
        self.connection.commit()
    def insertRelation(self,relation):
        insert = "INSERT INTO relation VALUES('" + relation[0] + "','" + relation[1] + "')"
        print(insert)
        self.c.execute(insert)
        self.connection.commit()

