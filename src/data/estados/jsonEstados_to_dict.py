import json
import os


def return_estado_dict_lat_long():
    try:
        path = os.path.abspath(__file__).split('/src')[0]
        json_path = os.path.join(
            path, 'src', 'data', 'estados', 'estados.json'
        )

        # Carregando o JSON a partir de um arquivo com utf-8-sig
        with open(json_path, 'r', encoding='utf-8-sig') as file:
            json_data = json.load(file)

        # Alterando para armazenar um dicionário com chaves latitude e longitude
        uf_dict = {
            item['codigo_uf']: {
                'latitude': item['latitude'],
                'longitude': item['longitude'],
            }
            for item in json_data
        }

        return uf_dict

    except Exception as e:
        raise ValueError(f'Erro ao carregar o arquivo JSON: {str(e)}')
