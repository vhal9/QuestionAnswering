import QuestionProcessing
import RotinaBD

class Prif(object):
    """docstring for Prif"""
    def __init__(self):
        self.processamentoPergunta = QuestionProcessing.QuestionProcessing()
        self.buscarRespostas = RotinaBD.RotinaBD()
        
    def responder(self, pergunta):
        consulta = self.processamentoPergunta.processar(pergunta)
        respostas = self.buscarRespostas.buscar(consulta)
        return respostas