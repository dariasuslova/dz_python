import re
from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem

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
    for i in ana:
        result += i['text']
        if i['text'].strip() and 'analysis' in i and i['analysis']:
            pos = i['analysis'][0]['gr'].split('=')[0].split(',')[0]
            count+=1
            if pos == 'V':
                j+=1
            verb = i['analysis'][0]['gr'].split(',')
            for v in verb:
                if v == 'несов':
                    nesov+=1
                elif v == 'сов':
                    sov +=1
            ve = i['analysis'][0]['gr'].split(',')
            for ver in ve:
                res = re.search('пе=',ver)
                if res:
                    per+=1
                res2 = re.search('нп=',ver)
                if res2:
                    neper+=1
                
    part_verbs=count/j
    return 'количество глаголов:{}, доля глаголов в тексте:{}, количество несов вида:{}, количество сов вида:{}, количество переходных:{}, количество непереходных:{}'.format(j, part_verbs, nesov, sov, per, neper)
    


@app.route('/', methods=['get', 'post'])
def index():
    if request.form:
        text = request.form['text']
        result = add_POS(text)
        return render_template('index_page.html', input=text, text=result)
    return render_template('index_page.html')


if __name__ == '__main__':
    app.run(debug=True)
