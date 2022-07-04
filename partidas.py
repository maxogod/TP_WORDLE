from archivo_csv import crear_archivo_csv

def actualizar_lista_partida(lista_partida, numero_partida, diccionario_jugadores, fecha, hora):
    for jugador in diccionario_jugadores:
        lista_partida.append((numero_partida, fecha, hora, jugador, diccionario_jugadores[jugador]['aciertos'], len(diccionario_jugadores[jugador]["intentos"])))


def imprimir_y_guardar_info_partidas_jugadas(lista_partidas, reinicio_archivo):
    lista_datos = []
    print("Partida    Fecha Partida    Hora Finalizacion    Nombre Jugador    Aciertos    Intentos")
    lista_partidas.sort(key = lambda tuple: tuple[4], reverse = True ) 
    for partida in lista_partidas:
        print('{}\t\t\t{}\t\t\t{}\t\t\t{}\t\t\t\t{}\t\t\t{}'.format(
            partida[0], partida[1], partida[2], partida[3], partida[4], partida[5]
        ))
        lista_datos.append(f'{partida[1]},{partida[2]},{partida[3]},{partida[4]},{partida[5]}')

    modo = 'w' if (reinicio_archivo) else 'a'
    crear_archivo_csv(lista_datos, 'archivos/partidas.csv', modo)
