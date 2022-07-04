
def read_config_file(config):
    # Esta funcion puede ser reemplazada si ya hay una que lee archivos,
    # Pero atencion con el return de los dos vacios
    # Maximo Utrera
    line = config.readline()
    return line.rstrip("\n").split(",") if line else ['','']


def config_dic_mod(config_file, config_dic):
    """
    Modifica y devuelve el diccionario config_dic que obtiene,
    en base a el archivo config_file que recibe abierto, sino puede
    no modificara cierta configuracion.
    Maximo Utrera
    """
    min_long_palabra = 3
    max_long_palabra = 15
    min_max_partida = 2
    max_max_partida = 10
    try:
        config, value = read_config_file(config_file)
    except ValueError:
        config, value = ['', '']

    while config:
        if config == 'LONGITUD_PALABRA_SECRETA':
            if min_long_palabra <= int(value) <= max_long_palabra:
                config_dic['LONGITUD_PALABRA_SECRETA'] = [int(value), 'por config.']

        elif config == 'MAXIMO_PARTIDAS':
            if min_max_partida <= int(value) <= max_max_partida:
                config_dic['MAXIMO_PARTIDAS'] = [int(value), 'por config.']

        elif config == 'REINICIAR_ARCHIV0_PARTIDAS':
            if value == 'False':
                config_dic['REINICIAR_ARCHIV0_PARTIDAS'] = [False, 'por config.']
            elif value == 'True':
                config_dic['REINICIAR_ARCHIV0_PARTIDAS'] = [True, 'por config.']

        try:
            config, value = read_config_file(config_file)
        except ValueError:
            config, value = ['', '']

    return config_dic

def config_main():
    """
    retorna lo que obtenga de config_dic_mod, en caso que no se pueda
    acceder al archivo config_file.csv retorna un dic de config por default.
    Maximo Utrera
    """
    config_default = {'LONGITUD_PALABRA_SECRETA': [5, 'por default.'],
                  'MAXIMO_PARTIDAS': [5, 'por default.'],
                  'REINICIAR_ARCHIV0_PARTIDAS': [False, 'por default.']}
    config_final = {}
    try:
        with open("config_file.csv") as config:
            config_final = config_dic_mod(config, config_default)
    except FileNotFoundError:
        config_final = config_default
    return config_final
