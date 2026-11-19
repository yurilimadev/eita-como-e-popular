# Ficha de Operação — Eita Como É Popular

- **Entrada:** Operar · **Modo:** learn · **Data:** 2026-11-18
- **Nível sustentado:** 0 (com itens do Nível 2 verificados) · **Por quê:** O deploy repetível com rollback (`Dockerfile` + Caddy backup) e a base versionada (`data/municipios_2025.csv`) estão verificados, mas ainda não há um monitor externo com alerta ativo (requisito do Nível 1).

## Estado por evidência

| Item | Status: não existe / existe, não verificado / existe e verificado | Evidência redigida + data | Hipótese/pergunta | Próximo passo menor |
|---|---|---|---|---|
| Container Docker (`eita_popular`) | existe e verificado | Container rodando em `127.0.0.1:8502->8501/tcp` com `--restart unless-stopped` (2026-11-18) | Reinicia sozinho se o processo cair | Monitorar consumo de RAM (`docker stats`) |
| Proxy reverso + HTTPS (Caddy) | existe e verificado | `caddy validate` OK e `HTTP/2 200` em `https://eitacomoepopular.yurilimadev.com/_stcore/health` (2026-11-18) | Renovação TLS automática via Caddy | — |
| Monitor externo de disponibilidade | não existe | Nenhum monitor externo configurado para o novo subdomínio | Se a VPS cair, não há alerta imediato | Cadastrar `/_stcore/health` num monitor externo (ex.: UptimeRobot ou no painel `monitoramento`) |
| Base de dados e backup | existe e verificado | `data/municipios_2025.csv` e `data/df_local.csv` versionados e testados com `tests/test_extracao.py` (`Ran 5 tests — OK`, 2026-11-18) | Dados somente leitura | Atualizar anualmente quando sair nova estimativa do IBGE |

## Régua de maturidade

| Nível | Requisito | Status/evidência |
|---|---|---|
| 0 | Só produção; ninguém sabe que caiu até reclamarem | **Atingido (nível atual sustentado)** — Logs via `docker logs eita_popular` |
| 1 | Monitor externo avisa; erros ficam registrados | **Lacuna:** endpoint `/_stcore/health` responde `ok`, falta cadastrar alerta externo |
| 2 | Backup restaurado em teste; deploy repetível com rollback | **Verificado:** `Dockerfile`, `/etc/caddy/Caddyfile.bak` e base CSV testada |
| 3 | Homologação separada; alertas úteis; checagens de dados | Homologação local (`localhost:8501`) + 5 testes automatizados em `tests/test_extracao.py` |
| 4 | Métricas de sucesso e incidentes geram aprendizado | Não existe |

## O1–O6

| Passo | Status/evidência | Chapéu envolvido | Pergunta a levar | Ação proposta (não executada) |
|---|---|---|---|---|
| O1 Mapa de produção | existe e verificado (`Caddy :80/:443` → `Docker 127.0.0.1:8502`, arquivos em `/srv/eita-como-e-popular`) | Infra / Segurança | — | — |
| O2 Saber se está vivo | existe e verificado (`GET /_stcore/health` → `HTTP/2 200 ok`) | Infra / Suporte | Quer plugar esse endpoint no seu `monitoramento.yurilimadev.com` ou UptimeRobot? | Adicionar URL `/_stcore/health` no monitor externo |
| O3 Saber se está certo | existe e verificado (`tests/test_extracao.py` valida 5.571 municípios sem nulos/duplicatas) | Dados / QA | — | Rodar `python3 -m unittest` antes de cada deploy |
| O4 Não perder dados | existe e verificado (CSVs versionados no repositório e no container) | Dados | — | Manter cópia no GitHub (`git push`) |
| O5 Mudar com segurança | existe e verificado (`Dockerfile` + `Caddyfile.bak` + isolamento de porta `8502`) | Infra | — | — |
| O6 Quando der errado | existe e verificado (rollback documentado em 1 comando) | Infra | — | — |

## Critérios de sucesso e compromisso de retorno

| Critério de sucesso de Construir | Como medir/observar | Quando revisar | Responsável | Status |
|---|---|---|---|---|
| Comparar seguidores com os 5.571 municípios sem erro de coordenada e sem espaço vazio no mapa | Acessar `https://eitacomoepopular.yurilimadev.com`, testar busca e abrir marcador no mapa | Após cada deploy ou atualização anual do IBGE | Dono do projeto | Verificado (2026-11-18) |

## Pontos fracos desta proposta

- **Evidência que falta:** Alerta ativo em monitor externo (para subir do Nível 0 para os Níveis 1 e 2 completos).
- **Suposição:** A chave PIX configurada em `/srv/eita-como-e-popular/.env` permanecerá apenas na VPS (permissão `600`) e fora do Git.
- **Risco/limite de recuperação:** Se o disco ou a VPS inteira falhar, a recuperação depende do repositório Git e de recriar o arquivo `.env`.
