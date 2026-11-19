# 0001 — Alinhamento de coordenadas e base local consolidada com ID do IBGE

- **Data e hora:** 2026-11-04 21:00
- **Status:** aceita
- **Contexto, evidência e decisão (1–3 frases):** Em `data/extracao.py:23-37`, `df_merge` iniciava no índice `1` (após `.iloc[1:, :]`) enquanto `df_loc` (`data/df_local.csv`) iniciava no índice `0`, fazendo o `pd.concat(..., axis=1)` deslocar as coordenadas de todos os 5.571 municípios em uma posição, além de depender da API do IBGE a cada carga do app. Decidimos corrigir o alinhamento de índice (`reset_index(drop=True)`), descartar a linha fantasma final (`iloc[:5571]`), preservar o `id` de 7 dígitos do IBGE e consolidar os dados em CSV local versionado, usando a API do IBGE apenas para validação/atualização anual.
- **Alternativas descartadas e por quê (opcional):** Reexecutar geocodificação via Google Maps API (desnecessário, pois as 5.571 coordenadas já estão no CSV e são constantes geográficas) ou fazer join apenas pelo nome da cidade (falha em municípios homônimos no Brasil).
- **Consequências, custo de desfazer e reversibilidade:** Porta de duas vias; o app abre instantaneamente sem depender da disponibilidade do IBGE em produção, exigindo apenas rodar a atualização anual quando sair nova estimativa populacional.
- **Quando revisitar:** Quando o IBGE publicar nova estimativa anual de população ou caso haja criação/emancipação de novos municípios na malha territorial.
