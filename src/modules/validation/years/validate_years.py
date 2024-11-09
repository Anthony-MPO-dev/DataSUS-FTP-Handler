import os
import sys

# Adiciona o diretório base ao sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from src.modules.validation.years.search_years import get_years_by_theme


def validate_years(years, theme):
    AVAILABLE_YEARS = get_years_by_theme(theme)
    """Valida os anos fornecidos como argumento."""
    if not years:
        return AVAILABLE_YEARS  # Se nenhum ano for fornecido, use todos os anos disponíveis.

    try:
        init_year, end_year = map(int, years.split('-'))
    except ValueError:
        raise ValueError(
            "Erro: O formato de anos deve ser 'YYYY-YYYY'. Exemplo: '2001-2005'."
        )

    if (
        init_year not in AVAILABLE_YEARS
        or end_year not in AVAILABLE_YEARS
        or init_year > end_year
    ):
        raise ValueError(
            f'Erro: O período de anos deve estar dentro do intervalo disponível: {AVAILABLE_YEARS[0]}-{AVAILABLE_YEARS[-1]}.\n'
            f"Exemplo válido: '2001-2005'. Anos fornecidos: '{init_year}-{end_year}'."
        )

    return list(range(init_year, end_year + 1))


def check_years_present(years, theme):
    """
    Verifica se os anos fornecidos estão presentes nos anos disponíveis
    para o tema especificado.

    Parâmetros:
    ----------
    years : list[int]
        Lista de anos a serem verificados.
    theme : str
        Tema para o qual os anos disponíveis serão consultados.

    Retorna:
    -------
    bool
        Retorna True se todos os anos estiverem disponíveis, caso contrário, False.
    """
    AVAILABLE_YEARS = get_years_by_theme(theme)

    if not years:
        return False  # Se não há anos fornecidos, retorna False

    return all(year in AVAILABLE_YEARS for year in years)
