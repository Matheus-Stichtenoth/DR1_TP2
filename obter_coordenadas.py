coodernadas_estados = {
    'RS': {'latitude': -30.0346, 'longitude': -51.2177},
    'SP': {'latitude': -23.5505, 'longitude': -46.6333},
    'MG': {'latitude': -19.9167, 'longitude': -43.9345}
}

def obter_coordenadas(estado):
    return coodernadas_estados.get(estado, {'latitude': None, 'longitude': None})