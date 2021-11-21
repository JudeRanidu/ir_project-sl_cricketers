from flask import Flask, render_template, request
from search import search
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def search_player():
    if request.method == 'POST':
        if request.form['query']:
            query = request.form['query']
            print(query)
        else:
            query = ''
        players = search(query)

        return render_template('index.html', players=players)
    else:
        return render_template('index.html', players='')


if __name__ == '__main__':
    app.run()
