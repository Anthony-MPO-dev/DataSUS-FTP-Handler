import json
import os
from urllib.request import URLError

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.modules.webscraping.init.configs import path_config, path_raw


def load_config(file_path: str) -> dict:
    """
    Carrega as configurações a partir de um arquivo JSON.

    Parâmetros:
    -----------
    file_path : str
        O caminho para o arquivo de configuração.

    Retorno:
    --------
    dict
        Um dicionário contendo as configurações.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def init_browser(hidden: bool = True) -> webdriver.Chrome:
    """
    Inicializa o navegador Chrome utilizando o Selenium WebDriver e navega para a página do DWweb.

    Parâmetros:
    -----------
    hidden : bool, opcional
        Define se o navegador deve ser executado em modo oculto (headless).
        O padrão é True, o que significa que o navegador será executado sem interface gráfica.

    Retorno:
    --------
    webdriver.Chrome
        Uma instância configurada do Selenium WebDriver para o Chrome.

    Exceções:
    ---------
    ValueError
        Lançada quando ocorre uma falha na resolução de nomes de domínio (problemas de conexão)
        ou qualquer outro erro ao inicializar o WebDriver.
    """

    try:

        def is_docker():
            import os

            var = os.getenv('DOCKER_ENV')
            return var == 'production'

        # Instala e verifica automaticamente a versão compatível do ChromeDriver
        chromedriver_autoinstaller.install()

        chrome_options = Options()

        # Carrega a configuração do arquivo
        config = load_config(path_config)
        hidden_mode = config.get('browser_mode', 'headless') == 'headless'

        if hidden_mode:
            chrome_options.add_argument('--headless')
        else:
            chrome_options.add_argument('--start-maximized')

        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920x1080')

        if is_docker():
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        # Configurações de download
        prefs = {
            'download.default_directory': path_raw,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True,
        }
        chrome_options.add_experimental_option('prefs', prefs)

        navegador = webdriver.Chrome(options=chrome_options)
        navegador.get(
            'https://datasus.saude.gov.br/transferencia-de-arquivos/#'
        )

        print('Sistema iniciado com sucesso!')

        return navegador

    except URLError as e:
        if '[Errno -3] Temporary failure in name resolution' in str(e):
            raise ValueError(
                'Erro: Falha temporária na resolução de nome. Verifique sua conexão com a internet.'
            )
        else:
            raise ValueError('Erro:', e)

    except Exception as e:
        raise ValueError(f'Ocorreu um erro ao inicializar o WebDriver:\n', e)


# Inicializa o navegador com base na configuração do arquivo
navigator = init_browser()
