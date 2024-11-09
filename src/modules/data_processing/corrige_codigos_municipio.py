import logging
import sys
import time

import pandas as pd
import requests
from requests.exceptions import ConnectionError, Timeout


def trata_codigos_municipio(file_path, final_path):
    try:

        # URL para buscar a lista de municípios
        url_municipios = (
            'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
        )

        # Número máximo de tentativas em caso de falha de conexão
        max_retries = 5

        # Função para fazer requisições com retry
        def fazer_requisicao(url):
            tentativa = 0
            while tentativa < max_retries:
                try:
                    response = requests.get(
                        url, timeout=10
                    )  # Timeout definido para 10 segundos
                    if response.status_code == 200:
                        return response
                    else:
                        logging.warning(
                            f'Erro na requisição: {response.status_code}'
                        )
                except (ConnectionError, Timeout) as e:
                    tentativa += 1
                    logging.warning(
                        f'Erro de conexão, tentativa {tentativa}/{max_retries}: {e}'
                    )
                    time.sleep(
                        2**tentativa
                    )  # Exponencial backoff: 2, 4, 8, 16, 32 segundos
            raise ConnectionError(f'Falha após {max_retries} tentativas')

        # Obter a lista de municípios
        response_municipios = fazer_requisicao(url_municipios)

        if response_municipios:
            municipios_data = response_municipios.json()

            import json

            # logging.infoar o JSON formatado para verificar os campos disponíveis
            # Salvar o JSON em um arquivo
            # with open('municipios_data.json', 'w') as json_file:
            #     json.dump(municipios_data, json_file, indent=4)
            # sys.exit(1)
        else:
            raise ValueError('Erro ao obter lista de municípios')

        # Criar um dicionário para mapear códigos incompletos para códigos completos
        codigo_municipio_completo = {}
        nome_municipio = {}
        siglas_estados = {}
        regiao_municipio = {}
        for municipio in municipios_data:
            cod_municipio_completo = str(municipio['id'])
            municip = municipio['nome']
            sigla_estado = municipio['microrregiao']['mesorregiao']['UF'][
                'sigla'
            ]

            regiao_nome = municipio['microrregiao']['mesorregiao']['UF']['regiao']['nome']

            cod_municipio_incompleto = cod_municipio_completo[:6]
            codigo_municipio_completo[
                cod_municipio_incompleto
            ] = cod_municipio_completo

            # Mapear código do município para a sua região
            regiao_municipio[cod_municipio_completo] = regiao_nome

            # Adicione nome municipio no dicionario
            nome_municipio[cod_municipio_completo] = municip

            # Adicionando a sigla do estado no dicionário
            siglas_estados[cod_municipio_completo] = sigla_estado

        # Ler o arquivo PARQUET em um DataFrame
        df = pd.read_parquet(file_path)

        # Verificar os primeiros registros para conferir a leitura
        logging.info('Dados antes da substituição:')
        logging.info(df.head())

        # Substituir códigos incompletos pelo código completo correspondente
        def substituir_codigo(codigo_incompleto):
            return codigo_municipio_completo.get(
                codigo_incompleto, codigo_incompleto
            )

        indices_incorretos = []

        # Função modificada para salvar o índice da linha com o código incorreto
        def verificar_codigo(codigo, index):
            # Verificar se o código não está presente no dicionário
            if codigo not in nome_municipio:
                indices_incorretos.append(
                    index
                )  # Salvar o índice em vez do valor do código
                # logging.info(f'Código incompleto na linha {index}: {codigo}')

        # Função para corrigir o código incorreto copiando o valor de outra coluna
        def corrigir_codigo_completo(df, coluna_de_origem, coluna_auxiliar):
            for index in indices_incorretos:
                # Substituir o valor de 'ID_MUNICIP' pelo valor correspondente de 'ID_MN_RESI'
                codigo_correto = df.at[index, coluna_auxiliar]
                logging.debug(
                    f'Corrigindo linha {index}: substituindo {df.at[index, coluna_de_origem]} por {codigo_correto}'
                )
                df.at[index, coluna_de_origem] = codigo_correto
            return df

        # Função para remover as linhas com índices incorretos
        def remover_linhas_incorretas(df, indices_incorretos):
            # Remover as linhas do DataFrame com base na lista de índices
            df = df.drop(indices_incorretos)
            # Resetar o índice do DataFrame para manter a consistência
            df = df.reset_index(drop=True)
            logging.info(
                f'Removidas {len(indices_incorretos)} linhas com códigos incorretos.'
            )
            return df

        def add_nome(codigo_municip):
            return nome_municipio.get(codigo_municip, codigo_municip)

        def add_sigla(codigo_municip):
            return siglas_estados.get(codigo_municip, codigo_municip)
        
        def add_regiao(codigo_municip):
            return regiao_municipio.get(codigo_municip, codigo_municip)
        
        # Substituir códigos incompletos pelo completo, e tratar nulos
        def substituir_codigo(codigo_incompleto):
            return codigo_municipio_completo.get(codigo_incompleto, codigo_incompleto)

        # Ajustes nas colunas de códigos de município para garantir a conversão correta
        for coluna in ['ID_MUNICIP', 'ID_MN_RESI']:
            df[coluna] = df[coluna].astype(str).str.replace(r'\.0$', '', regex=True).apply(substituir_codigo)

        # df['ID_MUNICIP'] = df['ID_MUNICIP'].astype('Int64')
        # df['ID_MUNICIP'] = df['ID_MUNICIP'].astype(str)
        # df['ID_MUNICIP'] = df['ID_MUNICIP'].apply(substituir_codigo)

        # Aplicar a função ao DataFrame usando apply e passando o índice como parâmetro
        df.apply(
            lambda row: verificar_codigo(row['ID_MUNICIP'], row.name), axis=1
        )

        if indices_incorretos:
            logging.info('Codigos incorretos em ID_MUNICIP')
            # Aplicar a função para corrigir os códigos incorretos
            df = corrigir_codigo_completo(df, 'ID_MUNICIP', 'ID_MN_RESI')

        indices_incorretos = []

        # df['ID_MN_RESI'] = df['ID_MN_RESI'].astype('Int64')
        # df['ID_MN_RESI'] = df['ID_MN_RESI'].astype(str)
        # df['ID_MN_RESI'] = df['ID_MN_RESI'].apply(substituir_codigo)
        # Aplicar a função ao DataFrame usando apply e passando o índice como parâmetro

        df.apply(
            lambda row: verificar_codigo(row['ID_MN_RESI'], row.name), axis=1
        )

        if indices_incorretos:
            logging.info('Codigos incorretos em ID_MN_RESI')
            # Aplicar a função para corrigir os códigos incorretos
            df = corrigir_codigo_completo(df, 'ID_MN_RESI', 'ID_MUNICIP')

        indices_incorretos = []

        # Ultima verificação de indices incorretos na coluna ID_MN_RESI
        df.apply(
            lambda row: verificar_codigo(row['ID_MN_RESI'], row.name), axis=1
        )

        # Aplicar a função para remover as linhas incorretas
        df = remover_linhas_incorretas(df, indices_incorretos)

        df['NOME_MUNIC'] = df['ID_MN_RESI'].apply(add_nome)

        df['SIGLA_UF'] = df['ID_MN_RESI'].apply(add_sigla)

        df['REGIAO'] = df['ID_MN_RESI'].apply(add_regiao)

        # Adiciona numero 1 em todas as linhas da coluna para simbolizar o caso e servir como agrupador futuramente
        df['NumeroCasos'] = 1

        # Lista de colunas que você quer reorganizar no início
        colunas_ordenadas = [
            'NumeroCasos', 'ID_MN_RESI', 'DT_NOTIFIC', 'NOME_MUNIC', 'SIGLA_UF', 'REGIAO'
        ]

        # Adiciona as colunas restantes (não listadas) mantendo a ordem original
        colunas_restantes = [col for col in df.columns if col not in colunas_ordenadas]

        # Reorganiza o DataFrame com as colunas na ordem desejada
        df = df.reindex(columns=colunas_ordenadas + colunas_restantes)


        # Verificar os primeiros registros após a substituição
        logging.info('Dados após a substituição:')
        logging.info(df.head())

        # Salvar o DataFrame atualizado em um novo arquivo PARQUET
        df.to_parquet(final_path)

        logging.info('Arquivo PARQUET atualizado com sucesso!')

    except Exception as e:
        raise ValueError(f'Erro durante a execução: {e}')
