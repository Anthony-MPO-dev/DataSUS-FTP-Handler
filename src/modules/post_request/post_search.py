import logging
import os
from ftplib import FTP
from io import BytesIO

import requests
from bs4 import BeautifulSoup


def start_search_resquest(theme: str, years):
    try:
        path_raw = os.path.abspath(__file__).split('/src')[0] + '/src/data/raw'

        # URL para a requisição POST
        url_post = 'https://datasus.saude.gov.br/wp-content/ftp.php'

        # Payload para a requisição POST com múltiplos anos
        payload = {
            'tipo_arquivo[]': theme,
            'modalidade[]': '1',
            'fonte[]': 'SINAN',
            'ano[]': list(map(str, years)),
            'uf[]': 'BR',
        }

        # Diretório de destino para os arquivos baixados
        download_directory = path_raw

        # Criando o diretório de destino se não existir
        os.makedirs(download_directory, exist_ok=True)

        # Enviando a requisição POST
        response_post = requests.post(url_post, data=payload)

        # Verificando o status da requisição POST
        if response_post.status_code == 200:
            print('Requisição POST bem-sucedida!')
            # Parseando a resposta JSON
            response_json = response_post.json()

            # Iterando sobre cada item na resposta JSON
            for item in response_json:
                # Obtendo o link FTP do JSON
                link_html = item['link']
                # Usando BeautifulSoup para extrair o link real
                soup = BeautifulSoup(link_html, 'html.parser')
                ftp_link = soup.find('a')['href']

                # Extraindo informações do link FTP
                ftp_url = ftp_link.replace('ftp://', '')
                host, path = ftp_url.split('/', 1)
                file_name = path.split('/')[-1]

                # Conectando ao servidor FTP
                ftp = FTP(host)
                ftp.login()  # Login anônimo

                # Baixando o arquivo
                with BytesIO() as file:
                    ftp.retrbinary(f'RETR {path}', file.write)
                    file.seek(0)

                    # Caminho completo do arquivo a ser salvo
                    file_path = os.path.join(download_directory, file_name)

                    # Salvando o arquivo localmente
                    with open(file_path, 'wb') as local_file:
                        local_file.write(file.read())

                ftp.quit()
                logging.info(
                    f"Download do arquivo '{file_name}' concluído com sucesso em {file_path}!"
                )
        else:
            raise ValueError(
                f'Erro na requisição POST: {response_post.status_code}'
            )

    except Exception as e:
        raise ValueError(f'Erro durante start_search_request{e}')
