from utiles import obtener_color
import random
import itertools
from datetime import datetime
from gameconfig import config_main
from palabras_candidatas import obtener_diccionario_palabras_candidatas
from login_signup import main_login
from palabras import sin_acentos

# Variables globales
# CANTIDAD_LETRAS = 5
# CANTIDAD_INTENTOS = 5
CONFIGURACION_JUEGO = config_main()
CANTIDAD_LETRAS = CONFIGURACION_JUEGO['LONGITUD_PALABRA_SECRETA'][0]
CANTIDAD_INTENTOS = CONFIGURACION_JUEGO['MAXIMO_PARTIDAS'][0]
LISTA_ARCHIVOS = ["archivos/Cuentos.txt", "archivos/La araña negra - tomo 1.txt", "archivos/Las 1000 Noches y 1 Noche.txt"]


def crear_dict_info_jugadores(lista_jugadores):
    """
    Crea un diccionario cuyas claves son los nombres de los jugadores y los valores la
    información de cada uno.
    Cada clave jugador posee un diccionario con los puntos, posicion y los intentos que
    le toca jugar por partida.
    Retorna el diccionario.
    #Florencia Russo
    """
    dict_info_jugadores = {}
    for cantidad in range(len(lista_jugadores)):
        dict_info_jugadores[lista_jugadores[cantidad]] = {"puntos": 0,
                                                          "posicion": cantidad + 1}

    return dict_info_jugadores


def cambiar_posicion_jugadores(dict_info_jugadores):
    """
    Recibe un diccionario con informacion de los jugadores. Cambia las posiciones.
    #Florencia Russo
    """
    lista_posicion_jugadores = []
    posiciones_disponibles = []

    for jugador in dict_info_jugadores:
        lista_posicion_jugadores += [(jugador, dict_info_jugadores[jugador]['posicion'])]
        posiciones_disponibles.append(dict_info_jugadores[jugador]['posicion'])

    for jugador in dict_info_jugadores:
        posiciones_sin_jugador = posiciones_disponibles.copy()
        if dict_info_jugadores[jugador]['posicion'] in posiciones_disponibles:
            posiciones_sin_jugador.remove(dict_info_jugadores[jugador]['posicion'])
        nueva_posicion = random.choice(posiciones_sin_jugador)
        dict_info_jugadores[jugador]['posicion'] = nueva_posicion
        posiciones_disponibles.remove(nueva_posicion)


def dividir_turnos_jugadores(dict_jugadores, cantidad_turnos):
    """
    Recibe el diccionario de jugadores y la cantidad de turnos.
    Asigna el turno de cada jugador segun su posicion y los guarda en una lista.
    Retorna una lista con el nombre del jugador en la posición segun el turno que le toca jugar.
    #Florencia Russo
    """
    jugadores = sorted(dict_jugadores.items(), key=lambda jugador: jugador[1]['posicion'])
    jugadores = [jugador[0] for jugador in jugadores]
    le_toca = []
    toggle = itertools.cycle(jugadores)

    for turno in range(cantidad_turnos):
        le_toca += [next(toggle)]

    return le_toca


def ocultar_letras_no_adivinadas(palabra_adivinar, arriesgo, palabra_oculta):
    """
    Oculta las letras de la palabra que no estan en el arriesgo o no estan
    bien posicionadas y pone '? '
    #Florencia Russo
    """
    letras = ""
    lista_arriesgo = arriesgo.split(' ')
    palabra = palabra_oculta.split(' ')

    for letra in range(len(palabra_adivinar)):

        if obtener_color("Verde") not in lista_arriesgo[letra] and palabra[letra] == '?':
            letras += '? '
        else:
            letras += palabra_adivinar[letra] + ' '

    return letras


def crear_tablero():
    """
    Crea un tablero de todos '?' y es usado solo una vez
    al empezar el juego.
    #Ivan Teuber
    """
    tablero = []
    for i in range(CANTIDAD_INTENTOS):
        tablero.append('? ' * CANTIDAD_LETRAS)

    return tablero


def actualizar_tablero(tablero, intentos, arriesgo):
    """
    Actualiza el tablero segun el intento y el arriesgo recibido.
    Actualiza el tablero anterior, en el primer intento actualiza el original (crear_tablero)
    y en el ultimo intento actualiza el anteriormente actualizado.
    #Florencia Russo
    """
    tablero[intentos] = arriesgo

    return tablero


def imprimir_interfaz(palabra_adivinar, palabra_oculta, tablero, fin=False):
    """
    Imprime el tablero con el formato
        Palabra a adivinar:
        ? ? ? ? ?
        ? ? ? ? ?
        ? ? ? ? ?
        ? ? ? ? ?
        ? ? ? ? ?
        Arriesgo:
        #Ivan Teuber
    """
    print(f"Palabra a adivinar: {palabra_oculta}" if not fin
          else f"Palabra a adivinar: {palabra_adivinar}")

    for celda in tablero:
        print(celda)

    if fin:
        texto = ""
    else:
        texto = input("Arriesgo: ").upper()

    return texto


