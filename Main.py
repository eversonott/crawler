from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse


class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]

    def links(self,url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type') == 'text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return self.links
        else:
            return []

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type') == 'text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "", []


def spider(url, word, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited + 1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if data.find(word) > -1:
                foundWord = True
            pagesToVisit = pagesToVisit + links
            print(" **Sucess!**")
        except:
            print("Failed")
        if foundWord:
            print("The word", word, "was found at", url)
        else:
            print("Word never found")



def processa_pagina(lista):

    for x in range(0, len(lista)):
        parser = LinkParser()
        links = parser.links(lista[0])
        lista.extend(links)
        lista.remove(lista[0])

        print(len(lista))
        print(lista)
        #processa_pagina(lista)


#spider("https://www.google.com", "a", 4000)


end = "https://www.dreamhost.com"
lista = []
lista.append(end)

parser = LinkParser()
links = parser.links(lista[0])
lista.extend(links)
lista.remove(lista[0])
print(lista)
print(len(lista))

processa_pagina(lista)

print("depois do processo")
print(len(lista))
