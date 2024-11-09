import logging
import os

import dbfread  # Usado para ler arquivos DBF
import pandas as pd
from pyreaddbc import dbc2dbf


def converter_dbc_para_dbf(diretorio_entrada, diretorio_saida):
    """
    Converte todos os arquivos DBC em um diretório para DBF e salva no diretório de saída.

    Parâmetros:
    diretorio_entrada (str): Caminho para o diretório contendo arquivos DBC.
    diretorio_saida (str): Caminho para o diretório onde os arquivos DBF serão salvos.
    """
    os.makedirs(diretorio_saida, exist_ok=True)

    for nome_arquivo in os.listdir(diretorio_entrada):
        if nome_arquivo.lower().endswith('.dbc'):
            caminho_entrada = os.path.join(diretorio_entrada, nome_arquivo)
            nome_arquivo_dbf = os.path.splitext(nome_arquivo)[0] + '.dbf'
            caminho_saida = os.path.join(diretorio_saida, nome_arquivo_dbf)

            try:
                dbc2dbf(caminho_entrada, caminho_saida)
                logging.info(
                    f"Arquivo DBC '{nome_arquivo}' convertido para DBF com sucesso."
                )
            except Exception as e:
                raise ValueError(
                    f"Erro ao converter o arquivo DBC '{nome_arquivo}' para DBF: {e}"
                )


def converter_dbf_para_csv(diretorio_entrada, diretorio_saida):
    """
    Converte todos os arquivos DBF em um diretório para CSV e salva no diretório de saída.

    Parâmetros:
    diretorio_entrada (str): Caminho para o diretório contendo arquivos DBF.
    diretorio_saida (str): Caminho para o diretório onde os arquivos CSV serão salvos.
    """
    os.makedirs(diretorio_saida, exist_ok=True)

    sucesso = False  # Flag para verificar se todos os arquivos foram convertidos com sucesso

    try:
        for nome_arquivo in os.listdir(diretorio_entrada):
            if nome_arquivo.lower().endswith('.dbf'):
                caminho_entrada = os.path.join(diretorio_entrada, nome_arquivo)
                nome_arquivo_csv = os.path.splitext(nome_arquivo)[0] + '.csv'
                caminho_saida = os.path.join(diretorio_saida, nome_arquivo_csv)

                try:
                    # Lê o arquivo DBF e converte para DataFrame
                    tabela = dbfread.DBF(caminho_entrada, encoding='latin1')
                    df = pd.DataFrame(iter(tabela))
                    # Salva o DataFrame como CSV
                    df.to_csv(caminho_saida, index=False)
                    logging.info(
                        f"Arquivo DBF '{nome_arquivo}' convertido para CSV com sucesso."
                    )
                except Exception as e:
                    raise ValueError(
                        f"Erro ao converter o arquivo DBF '{nome_arquivo}' para CSV: {e}"
                    )

        sucesso = True  # Flag para verificar se todos os arquivos foram convertidos com sucesso
    finally:
        # Verifica a flag para deletar os arquivos .dbf se todas as conversões tiverem sido bem-sucedidas
        if sucesso:
            for nome_arquivo in os.listdir(diretorio_entrada):
                if nome_arquivo.lower().endswith('.dbf'):
                    caminho_arquivo = os.path.join(
                        diretorio_entrada, nome_arquivo
                    )
                    try:
                        os.remove(caminho_arquivo)
                        logging.info(
                            f"Arquivo DBF '{nome_arquivo}' deletado com sucesso."
                        )
                    except Exception as e:
                        raise ValueError(
                            f"Erro ao deletar o arquivo DBF '{nome_arquivo}': {e}"
                        )