def selecciona_palabra():
    """
    Selecciona de forma aleatoria una palabra de la lista generada por el diccionario que contiene todas las palabras adecuadas de los archivos indicados.
    Retorna la palabra seleccionada.
    Florencia Russo
    """
    dict_palabras = obtener_diccionario_palabras_candidatas(LISTA_ARCHIVOS, CANTIDAD_LETRAS)
    lista = sorted(dict_palabras.keys(), key = lambda dict: dict[0])
    
    return lista[random.randint(0, len(lista))].upper()


def definir_victoria(arriesgo):
    """
    Recibe una palabra ya pintada (retorno de validar_aciertos) y valida si está toda en verde.
    Retorna True si la palabra esta en verde o False si alguna letra tiene otro color.
    #Facundo Talellis
    """
    cont = 0
    arriesgo = arriesgo.split(' ')
    estado_partida = False

    for i in arriesgo:
        if obtener_color("Verde") in i:
            cont += 1
    if cont == CANTIDAD_LETRAS:
        estado_partida = True

    return estado_partida


def contar_letras(palabra_adivinar):
    """
    Funcion auxiliar de (validar_aciertos), devuelve un diccionario
    con las letras de la palabra como claves y con valores = cantidad de veces
    que esa letra esta en la palabra.
    #Florencia Russo
    """
    diccionario = {}
    for letra in palabra_adivinar:
        if letra not in diccionario.keys():
            diccionario[letra] = 1
        else:
            diccionario[letra] += 1

    return diccionario


def validar_aciertos(palabra_adivinar, arriesgo):
    """
    Recibe la palabra a adivinar y la palabra ingresada por el usuario, ambas en mayusculas.
    Retorna la palabra arriesgada, cada letra con su color correspondiente segun
    si esta en la palabra a adivinar y en la posicion adecuada (verde),
    si aparece en la palabra a adivinar pero en otra posicion (amarillo)
    o si no esta en la palabra (gris oscuro).
    Cada letra esta separada por espacios para mejor lectura.
    #Florencia Russo
    """
    cantidad_letras = contar_letras(palabra_adivinar)
    palabra_pintada = ''

    for indice in range(CANTIDAD_LETRAS):
        if arriesgo[indice] == palabra_adivinar[indice]:
            palabra_pintada += obtener_color("Verde") + arriesgo[indice] + " "

        else:
            palabra_pintada += obtener_color("GrisOscuro") + arriesgo[indice] + " "

    for indice in range(CANTIDAD_LETRAS):
        if (arriesgo[indice] in palabra_adivinar and
                arriesgo[indice] != palabra_adivinar[indice] and
                ((palabra_pintada.count(obtener_color("Amarillo") + arriesgo[indice]) +
                  (palabra_pintada.count(obtener_color("Verde") + arriesgo[indice]))
                 ) < cantidad_letras[arriesgo[indice]])):
            palabra_pintada = palabra_pintada.replace(
                obtener_color("GrisOscuro") +
                arriesgo[indice], obtener_color("Amarillo") + arriesgo[indice], 1) + " "

    palabra_pintada += obtener_color("Defecto")

    return palabra_pintada


def validar_palabra(arriesgo):
    """
    La funcion recibe una palabra y verifica que sea de 5 letras y
    alpha, en caso contrario pide input hasta tener una palabra valida,
    luego de obtenerla le pasa la palabra a la funcion sacar_acentos y retorna
    lo que esta le de.
    #Maximo Utrera
    """
    while len(arriesgo) != CANTIDAD_LETRAS or not arriesgo.isalpha():
        if len(arriesgo) != CANTIDAD_LETRAS:
            print('Error, el arriezgo debe tener la misma cantidad '
                  'de letras que la palabra que se intenta adivinar')
        elif not arriesgo.isalpha():
            print('Error, el arriezgo deben ser todas letras')
        arriesgo = input("Arriesgo: ").upper()

    return (sin_acentos(arriesgo)).upper()

def puntos_jugadores(jugador_arranca, ganador, dict_jugadores, intentos):
    """
    Define cuantos puntos se le asigna a cada jugador por partida.
    Recibe el jugador que empieza la partida, quien fue el ganador ('' si no hubo),
     y el diccionario de jugadores.
    Acumula los puntos de la partida en la propiedad puntos del diccionario de cada jugador.
    Retorna una lista de tuplas.
    Cada tupla tiene al nombre del jugador en la primera posicion y los puntos de la partida
     en la segunda posicion.
    #Ruth Gomez - Facundo Talellis
    """
    diccionario = {1: 50, 2: 40, 3: 30, 4: 20, 5: 10}
    puntos_obtenidos_a = 100
    puntos_obtenidos_b = 50
    puntos_partida = []

    if ganador == '':  # no gano nadie
        for jugador in dict_jugadores:
            if jugador == jugador_arranca:
                dict_jugadores[jugador]['puntos'] -= puntos_obtenidos_a
                puntos_partida.append((jugador, (-puntos_obtenidos_a)))
            else:
                dict_jugadores[jugador]['puntos'] -= puntos_obtenidos_b
                puntos_partida.append((jugador, (-puntos_obtenidos_b)))
    else:
        for jugador in dict_jugadores:

            if jugador == ganador:
                dict_jugadores[jugador]['puntos'] += diccionario[intentos]
                puntos_partida.append((jugador, diccionario[intentos]))
            else:
                dict_jugadores[jugador]['puntos'] -= diccionario[intentos]
                puntos_partida.append((jugador, (-diccionario[intentos])))

    return puntos_partida


