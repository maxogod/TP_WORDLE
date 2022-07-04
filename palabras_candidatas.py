from palabras import sin_acentos

def agregar_palabra_candidata_a_diccionario(diccionario_palabras, palabra, cantidad_letras_palabra, indice_archivo):
    '''
    Recibe un diccionario con las palabras a adivinar, la palabra a agregar al diccionario, la cantidad de letras que deben tener las palabras candidatas, y un numero identificatorio de archivo.
    Si palabra esta formada solo por letras y su longitud es cantidad_letras_palabra, agrega al diccionario diccionario_palabras una clave con la palabra en mayusculas y la cantidad de veces que aparece.
    Florencia Russo
    '''
    palabra_sin_acentos_ni_signos = sin_acentos_ni_signos(palabra)
    if (palabra_sin_acentos_ni_signos.isalpha() and (len(palabra_sin_acentos_ni_signos) == cantidad_letras_palabra)):
        if (palabra_sin_acentos_ni_signos not in diccionario_palabras.keys()):
            diccionario_palabras[palabra_sin_acentos_ni_signos] = {indice_archivo: 1}
        elif(indice_archivo not in diccionario_palabras[palabra_sin_acentos_ni_signos.upper()].keys()):
            diccionario_palabras[palabra_sin_acentos_ni_signos][indice_archivo] = 1
        else:
            diccionario_palabras[palabra_sin_acentos_ni_signos][indice_archivo] += 1

def sin_acentos_ni_signos(palabra):
    '''
    Recibe una palabra. Retorna la misma con sus vocales sin acentos y sin signos de puntuacion. Por ejemplo, 'murciélago,' --> murcielago 
    Florencia Russo
    '''
    palabra_sin_acento = sin_acentos(palabra)
    palabra_sin_signos = ''
    signos_puntuacion = ',.:;¡!¿?-_'

    for caracter in palabra_sin_acento:
        if (caracter not in signos_puntuacion):
            palabra_sin_signos += caracter
    
    return palabra_sin_acento.upper()

def obtener_palabras_de_archivo(diccionario_palabras, nombre_archivo, indice_archivo, cantidad_letras_palabra):
    '''
    Funcion que lee el archivo y agrega palabras al diccionario. Recibe el diccionario de palabras, el nombre del archivo y un indice de archivo. Por cada palabra de cada linea, llama a la funcion agregar_palabra_candidata_a_diccionario.
    Florencia Russo
    '''
    with open(nombre_archivo, 'r', encoding = "utf8") as archivo:
        for linea in archivo:
            lista_palabras = linea.rstrip("\n").split(' ')

            for palabra in lista_palabras:
                agregar_palabra_candidata_a_diccionario(diccionario_palabras, palabra, cantidad_letras_palabra, indice_archivo)


def crear_archivo_csv(diccionario_palabras, cantidad_archivos):
    '''
    Funcion que crea el archivo palabras.csv y guarda las claves del diccionario diccionario_palabras ordenadas alfabeticamente y cuantas veces aparecen esas claves en cada archivo.
    Recibe el diccionario de palabras y la cantidad de archivos. 
    No tiene retorno.
    Florencia Russo
    '''
    archivo_csv = open('archivos/palabras.csv', 'w', encoding = 'utf8')
    dict_ordenado = sorted(diccionario_palabras.items(), key = lambda dict: dict[0])
    for clave in dict_ordenado:
        lista_cantidades = ''
        for item in range(cantidad_archivos):
            if item in clave[1]:
                lista_cantidades += f'{str(clave[1][item])},'
            else:
                lista_cantidades += '0,'
        archivo_csv.write(f'{clave[0].lower()},{lista_cantidades.rstrip(",")} \n')

    archivo_csv.close()

def obtener_diccionario_palabras_candidatas(lista_archivos, cantidad_letras_palabra):
    '''
    Recibe una lista con todos los archivos a extraer las palabras. Crea el archivo Retorna el diccionario con las palabras candidatas a ser adivinadas.
    Florencia Russo
    '''
    diccionario_palabras = {}
    for indice_archivo in range(len(lista_archivos)):
        obtener_palabras_de_archivo(diccionario_palabras, lista_archivos[indice_archivo], indice_archivo, cantidad_letras_palabra)

    crear_archivo_csv(diccionario_palabras, len(lista_archivos))

    return diccionario_palabras
