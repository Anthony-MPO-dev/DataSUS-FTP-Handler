import logging
import os
import time

from src.modules.webscraping.init.configs import (
    path_raw,
    save_browser_mode_to_config,
)
from src.modules.webscraping.scraper.element_selector import (
    request_data,
    select_data_source,
    select_data_theme,
    select_modality,
    select_UF,
    select_years_from_dropdown,
)


def monitor_download_progress(expected_size):

    download_dir = path_raw

    while True:
        files = [
            f for f in os.listdir(download_dir) if f.endswith('.crdownload')
        ]
        if not files:
            logging.info('Download completo!')
            break

        for file in files:
            file_path = os.path.join(download_dir, file)
            try:
                file_size = os.path.getsize(file_path)
                percent_complete = (file_size / expected_size) * 100
                logging.info(f'Progresso do download: {percent_complete:.2f}%')
            except FileNotFoundError:
                logging.info('Arquivo não encontrado.')
                continue

        time.sleep(1)  # Aguarde um segundo antes de verificar novamente


def start_search(theme: str, browser_mode: str, years: list[int]):

    # configura o modo do browser_mode antes de iniciar
    save_browser_mode_to_config(browser_mode)

    # Seleciona o campo da fonte de dados SINAN
    select_data_source()

    # seleciona modalidade Dados
    select_modality()

    select_data_theme(theme)

    # converte inteiros em strings
    years_str = list(map(str, years))
    select_years_from_dropdown(years_str)

    # Seleciona campo BR dentro de UF
    select_UF()

    # Requisita os arquivos e faz o download deles
    request_data()

    import time

    time.sleep(180)
