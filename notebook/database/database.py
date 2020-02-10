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
    def getAllEntitie(self):
        consulta = "SELECT * FROM entitie "
        return self.getAccess(consulta)

    """consultar uma entidade"""
    def getEntitie(self, idEntidade):
        consulta = "SELECT * FROM entitie WHERE entitie.idEnt = '"+ idEntidade + "'"
        return self.getAccess(consulta)
    def getEntitieID(self, entidade):
        consulta = "SELECT idEnt FROM entitie WHERE entitie.name = '"+ entidade +"'"
        return self.getAccess(consulta)

    """consultar todas propriedades"""
    def getAllProperty(self):
        consulta = "SELECT * FROM property"
        return self.getAccess(consulta)

    """consultar uma propriedade"""
    def getProperty(self, idProp):
        consulta = "SELECT * FROM property P WHERE P.idProp = '"+idProp+"'"
        print(consulta)
        return self.getAccess(consulta)
    """consultar o id de uma propriedade"""
    def getPropertyID(self, prop):
        consulta = "SELECT idProp FROM property WHERE property.desc = '"+ prop +"'"
        print(consulta)
        return self.getAccess(consulta)

    """consultar todas relacoes"""
    def getAllRelation(self):
        consulta = "SELECT * FROM relation"
        return self.getAccess()
    """consultar relacoes retornando (nome Entidade 1, propriedade, nome Entidade 2)"""
    def getAllRelations(self):
        consulta = "SELECT E.name, P.desc, V.name  FROM ((entitie E INNER JOIN relation R ON E.idEnt = R.idEnt1) INNER JOIN property P ON R.idProp = P.idProp) INNER JOIN entitie V ON R.idEnt2 = V.idEnt"
        return self.getAccess(consulta)
    """consultar relacao por entidade"""
    def getRelation(self, idEntidade):
        consulta = "SELECT E.name, P.desc, R.name  FROM (entitie E LEFT JOIN relation R ON E.idEnt = R.idEnt1) LEFT JOIN property P ON R.idProp = P.idProp WHERE E.idEnt = '"+idEntidade+"'"
        return self.getAccess(consulta)
    """consultar entidades que foram trazidas em uma relacao e não foram mapeadas para a tabela entitie"""
    def getEntitiesNotMapped(self):
        consulta = "SELECT R.idEnt2 FROM relation R LEFT JOIN entitie E ON R.idEnt2 = E.idEnt WHERE E.idEnt IS NULL"
        return self.getAccess(consulta)
    """consultar uma entidade a partir de uma relacao com outra entidade e uma propriedade"""
    def getEntitieInRelation(self, idEntidade, idProperty):
        consulta = "SELECT E.name FROM (entitie E INNER JOIN relation R ON E.idEnt = R.idEnt2) WHERE R.idEnt1 = '"+idEntidade+"' AND R.idProp = '"+idProperty+"'"
        print(consulta)
        return self.getAccess(consulta)
############################################################################################################################## 
    """funcao responsavel por realizar uma consulta especificada ao banco de dados"""
    def getAccess(self, consulta):
        resposta = []
        try:
            resposta = self.c.execute(consulta)
            pass
        except Exception as e:
            reposta = e
        return resposta
##############################################################################################################################
    """Finalizar conexao"""
    def finalizarConnection(self):
        self.connection.close()
