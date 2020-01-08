import sqlite3

class Database:
    """docstring for Database"""
    def __init__(self):
        self.connection = sqlite3.connect('knowlegde.db')
        self.c = self.connection.cursor()
        self.createTables()
    """criar tabelas"""
    def createTables(self):
        createEntitie = "CREATE TABLE IF NOT EXISTS entitie(idEnt TEXT PRIMARY KEY NOT NULL, name TEXT, desc TEXT, pageid TEXT, url TEXT)"
        createProperty = "CREATE TABLE IF NOT EXISTS property(idProp TEXT PRIMARY KEY NOT NULL, desc TEXT)"
        createRelation = "CREATE TABLE IF NOT EXISTS relation(idEnt1 TEXT, idEnt2 TEXT, idProp TEXT, PRIMARY KEY(idEnt1, idEnt2, idProp), FOREIGN KEY(idProp) REFERENCES property(idProp), FOREIGN KEY(idEnt1) REFERENCES entitie(idEnt), FOREIGN KEY (idEnt2) REFERENCES entitie(idEnt))"
        try:
            self.c.execute(createEntitie)
            self.c.execute(createProperty)
            self.c.execute(createRelation)
            self.connection.commit()
            pass
        except Exception as e:
            print('erro')

############################################################################################################################
    """Bloco de insercoes"""

    """inserir entidade:""" 
    """entrada: dicionario do tipo: {'id':'', 'name':'', 'desc':'', 'pageid':'', 'url':''} """
    def insertEntitie(self, entitie):
        try:
            insert = "INSERT INTO entitie VALUES('" + entitie['id'] + "','" + entitie['name'] + "','" + entitie['desc']+ "','" + entitie['pageid'] +"','" + entitie['url'] +"')"
            pass
        except Exception as e:
            print('erro no dicionario de entrada')
        try:
            self.c.execute(insert)
            self.connection.commit()
            pass
        except Exception as e:
            print('Não foi possivel inserir', e)
    """inserir propriedade:"""
    """entrada: lista: [ID, desc]"""
    def insertProperty(self,propertys):
        try:
            insert = "INSERT INTO property VALUES('" + propertys[0] + "','" + propertys[1] + "')" 
            pass
        except Exception as e:
            print('erro na lista de entrada')
        try:
            self.c.execute(insert)
            pass
        except Exception as e:
            print('Não foi possivel inserir', e)
        
        self.connection.commit()

    """inserir relacao"""
    """entrada: lista: [ID ENTIDADE 1, ID ENTIDADE 2, ID PROPRIEDADE]"""
    def insertRelation(self, relation):
        try:
            insert = "INSERT INTO relation VALUES('"+ relation[0] + "','" + relation[1] + "','" + relation[2] +"')"
            pass
        except Exception as e:
            print('erro na lista de entrada')
        try:
            self.c.execute(insert)
            self.connection.commit()
            pass
        except Exception as e:
            print('Não foi possivel inserir', e)
        
#############################################################################################################################
    
    """Bloco de consultas"""

    """consultar todas entidades"""
    def consultarAllEntitie(self):
        consulta = "SELECT * FROM entitie "
        return self.c.execute(consulta)

    """consultar uma entidade"""
    def consultarEntidade(self, idEntidade):
        consulta = "SELECT * FROM entitie WHERE entitie.idEnt = '"+ idEntidade + "'"
        return self.c.execute(consulta)

    """consultar todas propriedades"""
    def consultarAllProperty(self):
        consulta = "SELECT * FROM property"
        return self.c.execute(consulta)

    """consultar uma propriedade"""
    def consultarProperty(self, idProp):
        consulta = "SELECT * FROM property P WHERE P.idProp = '"+idProp+"'"
        return self.c.execute(consulta)

    """consultar todas relacoes"""
    def consultarAllRelation(self):
        consulta = "SELECT * FROM relation"
        return self.c.execute(consulta)
    """consultar relacao por entidade"""
    def consultarRelations(self, idEntidade):
        consulta = "SELECT E.name, P.desc, R.idEnt2  FROM (entitie E LEFT JOIN relation R ON E.idEnt = R.idEnt1) LEFT JOIN property P ON R.idProp = P.idProp WHERE E.idEnt = '"+idEntidade+"'"
        try:
            resposta = self.c.execute(consulta)
            pass
        except Exception as e:
            reposta = 'erro'
        return resposta

    def finalizarConnection(self):
        self.connection.close()
