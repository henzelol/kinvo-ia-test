import flask
from flask import render_template
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    with open('EntidadesReconhecidas.txt') as json_file:
        Entidades = json.load(json_file)
        #EntidadesReconhecidas = json.dumps(Entidades, sort_keys = False, indent = 4)
        #print(EntidadesReconhecidas)

    return render_template('index.html', Entidades = json.dumps(Entidades['entidades'], sort_keys = False, indent = 4), Datas = json.dumps(Entidades['Data'], sort_keys = False, indent = 4))

app.run()