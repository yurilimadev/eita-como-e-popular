# app.py
import base64

def carregar_html_popup(encoded_string, repo_url):
    # Lê o arquivo HTML
    with open('components/mapa_popup.html', 'r', encoding='utf-8') as file:
        html_template = file.read()
    
    # Substitui as variáveis no template
    html_final = html_template.replace('{encoded_string}', encoded_string)
    html_final = html_final.replace('{repo_url}', repo_url)
    
    return html_final