# data.py
import pandas as pd
import streamlit as st
from utils import get_iso_alpha
import os
# Antigo
# from dotenv import load_dotenv
# import os
# from databricks import sql

# Carrega variáveis do .env
# load_dotenv()

# DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
# DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
# DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")


# @st.cache_data(ttl=30)
# def load_data_from_databricks():
#   """Carrega tabela gapminder do Databricks e adiciona coluna iso_alpha"""
#  try:
#     with sql.connect(
#        server_hostname=DATABRICKS_HOST,
#       http_path=DATABRICKS_HTTP_PATH,
#      access_token=DATABRICKS_TOKEN
# ) as connection:
#    query = "SELECT * FROM my_schema.gapminder"
#   df = pd.read_sql(query, connection)

#  if df is None:
#     return pd.DataFrame()

# except Exception as e:
#   st.error("Erro ao carregar dados do Databricks: " + str(e))
#  return pd.DataFrame()

# Novo, Import Local
@st.cache_data
def load_data():
    """Carrega dados a partir do CSV local."""
    try:
        csv_path = os.path.join("data", "gapminder_completo.csv")

        df = pd.read_csv(csv_path)

        # Garante tipos corretos
        if "year" in df.columns:
            df["year"] = pd.to_numeric(
                df["year"], errors="coerce").astype("Int64")

        # Cria iso_alpha se não existir
        if "iso_alpha" not in df.columns and "country" in df.columns:
            df["iso_alpha"] = df["country"].apply(get_iso_alpha)

        # Ordena para manter consistência
        df = df.sort_values(["country", "year"]).reset_index(drop=True)

        return df

    except Exception as e:
        st.error(f"Erro ao carregar o CSV: {e}")
        return pd.DataFrame()


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria colunas derivadas (diffs, pct change, ranking).
    Retorna cópia do dataframe sem alterar o original do Databricks.
    """
    df = df.copy()
    if df.empty:
        return df

    # ordenar por país/ano para diff/pct_change funcionarem corretamente
    df = df.sort_values(["country", "year"]).reset_index(drop=True)

    # deltas (valor atual - anterior) por país
    if "lifeExp" in df.columns:
        df["delta_lifeExp"] = df.groupby("country")["lifeExp"].diff()
    if "gdpPercap" in df.columns:
        df["delta_gdpPercap"] = df.groupby("country")["gdpPercap"].diff()
    if "pop" in df.columns:
        df["delta_pop"] = df.groupby("country")["pop"].diff()

    # crescimento populacional (%) por país (pct change)
    if "pop" in df.columns:
        df["growth_pop"] = df.groupby("country")["pop"].pct_change() * 100

    # ranking global (por ano) baseado em lifeExp — menor rank = melhor posição
    if "lifeExp" in df.columns and "year" in df.columns:
        df["ranking_global"] = df.groupby("year")["lifeExp"].rank(
            method="dense", ascending=False
        )

    return df
