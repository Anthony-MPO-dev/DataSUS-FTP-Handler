import os

import pandas as pd

from src.data.estados.jsonEstados_to_dict import return_estado_dict_lat_long
from src.data.municipios.dfMunicipios_to_dict import (
    return_municipio_dict_lat_long,
)


def insere_lat_long_municipios(df):

    # Função para extrair a latitude de um município
    def get_latitude_municipio(codigo):
        return municipios_dict[int(codigo)]['LATITUDE']

    # Função para extrair a longitude de um município
    def get_longitude_municipio(codigo):
        return municipios_dict[int(codigo)]['LONGITUDE']

    municipios_dict = return_municipio_dict_lat_long()

    # Usando apply para criar as colunas Latitude_Municipio e Longitude_Municipio
    df['LAT_MUNIC'] = df['ID_MN_RESI'].apply(get_latitude_municipio)
    df['LONG_MUNIC'] = df['ID_MN_RESI'].apply(get_longitude_municipio)

    return df


def insere_lat_long_estados(df):

    # Função para extrair a latitude de um município
    def get_latitude_estado(codigo):
        return uf_dict[int(codigo)]['latitude']

    # Função para extrair a longitude de um município
    def get_longitude_estado(codigo):
        return uf_dict[int(codigo)]['longitude']

    uf_dict = return_estado_dict_lat_long()

    # Usando apply para criar as colunas Latitude e Longitude
    df['LAT_UF'] = df['SG_UF_NOT'].apply(get_latitude_estado)
    df['LONG_UF'] = df['SG_UF_NOT'].apply(get_longitude_estado)

    return df


def inserir_latitude_e_longitude(file_path):

    df = pd.read_parquet(file_path)

    df = insere_lat_long_estados(df)

    df = insere_lat_long_municipios(df)

    file_path = (
        os.path.abspath(__file__).split('/src')[0]
        + '/src/data/output/unified_datasus_data.parquet'
    )

    df.to_parquet(file_path)
