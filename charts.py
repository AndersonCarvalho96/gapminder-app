# charts.py
import streamlit as st
import plotly.express as px


def plot_metric(df_filtrado, metrica_coluna, metricas_dict, tipo_grafico):
    """Plota a métrica normal (usuário escolhe tipo_grafico)"""
    title = f"{metricas_dict[metrica_coluna]} — dados filtrados"
    if df_filtrado.empty:
        st.warning("Sem dados para essa visualização.")
        return

    if tipo_grafico == "Linha":
        fig = px.line(df_filtrado, x="year", y=metrica_coluna,
                      color="country", markers=True, title=title)
    elif tipo_grafico == "Barra":
        ano_max = int(df_filtrado["year"].max())
        df_barras = df_filtrado[df_filtrado["year"] == ano_max]
        if df_barras.empty:
            st.warning("Sem dados para criar barras no ano selecionado.")
            return
        fig = px.bar(df_barras.sort_values(metrica_coluna, ascending=False),
                     x="country", y=metrica_coluna, title=f"{title} — {ano_max}")
    elif tipo_grafico == "Dispersão":
        # scatter fixo entre GDP per cap e lifeExp (se existir)
        if "gdpPercap" in df_filtrado.columns and "lifeExp" in df_filtrado.columns:
            fig = px.scatter(df_filtrado, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                             hover_name="country", animation_frame="year", title="PIB per Capita vs Expectativa de Vida")
        else:
            st.warning("Não há colunas necessárias para dispersão.")
            return
    else:  # Mapa
        if "iso_alpha" not in df_filtrado.columns:
            st.warning("Coluna iso_alpha ausente — não é possível gerar mapa.")
            return
        fig = px.choropleth(df_filtrado, locations="iso_alpha", color=metrica_coluna,
                            hover_name="country", projection="natural earth", animation_frame="year",
                            title=title, color_continuous_scale="Viridis")

    st.plotly_chart(fig, use_container_width=True)


# --------- Análises Avançadas ---------
def plot_ranking_global(df_filtrado, metrica_coluna, metricas_dict, top_n=20, use_map=False):
    """Ranking por último ano filtrado. top_n controla quantos países mostrar em barra."""
    if df_filtrado.empty:
        st.warning("Sem dados para ranking.")
        return
    ano = int(df_filtrado["year"].max())
    df_latest = df_filtrado[df_filtrado["year"] == ano]
    df_rank = df_latest.groupby("country", as_index=False)[
        metrica_coluna].mean()
    df_rank = df_rank.sort_values(metrica_coluna, ascending=False).head(top_n)

    title = f"Ranking Global — {metricas_dict[metrica_coluna]} — Ano {ano}"
    if use_map and "iso_alpha" in df_latest.columns:
        df_map = df_latest.copy()
        fig = px.choropleth(df_map, locations="iso_alpha", color=metrica_coluna,
                            hover_name="country", projection="natural earth", title=title)
    else:
        fig = px.bar(df_rank.sort_values(metrica_coluna),
                     x=metrica_coluna, y="country", orientation="h", title=title)
    st.plotly_chart(fig, use_container_width=True)


def plot_growth_percent(df_filtrado, metrica_coluna, metricas_dict):

    if df_filtrado.empty:
        st.warning("Sem dados suficientes para calcular crescimento percentual.")
        return

    metrica_label = metricas_dict.get(metrica_coluna, metrica_coluna)

    # Crescimento: últimos vs primeiros valores de cada país no intervalo selecionado
    df_growth = (
        df_filtrado.groupby("country")[metrica_coluna]
        .apply(lambda x: ((x.iloc[-1] - x.iloc[0]) / x.iloc[0]) * 100 if x.iloc[0] != 0 else 0)
        .reset_index(name="growth_pct")
    )

    # Ordenar para destacar maiores crescimentos
    df_growth = df_growth.sort_values("growth_pct", ascending=False)

    # Formatar os valores como porcentagem com 2 casas
    df_growth["growth_pct_fmt"] = df_growth["growth_pct"].map(
        lambda x: f"{x:.2f}%")

    # Gráfico de pizza
    fig = px.pie(
        df_growth,
        names="country",
        values="growth_pct",
        title=f"Crescimento Percentual de {metrica_label} ({df_filtrado['year'].min()}–{df_filtrado['year'].max()})",
        hole=0.4  # donut mais elegante
    )

    # Mostrar labels no hover
    fig.update_traces(
        text=df_growth["growth_pct_fmt"],
        textposition="inside"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Mostrar tabela opcional
    with st.expander("Mostrar dados do crescimento percentual"):
        st.dataframe(df_growth.reset_index(drop=True))


def plot_variacao_decada(df_filtrado, metrica_coluna, metricas_dict):
    """Mostra deltas entre décadas (valor atual - valor anterior) — linha por país."""
    if df_filtrado.empty:
        st.warning("Sem dados para variação por década.")
        return
    df_sorted = df_filtrado.sort_values(["country", "year"]).copy()
    df_sorted["delta"] = df_sorted.groupby("country")[metrica_coluna].diff()
    fig = px.line(df_sorted, x="year", y="delta", color="country",
                  title=f"Variação por Década — {metricas_dict[metrica_coluna]}", markers=True)
    st.plotly_chart(fig, use_container_width=True)
