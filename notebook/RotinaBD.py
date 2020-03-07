from datasearch import wikidata
from database import database   
class RotinaBD():
    '''docstring for RotinaBD'''
    '''construtor da classe'''
    def __init__(self):
        #instancia o objeto da classe Database para acesso ao banco de dados
        self.db = database.Database()
        #instancia o objeto Searching para acesso acesso a wikidata
        self.api = wikidata.searching.Searching()
    
    '''Funcao para buscar id's associados a uma entidade de entrada'''
    '''Entrada: string'''
    '''saida: lista com os possiveis ids no formato string'''
    def buscarIdEntidade(self, entidade):
        #busca os ids da entidade no banco de dados
        resultado = self.db.getIdEntitie(entidade)
        #extrair os elementos do objeto do banco de dados retornado
        ids = self.extracaoDeStringDoObjetoDoBD(resultado)
        return ids
    '''Funcao para buscar os id's associados a uma propriedade de entrada'''
    '''Entrada: string'''
    '''Saida: lista com os possiveis ids no formato string'''
    def buscarIdPropriedade(self, propriedade):
        #busca os ids da propriedade no banco de dados
        resultado = self.db.getPropertyID(propriedade)
        ids = self.extracaoDeStringDoObjetoDoBD(resultado)
        return ids
    '''Funcao para extrair do banco de dado(s) as entidade(s) a partir do(s) id(s) da(s) entidade(s) e id(s) da(s) propriedade(s) consultando no BD a(s) relacao(oes) com o(s) id(s) da(s) entidade(s) e da(s) propriedade(s)'''
    '''Entrada: lista de idEntidade e lista idPropriedade, ambas em formato string'''
    '''Saida: lista de nomes no formato string'''
    def buscarNoBD(self, idEntidade, idPropriedade):
        print("buscando a entidade resposta ...")
        ids = []
        for id in idEntidade:
            for idP in idPropriedade:
                print('buscando',id, idP)
                resultado = self.db.getEntitieInRelation(id, idP)
                for tupla in resultado:
                    print("imprime tupla", tupla)
                    for string in tupla:
                        print('imprime string', string)
                        ids.append(string)
        resposta = []
        for id in ids:
            #verificar se a entidade esta mapeada
            nome = self.buscarNomeEntidade(id)
            resposta.append(nome)
        return resposta
    def verificarIdEntidade(self, idEntidade):
        entidade = self.db.getEntitie(idEntidade)
        correspondencia = 0
        for ent in entidade:
            correspondencia +=1
        if correspondencia > 0:
            return True
        else:
            return False
    def buscarNomeEntidade(self,idEntidade):
        nome = ''
        if(not self.verificarIdEntidade(idEntidade)):
            nome = self.baixarNomeEntidade(idEntidade)
        else:
            nome = self.db.getNomeEntidade(idEntidade)
        return nome
    def baixarNomeEntidade(self,idEntidade):
        dados = self.api.entitie(idEntidade).json()['search']
        '''para consultar a entidade necessita do link e do Qid'''
        site = dados[0]['concepturi']
        id = dados[0]['id']
        title = dados[0]['title']
        print("entidade encontrada:")
        print(id, title, site)
        dataEntitie = self.api.getEntitie(id, site, title).json()['entities']
        print("extraindo informações...")
        dadosEntidade = self.extrairInformacaoDaEntidade(dataEntitie, dados)
        return dadosEntidade['name']
    '''Funcao para verificar se ha alguma entidade no banco de dados associada a entidade buscada'''
    '''Entrada: entidade no formato string'''
    '''Saida: booleano'''
    def verificarEntidade(self, entidade):
        consulta = self.db.getIdEntitie(entidade)
        entidades = []
        for elemento in consulta:
            entidades.append(elemento)
        if entidades == []:
            return False
        return True
    
    '''Metodo para buscar na wikidata a entidade buscada e a salvar no BD'''
    '''Entrada: entidade no formato string'''
    def baixarInformacao(self, entidade):
        dados = self.api.entitie(entidade).json()['search']
        '''para consultar a entidade necessita do link e do Qid'''
        site = dados[0]['concepturi']
        id = dados[0]['id']
        title = dados[0]['title']
        print("entidade encontrada:")
        print(id, title, site)
        dataEntitie = self.api.getEntitie(id, site, title).json()['entities']
        print("extraindo informações...")
        dadosEntidade = self.extrairInformacaoDaEntidade(dataEntitie, dados)
        dadosPropriedades = self.extrairPropriedadesDaEntidade(dataEntitie)
        print("inserindo no banco de dados...")
        print(dadosEntidade)
        self.inserirDados(dadosEntidade, dadosPropriedades)
    '''Funcao para extrair informações do json da entidade recuperado na wikidata'''
    '''Entrada: dicionarios com dados sobre a entidade extraidas da wikidata'''
    '''Saida: dicionario com dados especificos da entidade para serem salvos no banco de dados'''
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
    
    '''Funcao para extrair informações sobre as propriedades do json das entidades buscadas na wikidata'''
    '''Entrada: dicionario com os dados extraidos sobre a entidade na wikidata'''
    '''Saida: dicionario com id da entidade e outro dicionario com as propriedades e entidades associadas do tipo: '''
    '''
        {entidade:
            {propriedade1: entidade1, propriedade2:entidade2, ...}
        }
    '''
    def extrairPropriedadesDaEntidade(self, dataEntitie):
        relacoes = {}
        propriedades = {}
        qId = None
        for key in dataEntitie:
            qId = key
        for relacao in dataEntitie[qId]['claims']:
            try:
                propriedades[relacao] = dataEntitie[qId]['claims'][relacao][0]['mainsnak']['datavalue']['value']['id']
                pass
            except Exception as e:
                propriedades[relacao] = 'desconhecido'
        relacoes[qId] = propriedades
        return relacoes

    '''Metodo para salvar os dados baixados na wikidata, salvando a entidade e as relacoes a ela'''
    '''Entrada: dicionrio com informacoes sobre a entidade e dicionario com as relacoes sobre a entidade'''
    def inserirDados(self, entidade, relacoes):
        #inserir entidade
        self.db.insertEntitie(entidade)
        #inserir relacoes
        for idEntidade in relacoes:
            for property in relacoes[idEntidade]:
                relation = [idEntidade, relacoes[idEntidade][property], property]
                print(relation)
                if relacoes[idEntidade][property] != 'desconhecido':
                    print('inserindo', relation)
                    self.db.insertRelation(relation)

    '''Funcao para extrair lista de informacoes de um objeto de retorno do banco de dados'''
    '''Entrada: objeto formato sql'''
    '''Saida: lista de strings'''
    def extracaoDeStringDoObjetoDoBD(self,objeto):
        informacoes = []
        for tupla in objeto:
            for string in tupla:
                informacoes.append(string)
        return informacoes
    '''Funcao para retornar entidades como resposta a consultas do tipo entidade(propriedade, X)'''
    '''entrada = dados = {'entidade': ' ', property:' '}'''
    '''saida = '''
    def buscarInformacao(self, dados):
        resposta = []
        # verificar se ha correspondencia da entidade no banco de dados
        print("verificando se há correspondencia da entidade na Base de Dados...")
        if (not self.verificarEntidade(dados['entidade'])):
            print("entidade não encontrada \nbuscando na wikidata")
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
    '''destruct da classe, finalizando a conexao com o banco de dados'''
    def __del__(self):
        self.db.finalizarConnection()