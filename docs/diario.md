# Diário de bordo — Eita Como É Popular

## 2026-11-04 21:00 — Herdar/learn — Raio-X do app e diagnóstico de georreferenciamento
- Decisão do dia: Manter input manual de seguidores (sem OAuth) e alinhar `df_merge` com `df_local.csv` usando `reset_index` e `id` do IBGE em base local consolidada.
- Minha razão, em uma linha: Evitar atrito com a API da Meta/IBGE em tempo real e reaproveitar coordenadas que são constantes geográficas.
- Descoberta ou evidência: `pd.concat` em `data/extracao.py:37` colava índice `1` com índice `1`, deslocando todas as 5.571 cidades em 1 posição e gerando uma linha extra (`-14.235004, -51.92528`) no fim de `data/df_local.csv:5573`.
- Registros: `docs/decisoes/0001-base-local-ibge-coordenadas.md`
- Suposições e perguntas abertas: Identificar qual é o município de índice `403` que ficou com a coordenada do centro do Brasil (`-14.235004, -51.92528`).
- Próximo passo: Executar o Passo 1 do plano incremental em `data/extracao.py` com teste de caracterização.

## 2026-11-08 21:07 — Herdar/learn — Execução do plano incremental (Passos 1 e 2)
- Decisão do dia: Gerar `data/municipios_2025.csv` alinhado pelo `id` do IBGE, corrigir as 6 coordenadas de homônimos/centro do Brasil e limpar o `session_state` redundante em `app.py`.
- Minha razão, em uma linha: Garantir 100% dos 5.571 municípios com coordenadas exatas e código Streamlit limpo sem chaves órfãs.
- Descoberta ou evidência: `tests/test_extracao.py` validou 5.571 municípios sem nulos e sem coordenadas duplicadas (`Ran 4 tests in 0.064s — OK`).
- Registros: `docs/decisoes/0001-base-local-ibge-coordenadas.md`, `docs/raio-x.md`
- Suposições e perguntas abertas: Nenhuma pendência bloqueante.
- Próximo passo: Rodar o Streamlit ou iniciar novas funcionalidades na entrada Construir.

## 2026-11-08 21:38 — Construir/learn — Layout horizontal (wide), cards HTML retrô e mascotes anos 30
- Decisão do dia: Reorganizar `app.py` em painel horizontal (`layout="wide"`), fixar `height=400` no mapa `st_folium`, criar cards HTML (`header_card.html`, `resumo_card.html`) e padronizar as ilustrações com o mascote retrô do Brasil.
- Minha razão, em uma linha: Eliminar a aparência de "tripa vertical" com espaço sobrando embaixo do mapa e unificar a identidade visual do app.
- Descoberta ou evidência: `st_folium(..., height=400, returned_objects=[])` elimina os 700px padrão de altura e evita reexecuções desnecessárias ao arrastar o mapa; `tests/test_extracao.py` passou nos 5 testes (`OK`).
- Registros: nenhum (decisão visual reversível / porta de duas vias)
- Suposições e perguntas abertas: Validar visualmente no navegador com `streamlit run app.py`.
- Próximo passo: Testar a interface no navegador e ajustar detalhes finos de estilo se desejar.

## 2026-11-18 22:46 — Operar/learn — Deploy em produção na VPS com Docker e Caddy (HTTPS)
- Decisão do dia: Publicar o app em container Docker (`eita_popular`) na porta interna `127.0.0.1:8502` (evitando conflito com `avista_parcelado` na `8501`) atrás do Caddy com HTTPS automático em `eitacomoepopular.yurilimadev.com`.
- Minha razão, em uma linha: Isolar o ambiente Python/Streamlit com reinício automático (`--restart unless-stopped`) sem interferir nos serviços existentes da VPS.
- Descoberta ou evidência: `curl -i https://eitacomoepopular.yurilimadev.com/_stcore/health` retornou `HTTP/2 200 ok` via Caddy com TLS ativo.
- Registros: `docs/operacao.md`
- Suposições e perguntas abertas: Cadastrar `https://eitacomoepopular.yurilimadev.com/_stcore/health` em monitor externo para atingir Nível 1/2 de maturidade operacional.
- Próximo passo: Fazer commit/push para o GitHub e opcionalmente cadastrar o health check no monitor.
