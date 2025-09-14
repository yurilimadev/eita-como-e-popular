# app.py
import base64
import json

def carregar_html_popup(encoded_string, repo_url):
    # Lê o arquivo HTML
    with open('components/mapa_popup.html', 'r', encoding='utf-8') as file:
        html_template = file.read()
    
    # Substitui as variáveis no template
    html_final = html_template.replace('{encoded_string}', encoded_string)
    html_final = html_final.replace('{repo_url}', repo_url)
    
    return html_final

def create_copy_button_html(text_to_copy):
    """
    Cria e retorna o código HTML, CSS e JavaScript para um botão de copiar.
    Usa uma classe CSS e event delegation para evitar problemas com sanitização.
    """
    json_safe_text = json.dumps(text_to_copy)
    
    html_code = f'''
    <div class="copy-button-container">
        <button class="copy-button" data-text-to-copy='{json_safe_text}' style="
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: rgb(255, 255, 255);
            color: rgb(49, 51, 63);
            fill: rgb(49, 51, 63);
            border: 1px solid rgba(49, 51, 63, 0.2);
            padding: 0.25rem 0.75rem;
            position: relative;
            text-decoration: none;
            border-radius: 0.5rem;
            border-width: 1px;
            border-style: solid;
            border-image: initial;
            margin: 0px;
            line-height: 1.6;
            width: 100%;
            user-select: none;
            cursor: pointer;
        ">
            📋 Copiar PIX
        </button>
        <span class="copy-feedback" style="display: none; color: green; margin-left: 10px;">
            ✓ Copiado!
        </span>
    </div>

    <script>
    // Função para copiar texto para a área de transferência
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            console.log('Texto copiado com sucesso: ' + text);
        }}).catch(function(err) {{
            console.error('Erro ao copiar texto: ', err);
            // Fallback para método antigo
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {{
                document.execCommand('copy');
                console.log('Texto copiado com método fallback');
            }} catch (fallbackErr) {{
                console.error('Erro com método fallback: ', fallbackErr);
                alert('Falha ao copiar texto. Por favor, copie manualmente: ' + text);
            }}
            document.body.removeChild(textArea);
        }});
    }}

    // Event delegation para lidar com cliques nos botões de copiar
    document.addEventListener('click', function(event) {{
        if (event.target.matches('.copy-button')) {{
            const textToCopy = JSON.parse(event.target.getAttribute('data-text-to-copy'));
            
            // Copia o texto
            copyToClipboard(textToCopy);
            
            // Mostra feedback visual
            const feedbackElement = event.target.nextElementSibling;
            if (feedbackElement && feedbackElement.matches('.copy-feedback')) {{
                feedbackElement.style.display = 'inline';
                setTimeout(function() {{
                    feedbackElement.style.display = 'none';
                }}, 2000);
            }}
        }}
    }});
    </script>
    '''
    
    return html_code