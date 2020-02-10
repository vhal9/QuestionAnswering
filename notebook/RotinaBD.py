from datasearch import wikidata
from database import database   
class RotinaBD():
    """docstring for RotinaBD"""
    
    def __init__(self):
        self.db = database.Database()
        self.api = wikidata.searching.Searching()
    '''dados = {'entidade': ' ', property:' '}'''
    ''''''
    def buscarInformacao(self, dados):
        resposta = []
        # verificar se nao tem a entidade no banco de dados
        print("verificando se tem a entidade...")
        if (not self.verificarEntidade(dados['entidade'])):
            print("entidade não encontrada \n buscando na wikidata")
            #se nao, baixar os dados da entidade e seus claims
            self.baixarInformacao(dados['entidade'])
        try:
            print("buscando o id da entidade...")
            #buscar o id da entidade
            idEntidade = self.buscarIdEntidade(dados['entidade'])
            print(idEntidade)
            #buscar o id da propriedade
            print("buscando o id da propriedade...")
            idPropriedade = self.buscarIdPropriedade(dados['propriedade'])
            print(idPropriedade)
            # buscar entidade resposta
            print("buscando relacao...")
            resposta = self.buscarNoBD(idEntidade, idPropriedade)
            pass
        except Exception as e:
            raise e
            print(e)
        return resposta
    '''busca o id da entidade'''
    def buscarIdEntidade(self, entidade):
        resultado = self.db.getEntitieID(entidade)
        elemento = []
        for tupla in resultado:
            for string in tupla:
                elemento.append(string)
        return elemento
    '''busca o id da propriedade'''
    def buscarIdPropriedade(self, propriedade):
        resultado = self.db.getPropertyID(propriedade)
        elemento = []
        for tupla in resultado:
            for string in tupla:
                elemento.append(string)
        return elemento
    '''consultar no BD a(s) relacao(oes) com o id da entidade e da propriedade'''
    def buscarNoBD(self, idEntidade, idPropriedade):
        print("buscando a entidade resposta ...")
        resposta = []
        for id in idEntidade:
            for idP in idPropriedade:
                print('buscando',id, idP)
                resultado = self.db.getEntitieInRelation(id, idP)
                for tupla in resultado:
                    print("imprime tupla", tupla)
                    for string in tupla:
                        print('imprime string', string)
                        resposta.append(string)
        return resposta
    '''verifica se ha alguma entidade que corresponda a entidade procurada'''
    def verificarEntidade(self, entidade):
        consulta = self.db.getEntitieID(entidade)
        entidades = []
        for elemento in consulta:
            entidades.append(elemento)
        if entidades == []:
            return False
        return True
    '''busca na wikidata a entidade buscada e a salva no BD'''
    def baixarInformacao(self, entidade):
        dados = api.entitie(entidade).json()['search']
        '''para consultar a entidade necessita do link e do Qid'''
        site = dados[0]['concepturi']
        id = dados[0]['id']
        title = dados[0]['title']
        print("entidade encontrada:")
        print(id, title, site)
        dataEntitie = api.getEntitie(id, site, title).json()['entities']
        print("extraindo informações...")
        dadosEntidade = self.extrairInformacaoDaEntidade(dataEntitie, dados)
        dadosPropriedades = self.extrairPropriedadesDaEntidade(dataEntitie)
        print("inserindo no banco de dados...")
        print(dadosEntidade)
        self.inserirDados(dadosEntidade, dadosPropriedades)
    '''extrair informações do json da entidade recuperado na wikidata'''
    def extrairInformacaoDaEntidade(self, dataEntitie, dados):
        entidade = {'id':'', 'name':'', 'desc':'', 'pageid':'', 'url':''}
        '''get id'''
        id = [id  for id in dataEntitie]
        entidade['id'] = id[0]
        '''get name'''
        try:
            entidade['name'] = dataEntitie[id[0]]['labels']['pt-br']['value']
            pass
        except Exception as e:
            try:
                entidade['name'] = dataEntitie[id[0]]['labels']['pt']['value']
            except Exception as e:
                try:
                    entidade['name'] = dataEntitie[id[0]]['labels']['en']['value']
                    pass
                except Exception as e:
                    entidade['name'] = 'desconhecido'
        
        '''get pageid'''
        entidade['pageid'] = str(dataEntitie[id[0]]['pageid'])
        '''get url'''
        entidade['url'] = dados[0]['concepturi']
        '''get desc'''
        try:
            entidade['desc'] = dataEntitie[id[0]]['descriptions']['pt-br']['value']
            pass
        except Exception as e:
            try:
                entidade['desc'] = dataEntitie[id[0]]['descriptions']['pt']['value']
                pass
            except Exception as e:
                entidade['desc'] = dataEntitie[id[0]]['descriptions']['en']['value']
        return entidade
    '''extrair informações do json da propriedade recuperado na wikidata'''
    def extrairPropriedadesDaEntidade(self, dataEntitie):
        entidades = {}
        propriedades = {}
        qId = None
        for key in dataEntitie:
            qId = key
        for relacao in dataEntitie[qId]['claims']:
            relacoes.append(relacao)
            try:
                propriedades[relacao] = dataEntitie[qId]['claims'][relacao][0]['mainsnak']['datavalue']['value']['id']
                pass
            except Exception as e:
                propriedades[relacao] = 'desconhecido'
        entidades[qId] = propriedades
        return entidades
    def inserirDados(self, entidade, relation):
        self.db.insertEntitie(entitie)
        for entidade in entidades:
            for property in entidades[entidade]:
                relation = [entidade, entidades[entidade][property], property]
                print(relation)
                if entidades[entidade][property] != 'desconhecido':
                    self.db.insertRelation(relation)
    '''destruct da classe, finalizando a conexao com o banco de dados'''
    def __del__(self):
        self.db.finalizarConnection()