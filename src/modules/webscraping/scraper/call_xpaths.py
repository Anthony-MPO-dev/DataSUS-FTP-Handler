"""
Multi-line docstring summary.

#Módulo de Funções Úteis para Interação com Elementos Web

Este módulo contém funções que são úteis para interagir com elementos em uma página da web.
Ele inclui funções para localizar elementos por XPath e realizar ações neles, como clicar e inserir texto.

# Funções:
-----------
    - call_element_by_xpath(xpath): Localiza um elemento pelo XPath e clica nele.
    - call_input_by_xpath(xpath, message): Localiza um elemento de entrada pelo XPath e insere um texto nele.

# Importações:
---------------
    - from selenium.webdriver.common.by import By
    - from selenium.webdriver.support.ui import WebDriverWait
    - from selenium.webdriver.support import expected_conditions as EC
    - from selenium.common.exceptions import NoSuchElementException, TimeoutException
    - from modules.init_modules.init_navigator import sys
    - from time import sleep (usado pelas funções de outros módulos)
"""
import os
import sys
from time import sleep

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def call_element_by_xpath(xpath: str) -> None:
    """
    Multi-line docstring summary.

    # Localiza um elemento pelo seu XPath e clica nele.

    # Args:
    --------
        xpath (str): O XPath do elemento a ser localizado e clicado.

    # Global:
    -----------
        navegador (webdriver): A instância do navegador global.

    # Raises:
    ----------
        NoSuchElementException: Se o elemento não for encontrado.
        TimeoutException: Se o elemento não for visível após o tempo limite de espera.

    # Retorna:
    -----------
        None
    """

    from src.modules.webscraping.init.navigator import navigator as nav

    diretorio_atual = os.path.abspath(__file__)

    try:
        # Aguarde até que o elemento seja visível na página
        elemento = WebDriverWait(nav, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        # Clique no elemento
        elemento.click()

    except (NoSuchElementException, TimeoutException, KeyboardInterrupt) as e:
        # deleta_arquivos('./')
        nav.quit()
        raise ValueError(
            f'{diretorio_atual}\n\tErro ao localizar ou interagir com o elemento:\n {e}'
        )
    except ConnectionError as ce:
        # deleta_arquivos('./')
        nav.quit()
        raise ValueError(f'{diretorio_atual}\n\tErro de conexão:\n{ce}')


def call_input_by_xpath(xpath: str, message: str) -> None:
    """
    Multi-line docstring summary.

    # Call input pelo xpath

    Localiza um elemento de entrada pelo seu XPath e insere um texto nele.

    # Args:
    --------
        xpath (str): O XPath do elemento de entrada a ser localizado.
        message (str): O texto a ser inserido no elemento de entrada.

    # Global:
    ----------
        navegador (webdriver): A instância do navegador global.

    # Raises:
    ----------
        NoSuchElementException: Se o elemento de entrada não for encontrado.
        TimeoutException: Se o elemento de entrada não for visível após o tempo limite de espera.

    # Retorna:
    ------------
        None

    """
    from src.modules.webscraping.init.navigator import navigator as nav

    diretorio_atual = os.path.abspath(__file__)

    try:
        # Aguarde até que o elemento de entrada seja visível na página
        elemento = WebDriverWait(nav, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        # Insira o texto e pressione Enter
        elemento.send_keys(message)
        elemento.submit()

    except (NoSuchElementException, TimeoutException, KeyboardInterrupt) as e:
        # deleta_arquivos('./')
        nav.quit()
        raise ValueError(
            f'{diretorio_atual}\n\tErro ao localizar ou interagir com o elemento de entrada: {e}'
        )
    except ConnectionError as ce:
        # deleta_arquivos('./')
        nav.quit()
        raise ValueError(f'{diretorio_atual}\n\tErro de conexão:\n{ce}')
