# utils.py
import pycountry


# Correções para nomes que pycountry não encontra diretamente
_CORRECOES_ISO = {
    "Russia": "RUS",
    "Vietnam": "VNM",
    "Egypt": "EGY",
    "Bolivia": "BOL",
    "Congo, Dem. Rep.": "COD",
    "Congo, Rep.": "COG",
    "Tanzania": "TZA",
    "Iran": "IRN",
    "Venezuela": "VEN",
    "United States": "USA",
    "South Korea": "KOR",
    "North Korea": "PRK",
    "Syria": "SYR",
    "Laos": "LAO",
    "Macedonia": "MKD",
    "Czechia": "CZE",
    "Ivory Coast": "CIV",
}


def get_iso_alpha(country_name: str):
    """Retorna o código ISO-3 (alpha_3) para um país, com correções manuais."""
    if not isinstance(country_name, str):
        return None
    if country_name in _CORRECOES_ISO:
        return _CORRECOES_ISO[country_name]
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except Exception:
        return None


def formatar_numero(n, decimais=None):
    """Formata números com abreviação automática (mil, M, B) mesmo usando decimais."""
    try:
        if n is None:
            return "N/A"
        n = float(n)
    except Exception:
        return "N/A"

    # --- abreviação automática ---
    abs_n = abs(n)

    if abs_n >= 1_000_000_000:
        valor = n / 1_000_000_000
        sufixo = " B"
    elif abs_n >= 1_000_000:
        valor = n / 1_000_000
        sufixo = " M"
    elif abs_n >= 1_000:
        valor = n / 1_000
        sufixo = " mil"
    else:
        valor = n
        sufixo = ""

    # --- formatação com decimais ---
    if decimais is None:
        # Se o número for inteiro após dividir, não colocar .0
        if valor.is_integer():
            return f"{int(valor)}{sufixo}"
        else:
            return f"{valor}{sufixo}"

    return f"{valor:.{decimais}f}{sufixo}"
