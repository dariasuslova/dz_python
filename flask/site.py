import re
from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
import json
import requests
from collections import Counter, defaultdict
import nltk
from nltk import word_tokenize
from nltk.collocations import *
from nltk.stem.snowball import SnowballStemmer


m = Mystem()
app = Flask(__name__)


def add_POS(text):
    result = ''
    ana = m.analyze(text)
    j=0
    count=0
    nesov=0
    sov=0
    per=0
    neper=0
    d = defaultdict(int)
    for i in ana:
        result += i['text']
        if i['text'].strip() and 'analysis' in i and i['analysis']:
            pos = i['analysis'][0]['gr'].split('=')[0].split(',')[0]
            count+=1
            d['все слова']+=1
            if pos == 'V':
                j+=1
                d['глаголы']+=1
            verb = i['analysis'][0]['gr'].split(',')
            for v in verb:
                if v == 'несов':
                    nesov+=1
                    d['несовершенный вид']+=1
                elif v == 'сов':
                    sov +=1
                    d['совершенный вид']+=1
            ve = i['analysis'][0]['gr'].split(',')
            for ver in ve:
                res = re.search('пе=',ver)
                if res:
                    per+=1
                    d['непереходные глаголы']+=1
                res2 = re.search('нп=',ver)
                if res2:
                    neper+=1
                    d['переходные глаголы']+=1

    part_verbs=count/j
    d['часть глаголов в тексте'] = part_verbs
    results = 'количество глаголов:{}, доля глаголов в тексте:{}, количество несов вида:{}, количество сов вида:{}, количество переходных:{}, количество непереходных:{}'.format(j, part_verbs, nesov, sov, per, neper)
    return results, d

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)


def count_followers(group):
    users = []
    j = 0

    result = vk_api('groups.getMembers', group_id=group)
    members_count = result['response']['count']
    users += result['response']["users"]

    while len(users) < members_count:
        result = vk_api('groups.getMembers', group_id=group, offset=len(users))
        users += result['response']["users"]

    for i in users:
        j +=1

    return j

def get_followers(group):
    users = []

    result = vk_api('groups.getMembers', group_id=group)
    members_count = result['response']['count']
    users += result['response']["users"]

    while len(users) < members_count:
        result = vk_api('groups.getMembers', group_id=group, offset=len(users))
        users += result['response']["users"]

    return users

def compare(group1, group2):
    us1 = get_followers(group1)
    us2 = get_followers(group2)
    common = []
    for i in us1:
        if i in us2:
            common.append(i)
    for i2 in us2:
        if i2 in us1:
            if i2 not in common:
                common.append(i2)

    return common

def cor(slovo):
    my_sent_tokenizer = nltk.RegexpTokenizer('[^.!?]+')
    my_corpus = nltk.corpus.PlaintextCorpusReader('/home/hsepython2017/mysite/corpora_songs', '.*\.txt', sent_tokenizer=my_sent_tokenizer)
    stemmer = SnowballStemmer("russian")
    sentenses=my_corpus.sents()
    res = ''
    res2 = ''
    for s in sentenses:
        if slovo in s:
            res +=str(s)+'\n'
        elif slovo in [stemmer.stem(t) for t in s]:
            res +=str(s)+'\n'
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(my_corpus.words())
    finder.apply_word_filter(lambda w: len(w) < 3 or re.search('[а-яё]+', w.lower()) is None)
    freqs = finder.ngram_fd
    for key, value in list(freqs.items()):
        if slovo in key:
            res2+=str(key)+'\n'
    return res, res2

@app.route('/corpora', methods=['get', 'post'])
def corpora():
    if request.form:
        slovo = request.form['slovo']
        results, results2 = cor(slovo)
        return render_template('corpora.html', slovo=slovo, results=results, results2=results2)
    return render_template('corpora.html')

@app.route('/verbs', methods=['get', 'post'])
def verbs():
    if request.form:
        text = request.form['text']
        results, d = add_POS(text)
        return render_template('mystem_page.html', input=text, text=results, data=d)
    return render_template('mystem_page.html', data={})

@app.route('/common', methods=['get', 'post'])
def common():
    if request.form:
        group_id1 = request.form['group_id1']
        group_id2 = request.form['group_id2']
        num1 = count_followers(group_id1)
        num2 = count_followers(group_id2)
        comm = len(compare(group_id1, group_id2))
        return render_template('common.html', **locals())
    return render_template('common.html')


@app.route('/', methods=['get'])
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
