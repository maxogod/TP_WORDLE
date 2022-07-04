def crear_archivo_csv(contenido, nombre_archivo, modo):
    '''
    Funcion que crea el archivo palabras.csv y guarda las claves del diccionario diccionario_palabras ordenadas alfabeticamente y cuantas veces aparecen esas claves en cada archivo.
    Recibe el diccionario de palabras y la cantidad de archivos. 
    No tiene retorno.
    Florencia Russo
    '''
    archivo_csv = open(nombre_archivo, modo, encoding = 'utf8')
    for linea in contenido:
        archivo_csv.write(f'{linea} \n')

    archivo_csv.close()
