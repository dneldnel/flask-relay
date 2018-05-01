from flask import Flask, render_template
from flask import jsonify
import os

app = Flask(__name__, static_folder='static', static_url_path='')


def getX10CurrentProfit():
        with open('revs.json','r',encoding='utf-8') as f:
            #f.write(json.dumps(revs))
            c = f.read()
            print c



@app.route('/')
def hello_world():
    return render_template('index.html')



@app.route('/api/x10currentprofit')
def x10CurrentProfit():
    getX10CurrentProfit()




if __name__ == '__main__':
    
    app.run(
        host='0.0.0.0',
        port=8081,
        debug=True
        )