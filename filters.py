# filters.py
import streamlit as st


def sidebar_filters(df, metricas_dict):
    """Cria sidebar e retorna as escolhas do usuário"""
    st.sidebar.title("Filtros")

    # Métrica principal (somente métricas base)
    metrica_amigavel = st.sidebar.selectbox(
        "Métrica principal",
        [v for k, v in metricas_dict.items() if k in ["lifeExp", "gdpPercap", "pop"]]
    )
    # converte label de volta para chave
    metrica_coluna = [k for k, v in metricas_dict.items()
                      if v == metrica_amigavel][0]

    # Continente
    continentes = st.sidebar.selectbox(
        "Selecione um continente",
        ["Todos"] + sorted(df["continent"].unique())
    )

    # Países dependente do continente
    if continentes == "Todos":
        paises_disponiveis = sorted(df["country"].unique())
    else:
        paises_disponiveis = sorted(
            df[df["continent"] == continentes]["country"].unique())

    paises = st.sidebar.multiselect(
        "Selecione os países",
        paises_disponiveis
    )

    # Intervalo de anos
    anos = st.sidebar.slider(
        "Intervalo de anos (filtra visualizações temporais)",
        int(df["year"].min()),
        int(df["year"].max()),
        (int(df["year"].min()), int(df["year"].max())),
        step=10
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Visualização")

    # Tipo de gráfico para métricas normais
    tipo_grafico = st.sidebar.selectbox(
        "Tipo de gráfico",
        ["Linha", "Barra", "Dispersão", "Mapa"]
    )

    # Nova seção: Análise Avançada (logo abaixo da métrica principal)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Análise Avançada")
    analise_avancada = st.sidebar.selectbox(
        "Escolha uma análise",
        ["Nenhuma", "Ranking Global", "Crescimento Percentual", "Variação por Década"]
    )

    return continentes, paises, metrica_coluna, tipo_grafico, anos, analise_avancada
