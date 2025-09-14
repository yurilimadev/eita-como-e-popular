import requests
import json
import pandas as pd
import io 

#EXTRAÇÃO DE ESTIMATIVA POPULACIONAL PARA 2025
URL = 'https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2025/variaveis/9324?localidades=N1[all]|N6[all]'

response = requests.get(URL)

obj = response.json()

dados_json = json.dumps(obj[0]['resultados'][0]['series'])

string_io_obj = io.StringIO(dados_json)

string_io_obj.seek(0)

df_json = pd.read_json(string_io_obj)

dados_brasil = pd.concat([pd.json_normalize(df_json['localidade']), pd.json_normalize(df_json['serie'])], axis=1).iloc[:1,:]

df_merge = pd.concat([pd.json_normalize(df_json['localidade']), pd.json_normalize(df_json['serie'])], axis=1).iloc[1:, :] 

df_merge['2025'] = df_merge['2025'].astype(int)

padrao = r'(.*)\s-\s([A-Z][A-Z])'
df_merge[['cidade', 'estado']] = df_merge['nome'].str.extract(padrao)
df_merge.drop('nome', axis=1, inplace=True)

#importando csv de localizações

csv_loc_file = 'data/df_local.csv'

df_loc = pd.read_csv(csv_loc_file)

df_merge = pd.concat([df_merge, df_loc], axis=1)