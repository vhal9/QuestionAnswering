import spacy

class Morpho:
    
    #contrutor da classe, recebe a língua para ser trabalhada como parametro e atribui para uso do spacy
    def __init__(self, language='../model/pt_core_news_sm-2.1.0'):
        self.nlp = spacy.load(language)
        
    #a funçao tag() recebe uma string e retorna uma lista de tuplas da string recebida contendo a (palavras, etiqueta morfossintatica da palavra)
    def tag(self, sentence):
        doc = self.nlp(sentence)
        
        #lista que que irá conter as tuplas de cada palavra da string
        ms_tags = []
        for token in doc:
            #é adicionado a lista ms_tags a tupla(palavra, etiqueta_morfossintática para cada palavra)
            ms_tags.append((token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.ent_type_, token.ent_iob_))
        #retorna a lista contendo uma tupla para cada palavra da string
        
        return ms_tags