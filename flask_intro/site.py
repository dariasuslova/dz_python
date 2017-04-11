import datetime

from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    urls = {'форма про животных': url_for('form'),
            'ответы': url_for('result'),}
    return render_template('index.html', urls=urls)

fw = open('data.txt', 'a', encoding='utf-8')
@app.route('/form')
def form():
    if request.args:
        name = request.args['name']
        dog = True if 'dog' in request.args else False
        cat = True if 'cat' in request.args else False
        fw.write(name + ',' + str(dog) + ',' + str(cat) + '\n')
        return redirect(url_for('result', name=name, dog=dog, cat=cat))
    return render_template('question.html')
    #fw.close()

@app.route('/result')
def result():
    ca=0
    do=0
    arr=[]
    schet=0
    if request.args:
        name = request.args['name']
        dog = request.args['dog']
        cat = request.args['cat']
        f = open('data.txt', 'r', encoding='utf-8')
        s = f.read()
        a = s.split('\n')
        for i in a:
            n = i.split(',')
            if n[0] != '':
                arr.append(n[0])
                if n[1] == 'True':
                        do+=1
                elif n[2] == 'True':
                        ca+=1
                    
        return render_template('result.html', name=name, dog=dog, cat=cat, arr=arr, do=do,ca=ca)
        f.close()

if __name__ == '__main__':
    app.run(debug=True)
