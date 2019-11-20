import requests
class Searching:
    """docstring for searching"""
    def __init__(self):
        self.api_end_point = 'https://www.wikidata.org/w/api.php'
    
    """função para retornar dados acerca de uma entidade, funcao wbseachentities"""
    """entrada: uma string"""
    """saida: uma lista de dicionarios (formato json)"""
    def entitie(self, query):
        parameters = {
            'action' : 'wbsearchentities',
            'format' : 'json',
            'language' : 'pt-br',
            'search' : query}
        return self.request(parameters)
    
    """função para retornar dados acerca de uma lista de entidades"""
    """entrada: uma lista de strings"""
    """saida: um dicionario com o resultado da consulta, em que para cada entidade se tem listas de 
    dicionarios (formato json)"""
    def entities(self, querys):
        data = {}
        for query in querys:
            data[query] = self.entitie(query)
        return data
    
    """funcao para retornar dados acerca de n entidades, funcao wbgetentities"""
    """entrada: ids, sites, titles"""
    def getEntitie(self, ids, sites, titles):
        action = 'wbgetentities'
        parameters = {
            'action': 'wbgetentities',
            'format': 'json',
            'language': 'pt-br',
            'sites': sites,
            'titles': titles,
            'ids': ids}
        return self.request(parameters)
    
    """funcao para realizar a requisicao na api"""
    """entrada: lista de parametros"""
    """saida: uma lista de dicionario com as informacoes da entidade (formato json)"""
    def request(self, parameters):
        try:
            return requests.get(self.api_end_point, params = parameters)
            pass
        except Exception as e:
            return []