from utiles import obtener_color, obtener_palabras_validas
import random
from datetime import datetime

#Variables globales
CANTIDAD_LETRAS = 5
CANTIDAD_INTENTOS = 5

def ocultar_letras_no_adivinadas(palabra_adivinar, arriesgo, palabra_oculta):
    """
    Oculta las letras de la palabra que no estan en el arriesgo o no estan
    bien posicionadas y pone '? '
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
    """
    tablero = []
    for i in range(CANTIDAD_LETRAS):
        tablero.append('? '*CANTIDAD_LETRAS)
    
    return tablero

def actualizar_tablero(tablero, intentos, arriesgo):
    """
    actualiza el tablero anterior, en el primer intento actualiza el original (crear_tablero)
    y en el ultimo intento actualiza el anteriormente actualizado.
    """

    tablero[intentos] = arriesgo
    
    return tablero

def imprimir_interfaz(palabra_adivinar, palabra_oculta, tablero, fin = False):
    #Me gusta más esta versión como imprime el arriesgo final que la que está en el pdf del TP.
    #Habría que ver si nos dejan que sea un poquito distinta a lo que muestra la consigna.
    #De ultima la cambiamos para la segunda parte.
    
    print(f"Palabra a adivinar: {palabra_oculta}" if not fin
          else f"palabra a adivinar: {palabra_adivinar}")

    for celda in tablero:
        print(celda)

    if fin:
        texto = ""
    else:
        texto = input("Arriesgo: ").upper()

    return texto

def selecciona_palabra():
    lista=obtener_palabras_validas()
    return lista[random.randint(0, len(lista))].upper()

def definir_victoria(arriesgo):
    cont=0
    arriesgo = arriesgo.split(' ')
    estado_partida = False

    for i in arriesgo:
        if obtener_color("Verde") in i:
            cont+=1
    if cont==CANTIDAD_LETRAS:
        estado_partida = True

    return estado_partida

def contar_letras(palabra_adivinar):
    """
    Funcion ayudante de (validar_aciertos), devuelve un diccionario
    con las letras de la palabra como claves y con valores = cantidad de veces
    que esa letra esta en la palabra.
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
    """
    cantidad_letras = contar_letras(palabra_adivinar)
    palabra_pintada = ''

    for indice in range(len(arriesgo)):           
        if arriesgo[indice] == palabra_adivinar[indice]:
            palabra_pintada += obtener_color("Verde") + arriesgo[indice] +  " "
    
        else:
            palabra_pintada += obtener_color("GrisOscuro") + arriesgo[indice] + " "

    for indice in range(len(arriesgo)):
        if (arriesgo[indice] in palabra_adivinar and
                arriesgo[indice] != palabra_adivinar[indice] and
                ((palabra_pintada.count(obtener_color("Amarillo") + arriesgo[indice]) +
                  (palabra_pintada.count(obtener_color("Verde") + arriesgo[indice]))
                 ) < cantidad_letras[arriesgo[indice]])):
            palabra_pintada = palabra_pintada.replace(
                obtener_color("GrisOscuro") +
                arriesgo[indice], obtener_color("Amarillo") + arriesgo[indice], 1) +  " "
    
    palabra_pintada += obtener_color("Defecto")

    return palabra_pintada

def validar_palabra(arriesgo):
    """
    La funcion recibe una palabra y verifica que sea de 5 letras y
    alpha, en caso contrario pide input hasta tener una palabra valida,
    luego de obtenerla le pasa la palabra a la funcion sacar_acentos y retorna
    lo que esta le de.
    """

    while len(arriesgo) != CANTIDAD_LETRAS or not arriesgo.isalpha():
        if len(arriesgo) != CANTIDAD_LETRAS:
            print('Error, el arriezgo debe tener la misma cantidad '
                  'de letras que la palabra que se intenta adivinar')
        elif not arriesgo.isalpha():
            print('Error, el arriezgo deben ser todas letras')
        arriesgo = input("Arriesgo: ").upper()

    return (sin_acentos(arriesgo)).upper()

def sin_acentos(arriesgo):
    #Me parece mejor esta versión que la otra con dos for. 
    #Voy a inverstigar lo que nos comentó el profe de la resta de codigos ASCII,
    #pero para la primera entrega me parece que esta quedaría mejor.
    #La propongo para la segunda parte lo del ASCII.

    vocales = 'áéíóú'
    vocales_1 = 'aeiou'
    palabra_1 = arriesgo.lower()
    for letra in palabra_1:
        if letra == vocales[0]:
            palabra_1 = palabra_1.replace(letra,vocales_1[0])
        elif letra == vocales[1]:
            palabra_1 = palabra_1.replace(letra,vocales_1[1])
        elif letra == vocales[2]:
            palabra_1 = palabra_1.replace(letra,vocales_1[2])
        elif letra == vocales[3]:
            palabra_1 = palabra_1.replace(letra,vocales_1[3])
        elif letra == vocales[4]:
            palabra_1 = palabra_1.replace(letra,vocales_1[4])
        else:
            pass

    return palabra_1.upper()


def logica_juego():
    """
    main loop del juego, esta funcion empieza cuando comienza el juego
    y termina cuando termina el juego.
    """

    intentos = 0
    time_start = datetime.now()
    palabra_adivinar = selecciona_palabra()
    palabra_oculta = "? " * CANTIDAD_LETRAS
    estado_partida = False
    tablero = crear_tablero()

    while intentos < CANTIDAD_INTENTOS and not estado_partida:
        arriesgo = imprimir_interfaz(palabra_adivinar, palabra_oculta, tablero)
        arriesgo = validar_palabra(arriesgo)
        arriesgo = validar_aciertos(palabra_adivinar, arriesgo)
        palabra_oculta = ocultar_letras_no_adivinadas(palabra_adivinar, arriesgo, palabra_oculta)
        tablero = actualizar_tablero(tablero, intentos, arriesgo)
        estado_partida = definir_victoria(arriesgo)
        if estado_partida or (intentos == CANTIDAD_INTENTOS -1):
            tablero = actualizar_tablero(tablero, intentos, arriesgo)
            imprimir_interfaz(palabra_adivinar, palabra_oculta, tablero, fin = True)
            time_end = datetime.now()
        intentos += 1

    delta_time = time_end - time_start
    mins = int(delta_time.total_seconds() / 60)
    secs = int(delta_time.total_seconds() - (60 * mins))

    print(f'Ganaste! Y te tomo {mins} minutos y {secs} segundos.') \
        if estado_partida else print("Perdiste!")


def rejugabilidad():
    print('\n~ WELCOME TO WORDLE ~')
    jugar_denuevo = True
    while jugar_denuevo:
        print('')
        logica_juego()
        desea_seguir = (input('Jugar denuevo (S/N): ')).upper()
        while desea_seguir not in 'SN':
            desea_seguir = (input('Error solo se acepta (S/N): ')).upper()
        if desea_seguir == 'N':
            jugar_denuevo = False
            print('Gracias por jugar!')

rejugabilidad()
