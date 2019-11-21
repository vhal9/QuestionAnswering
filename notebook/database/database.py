import sqlite3

class Database:
    """docstring for Database"""
    def __init__(self):
        self.connection = sqlite3.connect('knowlegde.db')
        self.c = self.connection.cursor()
        self.createTables()
    def createTables(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS entitie(id TEXT PRIMARY KEY NOT NULL, name TEXT, desc TEXT, pageid TEXT, url TEXT)')
        self.c.execute('CREATE TABLE IF NOT EXISTS property(id TEXT PRIMARY KEY NOT NULL, desc TEXT)')
        self.connection.commit()
    '''entrada: dicionario do tipo: {'id':'', 'name':'', 'desc':'', 'pageid':'', 'url':''} '''
    def insertEntitie(self, entitie):
        insert = "INSERT INTO entitie VALUES('" + entitie['id'] + "','" + entitie['name'] + "','" + entitie['desc']+ "','" + entitie['pageid'] +"','" + entitie['url'] +"')"
        try:
            self.c.execute(insert)
            self.connection.commit()
            pass
        except Exception as e:
            insert = "erro"
        
    def insertProperty(self,propertys):
        '''ID, Desc '''
        insert = "INSERT INTO property VALUES('" + propertys[0] + "','" + propertys[1] + "')"
        print(insert)
        self.c.execute(insert)
        self.connection.commit()
        '''pass
        except Exception as e:
            insert = "erro"
            print(insert)'''
    def consultarEntitie(self):
        consulta = "SELECT * FROM entitie "
        return self.c.execute(consulta)
    def consultarProperty(self):
        consulta = "SELECT * FROM property"
        return self.c.execute(consulta)
    def finalizarConnection(self):
        self.connection.close()
