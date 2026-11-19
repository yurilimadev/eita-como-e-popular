# Pré-requisitos — Eita Como É Popular

## Essencial (sem isso a decisão sai errada)
- Identidade × posição (chave de junção vs. índice) — morde em `data/extracao.py:23-37` e `data/df_local.csv:1`: juntar tabelas sem chave identificadora (`id` IBGE de 7 dígitos) ou com índice desalinhado no `pandas.concat` troca as coordenadas de todas as cidades.
- Tempo de preparação vs. tempo de execução — morde em `app.py:11` e `data/extracao.py:9`: requisitar a API do IBGE na importação acopla a abertura da tela à disponibilidade e às regras de firewall da API.
- Ciclo de reexecução do Streamlit e `st.session_state` — morde em `app.py:17-109`: distinguir widgets que já retêm estado (`st.selectbox`) de botões efêmeros (`st.form_submit_button`).
- Containers de layout e o bloco `with` (Context Manager) — morde em `app.py:34-90`: delimitar em qual caixa visual (`st.sidebar`, `st.form`, `st.columns`, `st.container`) cada componente é desenhado.

## Sob demanda (carregar quando a decisão tocar)
- Separação entre consulta de dados (Pandas) e componentes de tela (Streamlit/Folium) — carregar ao refatorar `app.py:72-143`.

## Fora de escopo / desconhecido
- Autenticação / OAuth com Instagram — fora porque a API oficial da Meta bloqueia contas pessoais (desde dez/2024) e exige verificação empresarial/App Review, gerando atrito para o usuário e desenvolvimento.
- Banco relacional transacional / filas — fora porque o app é de consulta pública somente leitura sobre dados anuais.
