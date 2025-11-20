# Gapminder App - Explorador de Dados Globais

📊 Projeto feito com **Streamlit** para explorar dados globais do Gapminder usando Databricks como banco de dados, incluindo população, PIB per capita e expectativa de vida entre as décadas de 1960 e 2020 e com projeção até 2040.

---

## Funcionalidades

- Filtros interativos por continente, país e intervalo de anos
- Visualização de métricas principais (Expectativa de Vida, PIB per Capita, População)
- Gráficos personalizáveis: Linha, Barra, Dispersão e Mapa
- Análises avançadas:
  - Ranking Global
  - Crescimento Percentual
  - Variação por Década
- Tabela filtrada disponível em qualquer momento

---

## Tecnologias

- Python 3.x
- Streamlit
- Pandas
- Plotly Express
- Databricks SQL
- Python-dotenv (para variáveis de ambiente)

---

## Como usar

### 1. Clone o repositório:

```bash
git clone https://github.com/AndersonCarvalho96/gapminder-app.git
cd gapminder-app
```
### 2. Instale as dependências:

pip install -r requirements.txt


### 3. Crie um arquivo .env com suas credenciais do Databricks:

DATABRICKS_HOST=<seu_host>
DATABRICKS_HTTP_PATH=<seu_http_path>
DATABRICKS_TOKEN=<seu_token>


### 4.Rode o Streamlit:

streamlit run app.py

## Screenshots


![População Total](screenshots/População total.png)
![Crescimento Percentual](screenshots/Crescimento Percentual.png)
