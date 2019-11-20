import sqlite3

class Database:
    """docstring for Database"""
    def __init__(self):
        self.connection = sqlite3.connect('knowlegde.db')
        self.c = self.connection.cursor()
        self.createTables()
    def createTables(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS entitie(id text, name text, desc text, pageid text, url text)')
        self.c.execute('CREATE TABLE IF NOT EXISTS property(id text, desc text)')
        self.connection.commit()
    '''entrada: dicionario do tipo: {'id':'', 'name':'', 'desc':'', 'pageid':'', 'url':''} '''
    def insertEntitie(self, entitie):
        insert = "INSERT INTO entitie VALUES('" + entitie['id'] + "','" + entitie['name'] + "','" + entitie['desc']+ "','" + entitie['pageid'] +"','" + entitie['url'] +"')"
        print(insert)
        self.c.execute(insert)
        self.connection.commit()
    def insertRelation(self,proprietys):
        '''ID, Desc '''
        insert = "INSERT INTO property VALUES('" + proprietys[0] + "','" + proprietys[1] + "')"
        print(insert)
        self.c.execute(insert)
        self.connection.commit()