def seleccionar_ganador(dict_jugadores):
    """
    Elige al ganador del juego.
    Recibe el diccionario de jugadores. Lo ordena de mayor a menor por puntos.
    Retorna una tupla con el nombre y los datos del ganador.
    #Florencia Russo
    """
    return (sorted(dict_jugadores.items(), key=lambda jugador: jugador[1]['puntos'], reverse=True))[0]


def imprimir_puntos_partida(puntos_partida, dict_jugadores):
    """
    Recibe los puntos de la partida y el diccionario de jugadores.
    Imprime los puntos de la partida y los acumulados por cada jugador
    #Ruth Gomez - Facundo Talellis
    """
    for jugador in puntos_partida:
        nombre = jugador[0].upper()
        puntos_partida = jugador[1]
        puntos_totales = dict_jugadores[jugador[0]]['puntos']
        mensaje = f"{nombre} obtuviste un total de {puntos_partida} puntos," \
                  f" tenes acumulados {puntos_totales} puntos" if puntos_partida > 0 else \
            f"{nombre} perdiste un total de {-1 * puntos_partida} puntos," \
            f" tenes acumulados {puntos_totales} puntos"

        print(mensaje)


def logica_juego(dict_jugadores):
    """
    Recibe el diccionario de jugadorescomo parametro.
    Contiene la logica perteneciente a una partida de fiuble.
    #Florencia Russo - Ruth Gomez - Facundo Talellis - Ivan Teuber - Maximo Utrera
    """
    intentos = 0
    time_start = datetime.now()
    time_end = None
    palabra_adivinar = selecciona_palabra()
    palabra_oculta = "? " * CANTIDAD_LETRAS
    estado_partida = False
    lista_jugador = dividir_turnos_jugadores(dict_jugadores, CANTIDAD_INTENTOS)
    ganador = ''
    tablero = crear_tablero()
    while intentos < CANTIDAD_INTENTOS and not estado_partida:
        print("\nJuega", lista_jugador[intentos].upper())
        arriesgo = imprimir_interfaz(palabra_adivinar, palabra_oculta, tablero)
        arriesgo = validar_palabra(arriesgo)
        arriesgo = validar_aciertos(palabra_adivinar, arriesgo)
        palabra_oculta = ocultar_letras_no_adivinadas(palabra_adivinar, arriesgo, palabra_oculta)
        tablero = actualizar_tablero(tablero, intentos, arriesgo)
        estado_partida = definir_victoria(arriesgo)
        if estado_partida or (intentos == CANTIDAD_INTENTOS - 1):
            tablero = actualizar_tablero(tablero, intentos, arriesgo)
            imprimir_interfaz(palabra_adivinar, palabra_oculta, tablero, fin=True)
            time_end = datetime.now()
            if estado_partida:
                ganador = lista_jugador[intentos]
        intentos += 1

    delta_time = time_end - time_start
    mins = int(delta_time.total_seconds() / 60)
    secs = int(delta_time.total_seconds() - (60 * mins))
    puntos_partida = puntos_jugadores(lista_jugador[0], ganador, dict_jugadores, intentos)

    print(f'La palabra ha sido adivinada en {mins} minutos y {secs} segundos :)') \
        if estado_partida else print("La palabra no fue adivinada :(")

    imprimir_puntos_partida(puntos_partida, dict_jugadores)



def rejugabilidad():
    """
    Funcion principal que ejecuta el juego. Permite jugar multiples partidas(logica_juego)
    #Maximo Utrera
    """
    print('\n~ WELCOME TO WORDLE ~')
    jugadores = main_login()
    # jugadores = jugadores_usernames()
    dict_info_jugadores = crear_dict_info_jugadores(jugadores)
    jugar_denuevo = True

    while jugar_denuevo:
        logica_juego(dict_info_jugadores)
        desea_seguir = (input('Jugar de nuevo (S/N): ')).upper()
        while desea_seguir not in 'SN':
            desea_seguir = (input('Error solo se acepta (S/N): ')).upper()
        cambiar_posicion_jugadores(dict_info_jugadores)
        if desea_seguir == 'N':
            jugar_denuevo = False
            print('\nGracias por jugar!')
    ganador = seleccionar_ganador(dict_info_jugadores)
    print(f"El ganador es {ganador[0].upper()} con un total de {ganador[1]['puntos']} puntos")


rejugabilidad()