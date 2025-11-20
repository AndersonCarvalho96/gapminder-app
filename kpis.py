# kpis.py
import streamlit as st
from utils import formatar_numero



def exibir_kpis(df_filtrado, metrica_coluna, metricas_dict, ano_inicial=None, ano_final=None):
    """Calcula e exibe KPIs usando apenas os anos filtrados pelo usuário."""
    if df_filtrado.empty:
        st.write("Nenhum dado disponível para gerar KPIs.")
        return

    # Ajusta anos se não informados
    if ano_inicial is None:
        ano_inicial = int(df_filtrado["year"].min())
    if ano_final is None:
        ano_final = int(df_filtrado["year"].max())

    # Filtra somente os anos selecionados
    df_kpi = df_filtrado[(df_filtrado["year"] >= ano_inicial)
                         & (df_filtrado["year"] <= ano_final)]

    if df_kpi.empty:
        st.write("Nenhum dado disponível no intervalo de anos selecionado.")
        return

    # ---------- CÁLCULOS BÁSICOS ----------
    kpi_media = df_kpi[metrica_coluna].mean()

    try:
        kpi_pais_maior = df_kpi.loc[df_kpi[metrica_coluna].idxmax(), "country"]
    except Exception:
        kpi_pais_maior = "N/A"

    kpi_valor_maior = df_kpi[metrica_coluna].max()
    kpi_valor_menor = df_kpi[metrica_coluna].min()
    kpi_range = kpi_valor_maior - kpi_valor_menor
    kpi_std = df_kpi[metrica_coluna].std()

    df_ordenado = df_kpi.sort_values("year")
    kpi_inicio = df_ordenado[metrica_coluna].iloc[0]
    kpi_fim = df_ordenado[metrica_coluna].iloc[-1]

    kpi_tendencia = kpi_fim - kpi_inicio

    if kpi_inicio != 0:
        kpi_growth_rate = ((kpi_fim - kpi_inicio) / abs(kpi_inicio)) * 100
    else:
        kpi_growth_rate = 0

    kpi_pop_total = df_kpi["pop"].sum()

    # ---------- FORMATAÇÃO ----------
    media_f = str(formatar_numero(kpi_media, decimais=2))
    maior_f = str(formatar_numero(kpi_valor_maior, decimais=2))
    menor_f = str(formatar_numero(kpi_valor_menor, decimais=2))
    range_f = str(formatar_numero(kpi_range, decimais=2))
    std_f = str(formatar_numero(kpi_std, decimais=2))
    tendencia_f = str(formatar_numero(kpi_tendencia, decimais=2))
    growth_pct_f = f"{kpi_growth_rate:.2f}%"
    total_pop_f = str(formatar_numero(kpi_pop_total))

    # ---------- EXIBIÇÃO ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Média " + metricas_dict[metrica_coluna], media_f)
        st.metric("Maior valor " + metricas_dict[metrica_coluna], maior_f)
        st.metric("País com maior valor", kpi_pais_maior)

    with col2:
        st.metric("Menor valor", menor_f)
        st.metric("Desigualdade (Range)", range_f)
        st.metric("Desvio-padrão", std_f)

    with col3:
        st.metric("Tendência no período (Fim - Início)", tendencia_f)
        st.metric("Crescimento (%) no período", growth_pct_f)
        st.metric("População total", total_pop_f)



# ------------------ EXPLICAÇÕES ---------------------

EXPLICACOES_KPIS = {
    "lifeExp": """
    ## 📘 Indicador: Expectativa de Vida

    A expectativa de vida representa quantos anos, em média, uma pessoa nascida naquele período tende a viver.
    - **Valores maiores** → maior longevidade, melhores condições de saúde e bem-estar.  
    - Ideal para avaliar desenvolvimento humano ao longo das décadas.
    """,

    "gdpPercap": """
    ## 💰 Indicador: PIB per Capita

    O PIB per capita indica quanto de riqueza, em média, cada pessoa produz no país.
    - **Valores altos** sugerem economia mais forte e produtiva.  
    - Em dados por décadas, mostra tendências econômicas estruturais de longo prazo.
    """,

    "pop": """
    ## 👥 Indicador: População Total

    Quantidade total de habitantes no país no período analisado.
    - Útil para entender crescimento demográfico, impacto regional e distribuição populacional.
    """,

    # MÉTRICAS AVANÇADAS
    "delta_lifeExp": """
    ## 🔄 Indicador: Variação da Expectativa de Vida

    Diferença da expectativa de vida entre uma década e a seguinte.
    - **Positivo** → a população passou a viver mais anos  
    - **Negativo** → piora temporária (guerras, crises, epidemias)  
    """,

    "delta_gdpPercap": """
    ## 📈 Indicador: Variação do PIB per Capita

    Indica quanto o PIB per capita mudou de uma década para a próxima.
    - **Positivo** → economia cresceu  
    - **Negativo** → recessão ou desaceleração temporária  
    """,

    "growth_pop": """
    ## 📊 Indicador: Crescimento Populacional (%)

    Percentual de aumento (ou queda) da população no intervalo selecionado.
    - Valores altos → forte expansão demográfica  
    - Valores baixos ou negativos → estagnação ou redução populacional  
    """
}


def exibir_explicacao_kpi(metrica_coluna: str):
    texto = EXPLICACOES_KPIS.get(metrica_coluna)
    if texto:
        st.markdown("---")
        st.markdown(texto)
