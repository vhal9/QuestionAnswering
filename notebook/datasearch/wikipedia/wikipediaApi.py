import wikipedia
class Wiki:
    def __init__(self):
        wikipedia.set_lang('pt')
    def search(self, query):
        lista = wikipedia.search(query, results=2, suggestion= False)
        print(lista)
        return self.getPage(lista[0])
    def getPage(self, title):
        page = wikipedia.page(title=title, pageid=None, auto_suggest=True, redirect=True, preload=False)
        return self.getContent(page)
    def getSummary(self, page):
        return page.getSummary
    def getText(self, page):
        return page.getSummary
    def getTitle(self, page):
        return page.title
    def getContent(self,page):
        return page.content