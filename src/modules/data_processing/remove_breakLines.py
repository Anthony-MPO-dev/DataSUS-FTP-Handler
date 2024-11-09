import csv
import logging
import re

from unidecode import unidecode


def remover_quebras_linha_arquivos_datasus(file_path, file_name):
    """
    Multi-line docstring summary.

    # Remove quebras de linha e tabulações de um arquivo datasus CSV.

    # Args:
    ---------
        file_path (str): O caminho para o arquivo CSV a ser ajustado.

    Retorno
    --------
        None
    """
    lines = []
    logging.info(f'Removendo quebras de linha ARQUIVOS DATASUS! [{file_name}]')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                corrected_row = [re.sub(r'[\n\t]+', ' ', cell) for cell in row]
                normalized_row = [unidecode(cell) for cell in corrected_row]
                lines.append(normalized_row)

        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file, delimiter=',')
            csv_writer.writerows(lines)

    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin1') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                corrected_row = [re.sub(r'[\n\t]+', ' ', cell) for cell in row]
                normalized_row = [unidecode(cell) for cell in corrected_row]
                lines.append(normalized_row)

        with open(file_path, 'w', encoding='latin1', newline='') as file:
            csv_writer = csv.writer(file, delimiter=',')
            csv_writer.writerows(lines)

    except Exception as e:
        raise ValueError(f'Erro ao remover quebras de linha DATASUS:\n', e)
