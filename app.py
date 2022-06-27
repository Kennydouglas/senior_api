import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

def buscar_ano(movieName):
  try:
    requestTotalPages = requests.get(f"https://jsonmock.hackerrank.com/api/movies/search/?Title={movieName}")
    datas = []
    #print(request.content)
    jsonFile = json.loads(requestTotalPages.content)
    totalPages = jsonFile['total_pages']
    for page in range(1,totalPages+1):
      request = requests.get(f"https://jsonmock.hackerrank.com/api/movies/search/?Title={movieName}&page={page}")
      jsonFile = json.loads(request.content)
      for idx, item in enumerate(jsonFile['data']):
        datas.append(jsonFile['data'][idx]['Year'])

    datasNaoRepetidas = list(set(datas))
    datasNaoRepetidas.sort()
    print(datasNaoRepetidas)
    return datasNaoRepetidas
  except:
    print('Erro buscar ano')

def buscar_filmes(anos):
  try:
    data = []
    for ano in anos:
      request = requests.get(f"https://jsonmock.hackerrank.com/api/movies/search/?Year={ano}")
      jsonFile = json.loads(request.content)
      totalMoviesByYear = jsonFile['total']
      item = {
        'Year:': ano,
        'Movies:': totalMoviesByYear,
      }
      data.append(item)             
      #data['Movies'] = totalMoviesByYear
    json_data = json.dumps(data)  
    print(json_data)
    return json_data
    #print(len(jsonFile['data']))
    #print(jsonFile['data'])
    
  except:
    print('Erro buscar filmes')

#@app.route('/api/v1/filmes')
@app.route('/api/movies', methods=['GET'])
def countDates():
  name = request.args.get('Title')
  anos = buscar_ano(name)
  result = buscar_filmes(anos)
  return result

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)