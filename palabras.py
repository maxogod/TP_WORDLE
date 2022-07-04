import unicodedata

def sin_acentos(arriesgo):
    """
    Recibe una palabra. Reemplaza las vocales con acentos. Retorna la misma palabra sin acentos.
    #Ruth Gomez
    """

    arrieesgo_sin_acento = ''
    for c in unicodedata.normalize('NFKD', arriesgo):
        if unicodedata.category(c) != 'Mn':
            arrieesgo_sin_acento += c
    return arrieesgo_sin_acento.upper()