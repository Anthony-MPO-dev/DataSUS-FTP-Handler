import logging
import os

import pandas as pd

from src.modules.data_processing.corrige_codigos_municipio import (
    trata_codigos_municipio,
)
from src.modules.data_processing.insere_lat_long import (
    inserir_latitude_e_longitude,
)
from src.modules.data_processing.remove_breakLines import (
    remover_quebras_linha_arquivos_datasus,
)


def trata_colunas_e_linhas_duplicadas(files_path, parquet_file_path):
    first_time = True  # Flag para verificar se é a primeira vez que os dados são carregados

    try:

        for nome_arquivo in os.listdir(files_path):
            if nome_arquivo.lower().endswith('.csv'):
                file_path = files_path + '/' + nome_arquivo

                # Remover quebras de linha
                remover_quebras_linha_arquivos_datasus(file_path, nome_arquivo)

                # Caminho para o arquivo CSV após a remoção das quebras de linha
                cleaned_file_path = file_path

                # Carregar o CSV em um DataFrame
                try:
                    df = pd.read_csv(cleaned_file_path, low_memory=False)

                    # Converte todas as colunas para string para evitar problemas com tipos mistos
                    for col in df.columns:
                        df[col] = df[col].astype(str)

                    if not first_time:

                        # Ler o arquivo Parquet existente
                        merged_df = pd.read_parquet(parquet_file_path)

                        # Concatenar o DataFrame atual com o existente
                        merged_df = pd.concat(
                            [merged_df, df], ignore_index=True
                        )
                        # Salvar o novo DataFrame concatenado

                        # Obter os nomes das colunas que começam com "Unnamed"
                        colunas_remover = [
                            coluna
                            for coluna in merged_df.columns
                            if coluna.startswith('Unnamed')
                        ]

                        # Remover as colunas do dataframe
                        merged_df = merged_df.drop(colunas_remover, axis=1)

                        # ==========================================================================
                        logging.info('Verificando colunas duplicadas')
                        # Verificar colunas com nomes duplicados
                        colunas_duplicadas = merged_df.columns[
                            merged_df.columns.duplicated()
                        ]
                        if len(colunas_duplicadas) > 0:
                            logging.info(colunas_duplicadas)

                            # Remover colunas com nomes duplicados, mantendo apenas a primeira ocorrência
                            merged_df = merged_df.loc[
                                :, ~merged_df.columns.duplicated()
                            ]

                        # ==========================================================================
                        # Identificar as linhas duplicadas
                        duplicatas = merged_df[
                            merged_df.duplicated(keep=False)
                        ]

                        logging.info('Verificando Linhas Duplicadas:')
                        # Imprimir as linhas duplicadas com o número da linha
                        if not duplicatas.empty:
                            logging.info('Linhas duplicadas:')
                            logging.warning(duplicatas)
                            logging.warning(
                                'Total duplicadas: {}'.format(len(duplicatas))
                            )

                            # Remover as duplicatas, mantendo apenas a primeira ocorrência
                            merged_df = merged_df.drop_duplicates(keep=False)

                            logging.info(
                                'Salvando dataframe tratado resultante em parquet...'
                            )
                            # Salvar o DataFrame sem duplicatas em um novo arquivo parquet

                        # ==========================================================================

                        merged_df.to_parquet(parquet_file_path)

                        logging.info('\n')
                        logging.info(
                            f'Arquivo atualmente com {len(merged_df)} linhas'
                        )
                        logging.info('\n')
                        os.remove(file_path)
                        logging.info(
                            f"Arquivo CSV '{nome_arquivo}' deletado com sucesso."
                        )

                    else:

                        # Salvar como Parquet
                        df.to_parquet(parquet_file_path)
                        logging.info(
                            f"Arquivo '{nome_arquivo}' convertido para Parquet com sucesso: '{parquet_file_path}'"
                        )
                        first_time = False

                        # Deletar o arquivo CSV original
                        os.remove(file_path)
                        logging.info(
                            f"Arquivo CSV '{nome_arquivo}' deletado com sucesso."
                        )

                except Exception as e:
                    raise ValueError(
                        f"Erro ao converter o arquivo '{nome_arquivo}' para Parquet: {e} in {parquet_file_path}"
                    )
    except Exception as e:
        raise ValueError(f'Erro durante tratamento dos dados: {e}')


def cleaning_data(files_path: str):
    """
    Remove quebras de linha dos arquivos CSV e converte para formato Parquet.

    Parâmetros:
    files_path (str): Caminho para o diretório contendo os arquivos CSV.
    """

    try:

        # Caminho de saída para o arquivo Parquet
        parquet_file_path = files_path + '/' + 'unified_data.parquet'

        trata_colunas_e_linhas_duplicadas(files_path, parquet_file_path)

        trata_codigos_municipio(parquet_file_path, parquet_file_path)

        inserir_latitude_e_longitude(parquet_file_path)

    except Exception as e:
        raise ValueError(f'Erro ao limpar os dados: {e}')
