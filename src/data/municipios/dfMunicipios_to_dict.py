import os

import pandas as pd


def return_municipio_dict_lat_long():

    try:

        # Função para transformar o DataFrame em um dicionário
        def criar_dicionario_geocodigos(df):
            # Criar um dicionário onde cada chave é o GEOCODIGO_MUNICIPIO
            # e o valor é outro dicionário com LATITUDE e LONGITUDE
            dicionario_geocodigos = df.set_index('GEOCODIGO_MUNICIPIO')[
                ['LATITUDE', 'LONGITUDE']
            ].to_dict(orient='index')
            return dicionario_geocodigos

        path = os.path.abspath(__file__).split('/src')[0]

        df_path = path + '/src/data/municipios/municipios_lat_long.csv'

        df = pd.read_csv(df_path)

        dicionario_geocodigos = criar_dicionario_geocodigos(df)

        # Criar o dicionário a partir do DataFrame
        return dicionario_geocodigos

    except Exception as e:
        raise ValueError(
            f'Erro ao carregar o dicionário de geocodigos dos municípios: {e}'
        )
