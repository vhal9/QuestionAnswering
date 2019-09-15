import spacy

class Preprocessing:
   
    #contrutor da classe, recebe a língua para ser trabalhada como parametro e atribui para uso do spacy
    def __init__(self, language='../models/pt_core_news_sm-2.1.0'):
        self.nlp = spacy.load(language)
    
    #a função parse recebe uma sentença e para cada palavra da sentenca é salvo uma tripla contendo (palavra, papel sintatico, objeto para o qual referencia (head)) e retorna uma lista de triplas das palavras da sentenca
    def parse(self, sentence):
        #recebe uma sentenca e transforma em objeto doc
        doc = self.nlp(sentence)
        
        #lista que irá conter uma tripla contendo (palavra, papel sintatico, head) para cada palavra da sentenca
        s_tags = []
        for token in doc:
            #(palavra, papel_sintático, head)
            s_tags.append((token.text, token.dep_, token.head))
        return s_tags
    
    #a função get_SVO returnetorna uma lista de triplas (sujeito, verbo, objeto).    
    def get_SVO(self, sentence):
        #recebe uma sentenca e transforma em objeto doc
        doc = self.nlp(sentence)
        
        #cria uma lista sujeito e percorre a sentenca armazenando na lista todos os sujeitos identificados pela tag 'nsubj'
        #extrai todos os sujeitos em sentenca
        sujeitos = [token for token in doc if token.dep_ in ['nsubj']]
        #print(sujeitos)
        
        #cria uma lista svo (sujeito, verbo, objeto)
        svo = []
        #para cada sujeito da lista verifica qual verbo o modifica e qual objeto é referenciado
        #extrai, para cada sujeito, o verbo e o objeto.
        for suj in sujeitos:
            #armazena o HEAD do sujeito
            cab = suj.head
            
            #se a etiqueta morfossintatica do head é um verbo e sua head é um substativo
            if cab.pos_ == "VERB" and cab.head.pos_ == "NOUN":
                aux = [t for t in cab.subtree if t.dep_ in ['obj', 'amod', 'obl', 'nummod']]
                #adiciona a lista a tupla de (sujeito, o verbo que é tbm o head do sujeito, head do verbo, que é o objeto)
                if len(aux) == 0:
                    svo.append((suj, cab,None))
                else:
                    svo.append((suj, cab,aux[0]))
            #caso a etiqueta morfossintatica do head seja um substantivo ou um adjetivo
            elif cab.pos_ in ["NOUN", "ADJ"]:
                #percorre a primeira subarvore do head do sujeito
                aux = [t for t in cab.subtree if t.dep_ in ['cop']]
                if len(aux) == 0:
                    svo.append((suj, None, cab))
                else:
                    svo.append((suj, aux[0], cab))
            else:
                #print([t.text for t in cab.subtree], '\n\n')
                aux = [t for t in cab.subtree if t.dep_ in ['obj', 'amod', 'obl', 'nummod']]
                if len(aux) == 0:
                    svo.append((suj, cab,None))
                else:
                    svo.append((suj, cab,aux[0]))
        
        #retorna a lista de tuplas svo
        return svo