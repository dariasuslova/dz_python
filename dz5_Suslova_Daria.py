import re

class Word:
    pass

def word(**values):
    result = Word()
    vars(result).update(values)
    return result
def add_to_arr(*arg, arr=[]):
    arr.append(arg)
    return arr



def find_lem(text):
    lem = re.findall(r'"lex":"([а-яё]*?)"', text, flags=re.DOTALL)
    d = {}
    for le in lem:
        if le in d:
            d[le]+=1
        else:
            d[le]=1
        return max(d)

def find_pos(text):
    p = re.findall(r',"gr":"([A-Z]+?).*?=', text, flags=re.DOTALL)
    d2 = {}
    for prt in p:
        if prt in d2:
            d2[prt]+=1
        else:
            d2[prt]=1
        return max(d2)

def find_slovo(text):
    sl = re.findall(r'"text":"((?:[А-ЯЁ]|[а-яё])[а-яё]*?)"', text, flags=re.DOTALL)
    if sl:
        for s in sl:
              return s
    
f = open('python_mystem.json', encoding = 'utf-8')
t = f.read()
res = re.findall(r'analysis(.*?)}\n', t, flags=re.DOTALL)

if res:
    for i in res:
        l = re.findall(r'lex', i, flags=re.DOTALL)
        k = 0
        if l:
            for j in l:
                k+=1
        sl = re.findall(r'"text":"((?:[А-ЯЁ]|[а-яё])[а-яё]*?)"', i, flags=re.DOTALL)
        if sl:
            for s in sl:
              sl2=s  
        lemm = find_lem(i)
        pr = find_pos(i)
        sl2 = find_slovo(i)    
        x = word(slovo=sl2, kolvo_razborov=k, lemma = lemm, pos = pr)
        a = add_to_arr(x)




    
