from data.extracao import df_merge
import pandas as pd
import time
import json
from dotenv import load_dotenv
import googlemaps
import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__),'..')))

#load env
load_dotenv()
c_map = os.getenv('API_KEY')
#print(df_merge[['cidade', 'estado']])

def get_geocode(chave: str, local: str):
    gmaps = googlemaps.Client(key=chave)
    
    try:
        busca_completa = f"{local}, Brazil"
        geocode_result = gmaps.geocode(busca_completa, components={'country':'BR'})
        if geocode_result:
            return geocode_result[0]['geometry']['location']
        else:
            print(f"Não encontrado para a busca: {local}")
            return None 
    except Exception as e:
        print(f"Não encontrado! {local}:{e}")
        return None

dict_local = {
    'latitude':[],
    'logitude':[]
}

for index, row in df_merge.iterrows():
    localizacao = f"{row['cidade']}, {row['estado']}"
    resposta = get_geocode(chave=c_map, local=localizacao)
    if resposta:
        dict_local['latitude'].append(resposta['lat'])
        dict_local['logitude'].append(resposta['lng'])
        print(f'Geocoding de {localizacao}: Extraído e add no dict: {resposta}')
    else:
        dict_local['latitude'].append(None)
        dict_local['logitude'].append(None)
    
#Cache agressivo    
df_local = pd.DataFrame(dict_local)
df_local.to_csv(
    'df_local.csv', 
    index=False)