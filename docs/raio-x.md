# Raio-X — Eita Como É Popular

**Entrada:** Herdar · **Modo:** learn · **Alvo:** Python (Streamlit / Pandas / Folium) · **Referência:** Python · **Data:** 2026-11-08 · **Ponto de partida:** bonde andando

> Só leitura por padrão. Separe fato visto, declaração, hipótese e pergunta. Cite `arquivo:linha`; não copie segredos, dados pessoais ou domínios/IPs sensíveis.

## Inventário H1

| Área | O que existe | Evidência/escopo | Status: não existe / não verificado / verificado |
|---|---|---|---|
| Dependências | Streamlit, Pandas, Folium, GoogleMaps, Requests | `requirements.txt:1-51` | existe, não verificado em venv local |
| Deploy config | Comando Streamlit para Railway | `Procfile:1`, `app.py:44` | existe, não verificado |
| Interface principal | Formulário de seguidores, tabela top 10/11 e mapa Folium | `app.py:1-154` | existe, verificado por leitura |
| Extração e junção | Busca estimativa IBGE 2025 e concatena com CSV local | `data/extracao.py:1-37` | existe, API IBGE verificada (HTTP 200 em 1,40s) |
| Geocodificação offline | Script que consultou Google Maps API e gerou CSV | `utils/locations.py:1-53`, `data/df_local.csv:1-5573` | existe, CSV verificado (5.572 linhas de dados) |
| Componentes HTML | Popup do mapa e botão de copiar PIX | `assets/style.py:1-97`, `components/mapa_popup.html:1-75` | existe, verificado por leitura |
| Testes automatizados | Testes de dados ou de tela | Escopo do repositório | não existe |

## Decisões já tomadas

| Decisão observada | Evidência | Registro retroativo | Motivo conhecido / “motivo não registrado” |
|---|---|---|---|
| Cachear latitudes/longitudes em CSV local | `utils/locations.py:49-53`, `data/df_local.csv` | `0001` | Evitar chamadas repetidas e pagas à API do Google Maps |
| Entrada manual de seguidores (sem OAuth) | `app.py:51` | Diário 2026-11-04 | Evitar atrito de login para o usuário e bloqueio da Meta a contas pessoais |
| Alinhar base IBGE + CSV local com `id` IBGE | `data/extracao.py:23-37` | `0001` | Corrigir deslocamento de 1 linha no `pd.concat` e evitar timeout da API em tempo de execução |

## Mapa do domínio H2

- **Glossário/contextos:**
  - *Município (`localidade`)*: cidade brasileira identificada pelo código IBGE de 7 dígitos (`id`), com `cidade` (nome), `estado` (sigla UF), estimativa populacional (`2025`) e coordenadas (`latitude`, `longitude`).
  - *Comparação de popularidade*: filtro dos municípios cuja população estimada em 2025 é menor ou igual ao `numero_seguidores` informado pelo usuário.
- **Divergências Declarado × Implementado:**
  - *Coordenadas dos municípios*: Declarado = cada cidade recebe sua própria coordenada; Implementado (`data/extracao.py:23,37`) = `df_merge` começa no índice `1` e `df_loc` no índice `0`, deslocando todas as cidades em 1 posição (`confirmado`).
  - *Top 10 cidades*: Declarado = mostrar top 10; Implementado (`app.py:86`) = `iloc[0:11,:]` retorna 11 cidades (`confirmado`).
  - *Botão Restaurar*: Declarado = zerar sessão; Implementado (`app.py:68`) = escreve em `numero_de_seguidores` em vez de `numero_seguidores` (`confirmado`).

## Fluxos de dados H3

