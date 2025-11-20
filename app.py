# app.py
import streamlit as st
import pandas as pd
from data import load_data_from_databricks, prepare_data
from filters import sidebar_filters
from kpis import exibir_kpis, exibir_explicacao_kpi
from charts import (
    plot_metric,
    plot_ranking_global,
    plot_growth_percent,
    plot_variacao_decada
)

st.set_page_config(layout="wide", page_title="Explorador de Dados Globais")

# Carregar dados

df = load_data_from_databricks()

if df is None or not isinstance(df, pd.DataFrame) or df.empty:
    st.title("Explorador de Dados Globais")
    st.warning("Nenhum dado disponível. Verifique a conexão ou a tabela.")
    st.stop()

# Preparar colunas derivadas (diffs, growth, ranking, projeção)
df = prepare_data(df)

# Dicionário de métricas (id -> label amigável)
metricas_dict = {
    "lifeExp": "Expectativa de Vida",
    "gdpPercap": "PIB per Capita",
    "pop": "População",
}

# ---- Sidebar ----
continentes, paises, metrica_coluna, tipo_grafico, anos, analise_avancada = sidebar_filters(
    df, metricas_dict)

# ---- Aplica filtros ----
df_filtrado = df.copy()
df_filtrado = df_filtrado[(df_filtrado["year"] >= anos[0]) & (
    df_filtrado["year"] <= anos[1])]
if continentes != "Todos":
    df_filtrado = df_filtrado[df_filtrado["continent"] == continentes]
if paises:
    df_filtrado = df_filtrado[df_filtrado["country"].isin(paises)]

# ---- Título ----
st.title("Explorador de Dados Globais")

# Explicações rápidas para as análises avançadas
EXPLICACOES_ANALISES = {
    "Ranking Global": "Ordena países pela métrica selecionada no último ano do intervalo — ideal para comparar posições globais.",
    "Crescimento Percentual": "Mostra o crescimento percentual entre o primeiro e o último ano do intervalo selecionado.",
    "Variação por Década": "Exibe a diferença entre cada década e a anterior (delta) por país."
}

# ---- Modo: Análise Avançada ou Normal ----
if analise_avancada != "Nenhuma":
    st.info(
        f"🔎 Modo Análise Avançada: **{analise_avancada}** — o gráfico abaixo corresponde a essa análise.")
    exibir_kpis(df_filtrado, metrica_coluna, metricas_dict)

    st.markdown("---")
    st.markdown(EXPLICACOES_ANALISES.get(analise_avancada, ""))

    if analise_avancada == "Ranking Global":
        plot_ranking_global(df_filtrado, metrica_coluna,
                            metricas_dict, top_n=20, use_map=False)
    elif analise_avancada == "Crescimento Percentual":
        plot_growth_percent(df_filtrado, metrica_coluna, metricas_dict)
    elif analise_avancada == "Variação por Década":
        plot_variacao_decada(df_filtrado, metrica_coluna, metricas_dict)

else:
    # Modo normal (usuário escolhe tipo de gráfico)
    exibir_kpis(df_filtrado, metrica_coluna, metricas_dict)

    st.markdown(
        f"**Filtro atual:** Continente = **{continentes}**, Países = **{', '.join(paises) if paises else 'Todos'}**, Anos = **{anos[0]}–{anos[1]}**")

    # Exibe explicação curta da métrica (se disponível)
    exibir_explicacao_kpi(metrica_coluna)

    # Plota métrica conforme tipo escolhido
    plot_metric(df_filtrado, metrica_coluna, metricas_dict, tipo_grafico)

# ---- Tabela filtrada (sempre disponível) ----
with st.expander("Mostrar tabela filtrada"):
    st.dataframe(df_filtrado.reset_index(drop=True))
