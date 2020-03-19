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
    def buscarValor(self, idEntidade, idPropriedade):
        #print("buscando a entidade resposta ...")
        respostas = []
        for id in idEntidade:
            for idP in idPropriedade:
                print('buscando',id, idP)
                resultado = self.db.getValorInRelation(id, idP)
                for tupla in resultado:
                    for string in tupla:
                        respostas.append(string)
        return respostas
    '''Funcao para verificar se ha correspondencia entre um id Entidade com o banco de dados
       Entrada: string
       saida: booleano
    '''
    def verificarIdEntidade(self, idEntidade):
        entidade = self.db.getEntitie(idEntidade)
        correspondencia = 0
        for ent in entidade:
            correspondencia +=1
        if correspondencia > 0:
            return True
        else:
            return False
    '''
    Funcao para buscar o nome de uma entidade no banco de dados a partir do id da entidade
    Entrada: string
    Saida: string
    '''
    def buscarNomeEntidade(self,idEntidade):
        nome = ''
        if(not self.verificarIdEntidade(idEntidade)):
            nome = self.baixarNomeEntidade(idEntidade)
        else:
            nome = self.db.getNomeEntidade(idEntidade)
        return nome
    '''
    Funcao para baixar o nome de uma entidade a partir do id da entidade
    Entrada: string
    Saida: String
    '''
    def baixarNomeEntidade(self,idEntidade):
        dados = self.api.entitie(idEntidade).json()['search']
        '''para consultar a entidade necessita do link e do Qid'''
        site = dados[0]['concepturi']
        id = dados[0]['id']
        title = dados[0]['title']
        #print("entidade encontrada:")
        #print(id, title, site)
        dataEntitie = self.api.getEntitie(id, site, title).json()['entities']
        #print("extraindo informações...")
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
        #print("entidade encontrada:")
        #print(id, title, site)
        dataEntitie = self.api.getEntitie(id, site, title).json()['entities']
        #print("extraindo informações...")
        dadosEntidade = self.extrairInformacaoDaEntidade(dataEntitie, dados)
        #dadosPropriedads
        dadosPropriedades = self.extrairPropriedadesDaEntidade(dataEntitie)
        #print("inserindo no banco de dados...")
        #print(dadosEntidade)
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
            [propriedade1, [valor, tipo]]
    '''
    def extrairPropriedadesDaEntidade(self, dataEntitie):
        relacoes = []
        qId = None
        for key in dataEntitie:
            qId = key
        for propriedade in dataEntitie[qId]['claims']:
            quantPropriedades = len(dataEntitie[qId]['claims'][propriedade])
            for valor in range(0,quantPropriedades):
                #coordenada global
                conteudo = ''
                if dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datatype'] == 'globe-coordinate':
                    conteudo += str(dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datavalue']['value']['latitude'])
                    conteudo += str(dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datavalue']['value']['longitude'])
                else:
                    #id externo
                    if dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datatype'] == 'external-id':
                        conteudo = dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datavalue']['value']
                    else:
                        #wikidata item
                        if dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datatype'] == 'wikibase-item':
                            conteudo = dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datavalue']['value']['id']
                        else:
                            if dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datatype'] == 'time':
                                conteudo = dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datavalue']['value']['time']
                            else:
                                if dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datatype'] == 'quantity':
                                    conteudo = dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datavalue']['value']['amount']
                                else:
                                    if dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datatype'] in ['string', 'url', 'commonsMedia', 'geo-shape']:
                                        conteudo = dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datavalue']['value']
                                    else:
                                        if dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datatype'] == 'monolingualtext':
                                            conteudo = dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datavalue']['value']['text']
                                        else:
                                            conteudo = 'desconhecido'
                tipo = dataEntitie[qId]['claims'][propriedade][valor]['mainsnak']['datatype']
                relacoes.append([propriedade, [conteudo, tipo]])
        return relacoes

    '''Metodo para salvar os dados baixados na wikidata, salvando a entidade e as relacoes a ela'''
    '''Entrada:  dicionario com informacoes sobre a entidade e dicionario com as relacoes sobre a entidade'''
    def inserirDados(self, entidade, relacoes):
        #inserir entidade
        self.db.insertEntitie(entidade)
        #inserir relacoes
        for relacao in relacoes:
            propriedade = relacao[0]
            valor = relacao[1]
            if valor != 'desconhecido':
                relation = [entidade['id'], valor[0], propriedade]
                self.db.insertValue(valor)
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
    '''Funcao para retornar possiveis respostas'''
    '''entrada = dados {'entidade': [], propriedade:[], indPergunta:[], sinonimosPropriedade:[[]]}'''
    '''saida = '''
    def buscar(self, dados):
        entidade = ''
        for ent in dados['entidade']:
            entidade += ent
        consulta = {}
        consulta['entidade'] = entidade
        respostas = []
        for listaSinonimos in dados['sinonimosPropriedade']:
            for sinonimo in listaSinonimos:
                consulta['propriedade'] = sinonimo
                resposta = [consulta['entidade'], consulta['propriedade'], self.buscarInformacao(consulta)]
                respostas.append(resposta)
        return respostas
    '''Funcao para retornar entidades como resposta a consultas do tipo entidade(propriedade, X)'''
    '''entrada = dados = {'entidade': ' ', propriedade' '}'''
    '''saida = '''
    def buscarInformacao(self, dados):
        resposta = []
        # verificar se ha correspondencia da entidade no banco de dados
        #print("verificando se há correspondencia da entidade na Base de Dados...")
        if (not self.verificarEntidade(dados['entidade'])):
            #print("entidade não encontrada \nbuscando na wikidata")
            #se nao, baixar os dados da entidade e seus claims
            self.baixarInformacao(dados['entidade'])
        try:
            #print("buscando o id da entidade...")
            #buscar o id da entidade
            idEntidade = self.buscarIdEntidade(dados['entidade'])
            #print(idEntidade)
            #buscar o id da propriedade
            #print("buscando o id da propriedade...")
            idPropriedade = self.buscarIdPropriedade(dados['propriedade'])
            #print(idPropriedade)
            # buscar entidade resposta
            #print("buscando relacao...")
            resposta = self.buscarValor(idEntidade, idPropriedade)
            pass
        except Exception as e:
            raise e
            print(e)
        return resposta
    '''destruct da classe, finalizando a conexao com o banco de dados'''
    def __del__(self):
        self.db.finalizarConnection()