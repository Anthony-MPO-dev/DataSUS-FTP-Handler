import logging

import resquest

from src.modules.webscraping.scraper.call_xpaths import call_element_by_xpath


def select_data_source() -> None:
    """
    Localiza e interage com a fonte de dados com base no tema fornecido.
    """

    # Obtém o xpath correspondente a fonte dos dados SINAN
    call_element_by_xpath('//*[@id="mySelect"]/option[13]')


def select_modality(modality_name: str = 'Dados') -> None:
    """
    Seleciona a modalidade de acordo com o nome fornecido no dropdown.

    Args:
    --------
        modality_name (str): O nome da modalidade a ser selecionada.
        O valor padrão é "Dados".

    Raises:
    --------
        ValueError: Se o nome da modalidade fornecido não for válido.
    """
    # Mapeia as modalidades para seus índices correspondentes
    modalities = {
        'Arquivos auxiliares para tabulação': 1,
        'Dados': 2,  # Segunda opção
        'Documentação': 3,
        # Adicione outras modalidades aqui conforme necessário ou conforme os dados mudarem
    }

    # Verifica se o nome da modalidade está no dicionário
    if modality_name not in modalities:
        raise ValueError(
            f"A modalidade '{modality_name}' não é válida. Modalidades disponíveis: {list(modalities.keys())}."
        )

    # Recupera o índice da modalidade
    modality_index = modalities[modality_name]

    # Cria o XPath dinâmico com base no índice da modalidade
    xpath = f'//*[@id="modSelect"]/option[{modality_index}]'

    # Chama a função para clicar no elemento com o XPath gerado
    call_element_by_xpath(xpath)


def select_data_theme(theme: str) -> None:
    """
    Localiza e interage com a tipo de arquivo com base no tema fornecido.

    Args:
    --------
        tema (str): O tema para o qual a fonte de dados será selecionada.

    Raises:
    --------
        ValueError: Se o tema fornecido não tiver um XPath associado.
    """

    # Dicionário que mapeia temas para seus respectivos xpaths
    THEME_XPATHS = {
        'TU': '//*[@id="tipo_arquivo"]/option[54]',  # Tema TUBE - Tuberculose
        # ...
        # Adicione mais temas e xpaths conforme necessário
    }

    # Obtém o xpath correspondente ao tema
    xpath = THEME_XPATHS.get(theme)

    # Verifica se o tema é válido e possui um xpath correspondente
    if xpath:
        call_element_by_xpath(xpath)
    else:
        raise ValueError(f"Tema '{theme}' não possui um XPath associado.")


def select_years_from_dropdown(years: list[str]) -> None:
    """
    Seleciona todos os anos disponíveis no menu de seleção de anos que estão na lista fornecida.
    Apenas os anos fornecidos na lista serão selecionados. Os anos que não estão na lista serão ignorados.

    Args:
    --------
        years (list of str): Lista de anos que devem ser verificados para seleção.
        driver (WebDriver): Instância do Selenium WebDriver usada para interagir com a página.

    Raises:
    --------
        ValueError: Se o elemento de seleção não for encontrado ou se ocorrer um erro ao interagir com ele.
    """
    import logging

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    from src.modules.webscraping.init.navigator import navigator as nav

    try:
        # Aguarde o dropdown estar visível e interagível
        dropdown = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="modAno"]'))
        )

        dropdown.click()

        # XPath base do menu de seleção de anos
        base_xpath = '//*[@id="modAno"]/option'

        # Aguarde até que o menu de seleção de anos esteja visível
        options_elements = WebDriverWait(nav, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, base_xpath))
        )

        # Lista para armazenar os anos que foram selecionados
        selected_years = []

        # Itera sobre todos os elementos de opção encontrados
        for option in options_elements:
            # Obtém o valor do atributo 'value' de cada opção
            year_value = option.get_attribute('value')

            # Verifica se o valor do ano está na lista de anos fornecidos
            if year_value in years:
                # Seleciona o ano clicando no elemento
                option.click()
                selected_years.append(year_value)
                logging.debug(f'Selecionado o ano: {year_value}')

        # Se nenhum ano da lista foi selecionado, levanta um erro
        if not selected_years:
            raise ValueError(
                'Nenhum ano da lista fornecida foi encontrado no menu de seleção.'
            )

    except Exception as e:
        nav.quit()
        raise ValueError(f'Erro ao verificar ou selecionar os anos: {e}')


def select_UF() -> None:
    """
    Localiza e interage com UF - BR disponivel
    """

    # Obtém o xpath correspondente a fonte dos dados SINAN
    call_element_by_xpath('//*[@id="moduf"]/option')


def request_data():

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    from src.modules.webscraping.init.navigator import navigator as nav

    # Clica em Enviar formulario e requisita arquivos
    call_element_by_xpath('//*[@id="dados_transferencia"]/button')

    # XPath do elemento que deve aparecer
    wait_element_xpath = '//*[@id="resultado"]/tbody/tr/td[1]'

    # Aguarde até que o elemento específico esteja visível
    WebDriverWait(nav, 10).until(
        EC.visibility_of_element_located((By.XPATH, wait_element_xpath))
    )

    # Faz requisicao de todos os para download
    call_element_by_xpath(
        '//*[@id="post-1492"]/div/div/section[2]/div/div[2]/div/div/div/p[2]/a'
    )

    # XPath do elemento que deve aparecer
    wait_element_xpath = '//*[@id="arquivo_compactado"]/p/a'

    href = None

    try:
        # Espera arquivos serem compactados e o elemento de download seja visivel
        element = WebDriverWait(nav, 100).until(
            EC.visibility_of_element_located((By.XPATH, wait_element_xpath))
        )

        # Captura o atributo 'href' do elemento
        href = element.get_attribute('href')
        if not href:
            raise ValueError(
                "O atributo 'href' não está presente no elemento."
            )

    except Exception as e:
        # Lida com exceções e registra o erro
        raise ValueError(f'Erro ao capturar o href do elemento: {e}')

    # Faz download dos arquivos
    call_element_by_xpath(wait_element_xpath)
