import requests
from lxml import etree
from lxml import html

class Professor:
    def __init__(self, name, number, position):
        self.name = name 
        self.number = number
        self.position = position
        
    def __repr__(self):
        return '({},{},{})'.format(self.name, self.number, self.position)

    #def teachers_with_etree(self, page)

    def teachers_with_xpath(self):
        pg = requests.get('https://www.hse.ru/org/persons/?ltr=%D0%A1;udept=22726')
        tree = html.fromstring(pg.content)
        names = tree.xpath('//a[@class="link link_dark large b"]/text()')
        numbers = tree.xpath('//div[@class="l-extra small"]/span/text()')
        positions = tree.xpath('//p[@class="with-indent7"]/span/text()')
        

        prof = []
        for name, number, position in zip(names, numbers, positions):
            professor = Professor(name.strip(), number, position.strip())
            prof.append(professor)

        return prof

p = Professor('','','')
res = p.teachers_with_xpath()
print (res)


#page = requests.get('https://www.hse.ru/org/persons/?ltr=%D0%A1;udept=22726')
#root = etree.HTML(page.content)
#posts = root[1][0][3][1][1][0][2][1][1][1][0][1][0]
#print(posts.attrib)
