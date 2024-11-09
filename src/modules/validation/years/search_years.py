from datetime import datetime

# Lista de temas disponíveis
TEMAS_DISPONIVEIS = ['TUBE']


def get_years_by_theme(theme):
    """
    Retorna uma lista de anos de 2001 até o ano atual com base no tema fornecido.

    Parâmetros:
    ----------
    theme : str
        O tema para o qual os anos devem ser retornados.

    Retorna:
    -------
    list
        Lista de anos de 2001 até o ano atual.

    Exceções:
    ---------
    ValueError
        Lançada se o tema não estiver na lista de temas disponíveis.
    """
    ano_atual = datetime.now().year
    if theme not in TEMAS_DISPONIVEIS:
        raise ValueError(
            f"Erro: O tema '{theme}' não é suportado. Temas disponíveis: {TEMAS_DISPONIVEIS}."
        )

    # retorna os anos 2001 até 2023
    return list(range(2001, 2024))