| Fluxo crítico | Caminho tela → rota → regra → integração/persistência → resposta | Arquivo:linha confirmado | Hipótese |
|---|---|---|---|
| Carga inicial de dados | Importação em `app.py` → `GET` API IBGE 2025 → regex `cidade/estado` → `pd.read_csv('data/df_local.csv')` → `pd.concat(axis=1)` | `app.py:11` → `data/extracao.py:7-37` | Se a API do IBGE bloquear o IP de nuvem ou oscilar, a abertura do app falha |
| Comparar seguidores | `st.form('form1')` → `submit_button` → `mostra_resultados = True` → `df_merge['2025'] <= numero_seguidores` → `df_top10` na tabela | `app.py:50-88` | Confirmado no código |
| Visualizar cidade no mapa | `st.selectbox` → filtro `df_top10['cidade'] == cidade` → `folium.Map` + `Marker` → `st_folium` | `app.py:101-143` | Se houver duas cidades homônimas no `df_top10`, o filtro por nome pega a primeira |

## Diagnóstico H4

| Achado | Evidência ou hipótese | Impacto/risco | Frequência | Prioridade: dói / feia mas inofensiva |
|---|---|---|---|---|
| Deslocamento de 1 linha no `pd.concat` das coordenadas | `data/extracao.py:23-37` e `data/df_local.csv:1-5573` (`confirmado`) | Todas as 5.571 cidades apontam para a coordenada da cidade seguinte | Sempre (100% das buscas) | **Dói** |
| Requisição síncrona ao IBGE sem cache/base local pronta | `data/extracao.py:9` importado em `app.py:11` (`confirmado`) | App cai ou dá timeout se a API do IBGE bloquear IP ou oscilar | A cada inicialização/reexecução sem cache | **Dói** |
| Município de índice `403` com coordenada genérica do Brasil | `data/df_local.csv:405` (`-14.235004, -51.92528`, `confirmado`) | Uma cidade específica cai no centro do país | Só quando essa cidade é selecionada | **Dói (pontual)** |
| Redundância de `session_state` no `selectbox` e typo no Restaurar | `app.py:68, 98-108` (`confirmado`) | Código confuso de manter; chave órfã `numero_de_seguidores` | Sempre | **Feia mas inofensiva** |

## Rede de proteção H5

| Pré-requisito | Status/evidência | Próxima verificação segura |
|---|---|---|
| Testes de caracterização | Não existe | Script verificando `5571` municípios, sem nulos, e coordenadas de Alta Floresta D'Oeste (`1100015`) e Brasília (`5300108`) |
| Backup com restauração testada | Existe e verificado (`data/df_local.csv` no Git) | Preservar `data/df_local.csv` e salvar base consolidada com `id` |
| Homologação representativa | Ambiente local | Validar execução do script de extração e tela Streamlit |
| Rollback/deploy | Git (`git checkout`) | Passos pequenos por arquivo (`data/extracao.py` e depois `app.py`) |

## Plano incremental H6

| Ordem | Menor passo reversível | Critério de pronto/teste | Risco e rollback | Cartão/Brief |
|---|---|---|---|---|
| Passo 1 | Alinhar índices em `data/extracao.py`, identificar cidade `403` e consolidar CSV local com `id` do IBGE | `5571` cidades alinhadas, `0` nulos, 1ª e última cidades verificadas | Baixo; `git checkout data/extracao.py` | Registro `0001` |
| Passo 2 | Limpar `session_state` redundante e filtro do `selectbox` em `app.py` | Seleção de cidade e botão Restaurar funcionando sem chaves órfãs | Baixo; `git checkout app.py` | Diário |

## Pontos fracos desta proposta

- Custo de desfazer: baixo (alterações isoladas em 2 arquivos Python e 1 CSV consolidado).
- Suposições: assumimos que a ordem dos 5.571 municípios retornada pela API do IBGE para o agregado 6579 é a mesma de quando `df_local.csv` foi gerado (verificado nas pontas: Alta Floresta D'Oeste e Brasília).
- Mudança provável que pode quebrar o diagnóstico: emancipação de novos municípios em anos futuros exige rodar a validação com a API do IBGE.
