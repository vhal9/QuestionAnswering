import spacy

class Syntax:

    def __init__(self, language="pt_core_news_sm"):
        self.nlp = spacy.load(language)

    def parse(self):
        pass
    
    def get_SVO(self, string):
        sujeitos = []
        for token in doc:
            if token.dep_ == 'nsubj': sujeitos.append(token)
        
        triple = []
        for suj in sujeitos:
            head = suj.head
            print(head.text)
            
            if head.pos_ == "VERB" and head.head.pos_ == "NOUN":
                triple.append((suj, head, head.head))
                
            elif head.pos_ in ["NOUN", "ADJ"]:
                for token in head.subtree:
                    if token.pos_ == "VERB" and token.head == head:
                        triple.append((suj, token, head))
                        break
        return triple