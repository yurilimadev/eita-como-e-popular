# 🌎 Eita, como é popular!

<p align="center">
  <img src="assets/logo-eita-como-e-popular.jpg" alt="Mascote Eita, como é popular!" width="420" />
</p>

> *"Tenho 15 mil seguidores!"* — Parabéns, você já pode fundar um município no interior, cobrar IPTU nos stories e disputar a prefeitura! 🎩✨

**Eita, como é popular!** é um aplicativo web em Python + Streamlit que responde à pergunta que todo criador de conteúdo (ou curioso de plantão) já se fez: **se os meus seguidores do Instagram, TikTok, YouTube ou X resolvessem morar todos juntos, quantas cidades do Brasil eu já teria superado em população?**

🔗 **Acesse agora no ar:** [https://eitacomoepopular.yurilimadev.com](https://eitacomoepopular.yurilimadev.com)

---

## 🏙️ O que o app faz?

1. **Você digita seu número de seguidores** (de qualquer rede social — não precisa fazer login nem entregar a alma em OAuth!).
2. **O Brasilzinho faz as contas:** cruzamos o seu número com as **Estimativas Populacionais de 2025 do IBGE** para todos os **5.571 municípios brasileiros**.
3. **Painel de Prefeito(a):**
   - Mostra **quantas cidades do Brasil têm menos habitantes que o seu perfil** (e a porcentagem do território nacional que você já "desbloqueou");
   - Destaca a **maior cidade que você lotaria sozinho(a)** e o **Top 10** das maiores cidades superadas;
   - Plota a cidade escolhida direto num **mapa interativo** para você saber onde fica o seu novo feudo!
   - *(E se você tiver menos de 833 seguidores — população de Serra da Saudade/MG — nosso mascote pega a lupa para te incentivar! 🔍)*

---

## 🛠️ Tecnologias utilizadas

- **[Python 3.12](https://www.python.org/)** + **[Streamlit](https://streamlit.io/)** (Interface em painel e componentes HTML/CSS customizados)
- **[Pandas](https://pandas.pydata.org/)** (Cruzamento dos dados populacionais e coordenadas geográficas)
- **[Folium](https://python-visualization.github.io/folium/)** (Mapas interativos com popup customizado)
- **[API de Agregados do IBGE](https://servicodados.ibge.gov.br/api/docs/agregados?versao=3)** (Agregado `6579` — Estimativas de População 2025, com base local consolidada por código IBGE de 7 dígitos)
- **Docker + Caddy** (Deploy em VPS com HTTPS automático)

---

## 🚀 Como rodar na sua máquina

### Opção 1: Com Python local

```bash
# 1. Clone o repositório
git clone https://github.com/yurilimadev/eita-como-e-popular.git
cd eita-como-e-popular

# 2. Instale as dependências
pip install -r requirements.txt

# 3. (Opcional) Configure uma chave PIX para o botão "Me pague um café"
echo 'PIX_KEY="sua-chave-aleatoria-ou-copia-e-cola"' > .env

# 4. Suba o aplicativo
streamlit run app.py
```

### Opção 2: Com Docker

```bash
docker build -t eita-como-e-popular .
docker run -p 8501:8501 eita-como-e-popular
```

Depois é só abrir `http://localhost:8501` no navegador!

---

## 🧪 Rodando os testes dos dados

Para garantir que nenhuma das **5.571 cidades** foi parar no meio da floresta por erro de coordenada:

```bash
python3 -m unittest discover -s tests -v
```

---

## ☕ Gostou da brincadeira?

Se você descobriu que já é maior que metade dos municípios do seu estado, considere pagar um café pelo QR Code PIX na barra lateral do app ou deixar uma ⭐ aqui no repositório!
