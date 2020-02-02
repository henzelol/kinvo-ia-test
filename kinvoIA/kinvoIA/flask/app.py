import flask
from flask import render_template, request, redirect, url_for


import spacy
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Carregando o idioma no NLP e 'path variables'
nlp = spacy.load('pt_core_news_sm')
file_name_titulo = 'titulo.txt'
file_name_noticiadata = 'noticiadata.txt'
print("Carregado as Variáveis")


@app.route('/loadData', methods=['GET','POST'])
def loadData():
    # criando arquivos .json separados dos dados brutos retirados do crawler.
    #Pelo menos eu prefiro trabalhar em arquivos separados, ou pelo menos, sempre ter eles em caso de necessidade.
    with open('noticias.txt') as json_file:
        dadosnoticias = json.load(json_file)
        for titulo in dadosnoticias['titulo']:
            with open('titulo.txt', 'w') as outfile:
                json.dump(dadosnoticias['titulo'], outfile, ensure_ascii=False, indent=4)
        for noticiadata in dadosnoticias['noticiadata']:
            with open('noticiadata.txt', 'w') as outfile:
                json.dump(dadosnoticias['noticiadata'], outfile, ensure_ascii=False, indent=4)
    print("Criado Dump archives")

    #Outra maneira de abrir e carregar os arquivos com os dados em arquivos separados. Não utilizei mais este método
    #pelo própio formato que me os arquviso vieram.
    #file_json_titulo = open(file_name_titulo).read()
    #file_json_noticiadata = open(file_name_noticiadata).read()

    #file_doc_titulo = nlp(file_json_titulo)
    #file_doc_noticiadata = nlp(file_json_noticiadata)

    #criando as variáveis utilizaveis para manipulação de dados
    titulos = [_ for _ in dadosnoticias['titulo']]
    noticiasdatas = [_ for _ in dadosnoticias['noticiadata']]
    #Print abaixo para teste dos dados
    #print("titulo:", titulos[1], " e noticia: ",noticiasdatas[1]) 

    #criação de uma variavel que será utilizada na iteração abaixo.
    entidades = {}
    entidades['entidades'] = []
    entidades['Data'] = []
    # Neste for abaixo, ele pecorre até o tamanho da variavel noticiasdatas, fazendo o sequinte teste : 

    for iteracao in range(len(noticiasdatas)):
        # Se o resto da divisão da variavel for diferente de zero(visto que as datas estão nas posições pares) :
        if iteracao % 2 != 0:
            #Nossa variavel 'noticialida' recebera a frase da posição de iteração será jogada no mlp para ser analisada
            noticialida = noticiasdatas[iteracao]
            noticiatratada = nlp(noticialida)
            #print(noticiatratada)
            

            #Neste comentário abaixo é uma linha de código que poderiamos utilizar para retirar Stop swords e pontuações
            #Porém, como as frases das notícias da B3 são pequenas, isso não será necessário.
            #noticiatratada = [token for token in noticiatratada if not token.is_stop and not token.is_punct]

            # itero por todas as entidades reconhecidas na frase analisada, adiciono numa variavel a : Entidade / label / Data e salvo o resultado num .Json
            for entidade in noticiatratada.ents:
                entidades['entidades'].append({
                    'entidade': entidade.text,
                    'Noticia Pertencente': iteracao,
                    'label': entidade.label_
                    })
                with open('EntidadesReconhecidas.txt', 'w') as arquivo:
                    json.dump(entidades, arquivo, ensure_ascii=False, indent=4)
        else:
            DataNoticia = noticiasdatas[iteracao]
            entidades['Data'].append({
                'Data da Noticia': DataNoticia,
                'Noticia Pertencente': iteracao+1
            })
    print("Processo Concluido")
    return render_template('index.html')


@app.route('/seeData', methods=['GET', 'POST'])
def seeData():
    with open('EntidadesReconhecidas.txt') as json_file:
        Entidades = json.load(json_file)

    return render_template('loadData.html',entidades = json.dumps(Entidades['entidades'], sort_keys = False, indent = 4), Datas = json.dumps(Entidades['Data'], sort_keys = False, indent = 4))

    

@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('index.html')

app.run()