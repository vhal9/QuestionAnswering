import nltk
from nlp import morphosyntax
from nltk.corpus import wordnet as wn

class QuestionProcessing(object):
    """docstring for QuestionProcessing"""
    def __init__(self):
        self.morpho = morphosyntax.Morpho()
        
    """Função principal que processa a pergunta e retorna suas partes principais para consulta na base de conhecimento""" 
    """Entrada: string com a pergunta"""
    """Saida: """

    def processar(self, question):
        #normalizar texto
        #processar morfologicamente o texto
        doc = self.morpho.tag(question)
        #query = {'entidade': [], 'propriedade':[], 'indPergunta':[], 'propriedadeOrigem':[]}
        query = self.extrairPalavrasChaves(doc)
        query['sinonimosPropriedade'] = []
        for propriedade in query['propriedade']:
            query['sinonimosPropriedade'].append(self.desambiguarPropriedade(propriedade))

        return query
    # Extrair elementos principais da pergunta
    """Entrada: doc"""
    """Saida: dicionario{
                entidade : []
                propriedade: []
                indPergunta:[]
                }
    """
    def extrairPalavrasChaves(self,doc):
        query = []
        entidade = self.getEntidade(doc)
        ind = self.getIND(doc)
        property = self.getProperty(doc)
        propertyOrigin = self.getPropertyOrigin(doc)
        """para cada tupla
        for tupla in doc: 
            entidade = self.getEntidade(doc)
            if entidade == []:
                questionsNotEntitie.append(question)
            property = self.getProperty(question)
            ind = self.getINI(question)
            #print(ind, property, entidade, '\n')
            query = {'indPergunta':ini, 'propriedade': property, 'entidade': entidade}
        """
        query = {'indPergunta':ind, 'propriedade': property, 'entidade': entidade, 'propriedadeOrigem':propertyOrigin}
        return query
    # Extrair entidade
    """Entrada: Doc"""
    """Saida: lista de string"""
    def getEntidade(self,question):
        propn = []
        for tupla in question:
            if tupla[2] == 'PROPN':
                propn.append(tupla[1])
        if propn == []:
            for tupla in question:
                if tupla[6] == 'B':
                    propn.append(tupla[1])
        if propn == []:
            for tupla in question:
                if tupla[4] == "ROOT":
                    propn.append(tupla[1])
        return propn
    # Extrair propriedade/verbo
    """Entrada: DOC"""
    """Saida: lista de string"""
    def getPropertyOrigin(self, question):
        props = []
        for tupla in question:
            if tupla[2] == 'VERB' or tupla[2] == "NOUN":
                props.append(tupla[0])
        return props
    def getProperty(self,question):
        props = []
        for tupla in question:
            if tupla[2] == 'VERB' or tupla[2] == "NOUN":
                props.append(tupla[1])
        return props
    """Extrair tipo da pergunta
       Entrada: Doc
       Saida: lista de string
    """
    def getIND(self,question):
        ini = []
        for tupla in question:
            if tupla[2] == 'SCONJ' or tupla[2] == 'PRON' or tupla[2] == 'ADV' or tupla[2] == "ADP" or tupla[2]=='X':
                ini.append(tupla[1])
        return ini
    """ Extrair lista de sinonimos utilizando o wordnet
        Entrada: string
        Saida: lista de string
    """
    def desambiguarPropriedade(self, palavra):
        synonyms = []
        for syn in wn.synsets(palavra, lang='por'):
            for l in syn.lemma_names('por'):
                synonyms.append(l)
        synonyms = self.preProcessarSinonimosWN(synonyms)
        return synonyms
    def preProcessarSinonimosWN(self, synonyms):
        #remover duplicatas
        sinonimos = []
        for sinonimo in synonyms:
            if sinonimo not in sinonimos:
                sinonimos.append(sinonimo)
        #trocar _ por ' '
        synonyms = []
        for sinonimo in sinonimos:
            synonyms.append(sinonimo.replace('_', ' '))
        return synonyms

    """
    def preprocessarTep2(self, line):
    lixos = '{}, <>1234567890\n'
    lista = []
    for elemento in line:
        for lixo in lixos:
            elemento = elemento.replace(lixo, '')
        lista.append(elemento)
    return lista

    def abrirArquivoTep2():
    """