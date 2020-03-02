import nltk
from nlp import lexical
from nlp import morphosyntax

class QuestionProcessing(object):
    """docstring for QuestionProcessing"""
    def __init__(self, arg):
        self.normalizer = lexical.Preprocessing():
        self.morpho = morphosyntax.morpho()
    def processar(question):
        question = self.normalizar(question)
        doc = []
        doc = self.morpho.tag(question[0])
        #consulta = {'entidade': [], 'propriedade':[], 'indPergunta':[]}
        consulta = self.extrair(doc)
        
        return consulta

    def normalizar(question):
        line = self.normalizer.lowercase(question)
        line = self.normalizer.tokenize_sentences(line)
        return line

    # Extrair elementos principais da pergunta
    def extrairConsulta(doc):
        query = []
        for question in docs:
        query = []
        #para cada tupla 
        entidade = self.getEntidade(doc)
        if entidade == []:
            questionsNotEntitie.append(question)
        property = self.getProperty(question)
        ind = self.getINI(question)
        #print(ind, property, entidade, '\n')
        query = {'indPergunta':ini, 'propriedade': property, 'entidade': entidade}
        return query
    # Extrair entidade
    def getEntidade(question):
        propn = []
        for tupla in question:
            if tupla[2] == 'PROPN':
                propn.append(tupla[1])
        if propn == []:
            print('entrou B')
            for tupla in question:
                if tupla[6] == 'B':
                    propn.append(tupla[1])
        if propn == []:
            print('entrou', question)
            for tupla in question:
                if tupla[4] == "ROOT":
                    print('entrou', tupla[0])
                    propn.append(tupla[1])
        return propn
    # Extrair propriedade/verbo
    def getProperty(question):
        props = []
        for tupla in question:
            if tupla[2] == 'VERB' or tupla[2] == "NOUN":
                props.append(tupla[1])
        return props
    # Extrair tipo da pergunta
    def getINI(question):
        ini = []
        for tupla in question:
            if tupla[2] == 'SCONJ' or tupla[2] == 'PRON' or tupla[2] == 'ADV' or tupla[2] == "ADP" or tupla[2]=='X':
                ini.append(tupla[1])
        return ini