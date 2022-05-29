from utiles import obtener_color, obtener_palabras_validas
import utiles
import random

CANTIDAD_LETRAS = 5 #CONSULTAR ALCANCE VARIABLE/VARIABLE GLOBAL

def ocultar_letras_no_adivinadas(palabra, arriesgo):
    letras = ""
    arriesgo = arriesgo.split(' ')

    for letra in range(len(palabra)):
        if ((len(arriesgo) >1 ) and (obtener_color("Verde") in arriesgo[letra])):
            letras += palabra[letra] + ' '
        else: 
            letras += '? '

    return letras

def crear_tablero():
    tablero = []
    for i in range (CANTIDAD_LETRAS):
        tablero.append('? '*CANTIDAD_LETRAS)
    
    return tablero

def actualizar_tablero(tablero, intentos, arriesgo):

    tablero[intentos] = arriesgo
    
    return tablero

def imprimir_interfaz(palabra, tablero, estado_partida = False):
    
    print("Palabra a adivinar: {} ".format(palabra))

    for celda in tablero:
        aux = " ".join(celda)
        print(celda)

    if (estado_partida):
        texto = print("Arriesgo: ")
    else:
        texto = input("Arriesgo: ").upper()
        

    return texto

def selecciona_palabra():
    lista=obtener_palabras_validas()
    #return lista[random.randint(0, len(lista))].upper()
    return lista[56].upper()

def definir_victoria(palabra):
    cont=0
    palabra = palabra.split(' ')
    estado = False

    for i in palabra:
        if obtener_color("Verde") in i:
            cont+=1
    if cont==CANTIDAD_LETRAS:
        estado = True
        #print("Ganaste!")     
    # else:
    #     print("Perdiste!")

    return estado

def validar_aciertos(palabra_a_adivinar, palabra_arriesgada):
    '''
    Recibe la palabra a adivinar y la palabra ingresada por el usuario, ambas en mayusculas. 
    Retorna la palabra arriesgada, cada letra con su color correspondiente segun si esta en la palabra a adivinar y en la posicion adecuada (verde), si aparece en la palabra a adivinar pero en otra posicion (amarillo) o si no esta en la palabra (gris oscuro). 
    Cada letra esta separada por espacios para mejor lectura.
    '''

    palabra_pintada = ""
    palabra_a_adivinar = palabra_a_adivinar.upper()
    palabra_arriesgada = palabra_arriesgada.upper()

    for letra in range(len(palabra_a_adivinar)):
        if (palabra_arriesgada[letra] in palabra_a_adivinar and palabra_arriesgada[letra] == palabra_a_adivinar[letra] and palabra_a_adivinar.count(palabra_arriesgada[letra]) <= palabra_arriesgada.count(palabra_arriesgada[letra])):
            palabra_pintada += obtener_color("Verde") + palabra_arriesgada[letra] + " "
        elif (palabra_arriesgada[letra] in palabra_a_adivinar and palabra_arriesgada[letra] != palabra_a_adivinar[letra] and palabra_a_adivinar.count(palabra_arriesgada[letra]) == palabra_arriesgada.count(palabra_arriesgada[letra]) ):
            palabra_pintada += obtener_color("Amarillo") + palabra_arriesgada[letra] + " "
        else:
            palabra_pintada += obtener_color("GrisOscuro") + palabra_arriesgada[letra] + " "

    palabra_pintada += obtener_color("Defecto")

    return palabra_pintada

def validar_palabra(palabra):
    """
    La funcion recibe una palabra y verifica que sea de 5 letras y
    alpha, en caso contrario llama a la imprimir interfaz hasta tener una palabra
    valida, luego de obtenerla le pasa la palabra a la funcion sacar_acentos.
    """
    while len(palabra) != CANTIDAD_LETRAS or not palabra.isalpha():
        if len(palabra) != CANTIDAD_LETRAS:
            print('Error, el arriezgo debe tener la misma cantidad de letras que la palabra que se intenta adivinar')
        elif not palabra.isalpha():
            print('Error, el arriezgo deben ser todas letras')
        palabra = imprimir_interfaz(palabra)
    palabra = sin_acentos(palabra)
    return palabra

def sin_acentos(palabra):
    vocales = 'áéíóú'
    vocales_1 = 'aeiou'
    palabra_1 = palabra.lower()
    for letra in palabra_1: 
        if letra == vocales[0]:
            palabra = palabra_1.replace(letra,vocales_1[0])   
        elif letra == vocales[1]:
            palabra = palabra_1.replace(letra,vocales_1[1])
        elif letra == vocales[2]:
            resulpalabratado = palabra_1.replace(letra,vocales_1[2])
        elif letra == vocales[3]:
            palabra = palabra_1.replace(letra,vocales_1[3])
        elif letra == vocales[4]:
            palabra = palabra_1.replace(letra,vocales_1[4])
        else:
            pass
            
    return palabra.upper()


def logica_juego():
    intentos = 0
    palabra_adivinar = selecciona_palabra()
    palabra_oculta = ocultar_letras_no_adivinadas(palabra_adivinar, '')
    estado_partida = False
    tablero = crear_tablero()

    while (intentos <= CANTIDAD_LETRAS and not estado_partida):
        arriesgo = imprimir_interfaz(palabra_oculta, tablero)
        arriesgo = validar_palabra(arriesgo)
        arriesgo = validar_aciertos(palabra_adivinar, arriesgo)
        palabra_oculta = ocultar_letras_no_adivinadas(palabra_adivinar, arriesgo)
        tablero = actualizar_tablero(tablero, intentos, arriesgo)
        estado_partida = definir_victoria(arriesgo)
        if(estado_partida):
            tablero = actualizar_tablero(tablero, intentos, arriesgo)
            arriesgo = imprimir_interfaz(palabra_oculta, tablero, estado_partida)
        intentos += 1
    
    print('Ganaste!') if (estado_partida) else print("Perdiste")



logica_juego()