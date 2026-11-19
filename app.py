#BIBLIOTECAS IMPORTADAS
import time
import os
from dotenv import load_dotenv
import branca
import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
import plotly.express as px
from data.extracao import df_merge
import base64
from assets.style import (
    carregar_css_pagina,
    carregar_html_header,
    carregar_html_popup,
    carregar_html_resumo,
    create_copy_button_html,
)

st.set_page_config(
    page_title="Eita, como é popular!",
    page_icon="🌎",
    layout="wide",
)
st.html(carregar_css_pagina())

#INICIANDO VARIAVEIS NECESSARIAS PARA A SESSAO
##CRIANDO VARIAVEL PARA CONTROLE DE SESSÂO
if 'mostra_resultados' not in st.session_state:
    st.session_state.mostra_resultados = False
if 'numero_seguidores' not in st.session_state:
    st.session_state.numero_seguidores = 0
load_dotenv(override=True)
PIX_KEY = os.environ.get("PIX_KEY") or os.environ.get("pix_key", "")
#INICIANDO O APP
def main():

    #SESSÃO SIDEBAR
    with st.sidebar:
        st.text('👨‍💻 ☕ Me pague um café!')
        st.image('assets/qrcode-pix-buy-a-coffe.png')

        if PIX_KEY:
            # CHAME A FUNÇÃO UMA ÚNICA VEZ AQUI
            texto_para_copiar = PIX_KEY
            components.html(create_copy_button_html(texto_para_copiar), height=100)
        else:
            st.error("Chave PIX não configurada")
            st.info("Configure a variável de ambiente PIX_KEY no Railway")

    #SESSÃO HEADER COM LOGO + SESSÃO DE INTERAÇÃO COM USUÁRIO (PAINEL HORIZONTAL)
    col_logo, col_interacao = st.columns([1, 2], vertical_alignment='center')
    with col_logo:
        st.image('assets/logo-eita-como-e-popular.jpg', width='stretch')
    with col_interacao:
        st.html(carregar_html_header())
        #print(st.session_state, "ANTES DO FORMULARIO")
        with st.form(key='form1'):
            numero_seguidores = st.number_input('Numero de seguidores', min_value=0, step=1)
            with st.container(horizontal=True, horizontal_alignment='left'):
                submit_button = st.form_submit_button(label='Comparar')
                submit_restaurar = st.form_submit_button(label='Restaurar')

    #BOTÃO QUE INICIA A LÓGICA     
    if submit_button:
        ## TROCA VALOR DA VARIAVEL DE CONTROLE PARA TRUE
        st.session_state.mostra_resultados = True
        st.session_state.numero_seguidores = numero_seguidores
        st.toast(f'Carregando...', icon='🚀')
        
    #print(st.session_state,"DEPOIS DO BOTAO SUBMIT")
    #BOTÃO QUE RESTAURA A SESSÃO
    if submit_restaurar:
        st.session_state.mostra_resultados = False
        st.session_state.numero_seguidores = 0
        

    #CHECANDO SE VARIAVEL 'MOSTRA RESULTADOS' FOI CRIADA 
    if st.session_state.mostra_resultados:
        ## CHECA SE VARIAVEL DE SESSÃO NUMERO DE SEGUIDORES FOI CRIADA
        st.divider()
            
        if numero_seguidores >= df_merge['2025'].min():
            #FILTRAGEM
            df_filtrado = df_merge[df_merge['2025'] <= numero_seguidores].sort_values(by='2025', ascending=False)
            df_top10 = df_filtrado.iloc[0:10,:]

            total_superadas = len(df_filtrado)
            percentual_superadas = (total_superadas / len(df_merge)) * 100
            maior_linha = df_top10.iloc[0]

            #COMEÇA A SESSÃO LÓGICA 1 E SESSÃO 2 LADO A LADO
            col_esquerda, col_direita = st.columns([1, 1], vertical_alignment='top')

            with col_esquerda:
                st.html(
                    carregar_html_resumo(
                        total_cidades=total_superadas,
                        percentual=percentual_superadas,
                        maior_cidade=maior_linha['cidade'],
                        maior_estado=maior_linha['estado'],
                        maior_populacao=maior_linha['2025'],
                    )
                )
                col_tabela, col_mascote = st.columns([3, 2], vertical_alignment='center')
                with col_tabela:
                    st.dataframe(
                        df_top10[['cidade', 'estado', '2025']].set_index('cidade'),
                        width='stretch',
                        height=300,
                    )
                with col_mascote:
                    st.image('assets/mascote-sucesso.png', width='stretch')

            #COMEÇA A SESSÃO 2
            ## MAPA
            with col_direita:
                cidade = st.selectbox(
                    'Veja onde fica no mapa:', 
                    options=df_top10['cidade'])
                
                filtro_lat_lng = df_top10[df_top10['cidade'] == cidade]
                
                if not filtro_lat_lng.empty:
                    latitude_atual = filtro_lat_lng['latitude'].iloc[0]
                    longitude_atual = filtro_lat_lng['longitude'].iloc[0]

                    mapa_cidade = folium.Map(
                        location=(latitude_atual, longitude_atual),
                        scale=True,
                        zoom_start=10,
                    )

                    caminho_imagem = "assets/mascote-mapa.png"
                    with open(caminho_imagem, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    
                    html = carregar_html_popup(
                        encoded_string=encoded_string,
                        repo_url="https://github.com/yurilimadev/eita-como-e-popular"
                    )
                    
                    iframe = branca.element.IFrame(html=html, width=250, height=290)
                    angle = 90
                    icon = folium.Icon(angle=angle)
                    popup = folium.Popup(iframe, max_width=270)
                    folium.Marker(
                        location=[latitude_atual, longitude_atual],
                        popup=popup,
                        icon=icon,
                        tooltip=f"{cidade}"
                    ).add_to(mapa_cidade)
                    
                    components.html(mapa_cidade.get_root().render(), height=380)
        else:
            col1_rodape, col2_rodape, col3_rodape = st.columns([1, 1, 1])
            with col2_rodape:
                st.image('assets/mascote-poucos-seguidores.png', width='stretch')

 

# INICIA O APP
if __name__ == '__main__':
    main()