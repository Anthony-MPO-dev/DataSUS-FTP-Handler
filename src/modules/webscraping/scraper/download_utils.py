import logging
import os
import time

import requests


def monitor_download_progress(expected_size):
    """
    Monitora o progresso do download de arquivos .crdownload no diretório especificado.

    Args:
    --------
        download_dir (str): Diretório onde os arquivos .crdownload são salvos.
        expected_size (int): Tamanho total esperado do arquivo em bytes.
    """

    download_dir = 
    while True:
        files = [f for f in os.listdir(download_dir) if f.endswith('.crdownload')]
        if not files:
            logging.info("Download completo!")
            break

        for file in files:
            file_path = os.path.join(download_dir, file)
            try:
                file_size = os.path.getsize(file_path)
                percent_complete = (file_size / expected_size) * 100
                logging.info(f"Progresso do download: {percent_complete:.2f}%")
            except FileNotFoundError:
                logging.info("Arquivo não encontrado.")
                continue
        
        time.sleep(1)  # Aguarde um segundo antes de verificar novamente

def get_file_size(url):
    """
    Obtém o tamanho do arquivo a partir da URL fornecida.

    Args:
    --------
        url (str): URL do arquivo.

    Returns:
    --------
        int: Tamanho do arquivo em bytes.

    Raises:
    --------
        ValueError: Se não for possível obter o tamanho do arquivo.
    """
    response = requests.head(url)
    if 'Content-Length' in response.headers:
        return int(response.headers['Content-Length'])
    else:
        raise ValueError("Não foi possível obter o tamanho do arquivo.")
