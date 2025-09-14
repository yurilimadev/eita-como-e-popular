#BIBLIOTECAS IMPORTADAS
import time
import branca
import streamlit as st
import plotly.express as px
from data.extracao import df_merge
import folium
from streamlit_folium import st_folium
import base64

#INICIANDO O APP
def main():
    
    #CRIANDO VARIAVEL PARA CONTROLE DE SESSÂO
    if 'mostra_resultados' not in st.session_state:
        st.session_state.mostra_resultados = False

    #SESSÃO HEADER COM LOGO
    st.image('/home/dimit/projeto-flask/assets/photo_2025-09-09_15-50-45.jpg',)
    st.subheader('Saiba quantas cidades tem no seu instagram!')
    st.text('Obs: Pode comparar com qualquer rede social! Qualquer uma que tem seguidores!')
    st.warning('Dados de população são relativos as estimativas populacionais do IBGE')

    #SESSÃO SIDEBAR
    st.sidebar.text('👨‍💻 ☕ Me pague um café!')
    st.sidebar.image('/home/dimit/projeto-flask/assets/qrcode-pix-buy-a-coffe.png')
    
    
    #SESSÃO DE INTERAÇÃO COM USUÁRIO
    with st.form(key='form1'):
        numero_seguidores = st.number_input('Numero de seguidores', min_value=0, step=1, key='numero_seguidores')
        with st.container(horizontal=True, horizontal_alignment='left'):
            submit_button = st.form_submit_button(label='Comparar')
            submit_restaurar = st.form_submit_button(label='Restaurar')

    #BOTÃO QUE INICIA A LÓGICA     
    if submit_button:
        ## TROCA VALOR DA VARIAVEL DE CONTROLE PARA TRUE
        st.session_state.mostra_resultados = True
        ## CRIA VARIAVEL NUMERO DE SEGUIDORES E CHECA SE VARIAVEL DE CONTROLE É TRUE
        if 'numero_seguidores' not in st.session_state and st.session_state.mostra_resultados:
            st.session_state.numero_de_seguidores = numero_seguidores
        
        st.subheader('Resultados')
        st.toast(f'Carregando...', icon='🚀')

    #BOTÃO QUE RESTAURA A SESSÃO
    if submit_restaurar:
        st.session_state.mostra_resultados = False
        st.session_state.numero_de_seguidores = 0
        

    #CHECANDO SE VARIAVEL 'MOSTRA RESULTADOS' FOI CRIADA 
    if st.session_state.mostra_resultados:
        ## CHECA SE VARIAVEL DE SESSÃO NUMERO DE SEGUIDORES FOI CRIADA
        if 'numero_de_seguidores' in st.session_state:
            
            if numero_seguidores >= df_merge['2025'].min():
                #FILTRAGEM
                df_filtrado = df_merge[df_merge['2025'] <= numero_seguidores].sort_values(by='2025', ascending=False)

                #COMEÇA A SESSÃO LÓGICA 1 
                col1, col2 = st.columns(
                    2, 
                    vertical_alignment='center'
                )
                with col1:
                    df_top10 = df_filtrado.iloc[0:11,:]
                    st.dataframe(df_top10[['cidade', 'estado','2025']].set_index('cidade'))
                with col2:
                    st.image('/home/dimit/projeto-flask/assets/TOMA ESSA!.png',width='stretch')
                
                st.subheader('Veja onde fica no mapa! ')
                #st.write(df_filtrado.head(10))
                

                #COMEÇA A SESSÃO 2
                ## MAPA
                ### CRIANDO SESSÃO -:> AS KEYS TEM QUE TER O MESMO NO DA SESSÂO QUE VÃO INTERAGIR
                if 'top10_cidades' not in st.session_state:
                    st.session_state['top10_cidades'] = df_top10['cidade'].iloc[0] #(primeira opção do top 10)

                top10_cidades = st.selectbox(
                    'Cidades', 
                    options=df_top10['cidade'],
                    key='top10_cidades')
                print(st.session_state['top10_cidades'])

                #ACESSANDO E CRIANDO A VARIAVEL
                cidade = st.session_state.top10_cidades
                
                filtro_lat_lng = df_top10[df_top10['cidade'] == cidade]
                if not filtro_lat_lng.empty:
                    latitude_atual = filtro_lat_lng['latitude'].iloc[0]
                    longitude_atual = filtro_lat_lng['longitude'].iloc[0]

                    mapa_cidade = folium.Map(
                        location=(latitude_atual, longitude_atual),
                        scale=True,
                        zoom_start=10,
                    )

                    caminho_imagem = "/home/dimit/projeto-flask/assets/photo_2025-09-10_23-31-32-removebg-preview.png"
                    with open(caminho_imagem, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    #print(encoded_string)
                    html = f"""
                    <h3>Ajude a melhorar a localização nas cidades!</h3>
                    <a href=#>Link do repositório</a>
                    <img src="data:image/png;base64,{encoded_string}" width="100%" alt="" srcset="">
                    """
                    iframe = branca.element.IFrame(html=html, width=200, height=400)
                    angle = 90
                    icon = folium.Icon(angle=angle)
                    popup = folium.Popup(iframe, max_width=500)
                    folium.Marker(
                        location=[latitude_atual, longitude_atual],
                        popup=popup,
                        icon=icon,
                        tooltip=f"{top10_cidades}"
                    ).add_to(mapa_cidade)
                    
                    
                    st_folium(mapa_cidade, width='stretch')
            else:
                
                col1_rodape, col2_rodape, col3_rodape = st.columns([1, 2, 1])
                with col2_rodape:
                    st.image('/home/dimit/projeto-flask/assets/meme_pernalonga.jpg', )
    
        

# INICIA O APP
if __name__ == '__main__':
    main()