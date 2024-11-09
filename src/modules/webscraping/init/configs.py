import logging
import os

path_config = (
    os.path.abspath(__file__).split('/src')[0]
    + '/src/modules/webscraping/init/config/config.json'
)

path_raw = os.path.abspath(__file__).split('/src')[0] + '/src/data/raw'


def save_browser_mode_to_config(browser_mode: str):
    """
    Salva o modo do navegador no arquivo de configuração JSON.

    Parâmetros:
    -----------
    browser_mode : str
        O modo do navegador que deve ser salvo no arquivo de configuração.
        Aceita 'visible' ou 'headless'.
    config_file : str, opcional
        O caminho para o arquivo de configuração JSON onde o modo do navegador será salvo.
        O padrão é 'config.json'.

    Exceções:
    ---------
    ValueError
        Lançada se o modo do navegador fornecido não for 'visible' ou 'headless'.
    IOError
        Lançada se houver um erro ao abrir ou gravar no arquivo de configuração.

    Exemplo de Uso:
    ---------------
    save_browser_mode_to_config('headless', 'config.json')
    """

    global path_config  # +
    import json

    config_file = path_config  # +

    if browser_mode not in ['visible', 'headless']:
        raise ValueError(
            "Modo do navegador inválido. Use 'visible' ou 'headless'."
        )

    try:
        # Carregar configurações existentes ou inicializar um novo dicionário
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
        except FileNotFoundError:
            config = {}

        # Atualizar o dicionário com o novo valor
        config['browser_mode'] = browser_mode

        # Salvar as configurações de volta no arquivo
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)

        logging.debug(
            f"Modo do navegador '{browser_mode}' salvo no arquivo de configuração '{config_file}'."
        )

    except IOError as e:
        raise IOError(
            f'Erro ao abrir ou gravar no arquivo de configuração: {e}'
        )
