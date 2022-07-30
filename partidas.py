from archivo_csv import crear_archivo_csv

def actualizar_lista_partida(lista_partida, numero_partida, diccionario_jugadores, fecha, hora):
    """
    #Ivan Teuber
    """
    for jugador in diccionario_jugadores:
        lista_partida.append((numero_partida, fecha, hora, jugador, diccionario_jugadores[jugador]['aciertos'],
                              len(diccionario_jugadores[jugador]["intentos"])))


def imprimir_y_guardar_info_partidas_jugadas(lista_partidas, reinicio_archivo):
    """
    #Ivan Teuber
    """
    lista_datos = []
    dic_resumen = {}
    #Partida    Fecha Partida    Hora Finalizacion    Nombre Jugador    Aciertos    Intentos
    lista_partidas.sort(key = lambda tuple: tuple[4], reverse = True ) 
    for partida in lista_partidas:
        if partida[3] not in dic_resumen.keys():
            dic_resumen[partida[3]] = [partida[4], partida[5]]
        else:
            dic_resumen[partida[3]][0] += partida[4]
            dic_resumen[partida[3]][1] += partida[5]
        lista_datos.append(f'{partida[1]},{partida[2]},{partida[3]},{partida[4]},{partida[5]}')

    modo = 'w' if (reinicio_archivo) else 'a'
    crear_archivo_csv(lista_datos, 'archivos/partidas.csv', modo)
    for i in dic_resumen.keys():
        print(f"Nombre - {i}\tAciertos - {dic_resumen[i][0]}\tIntentos - {dic_resumen[i][1]}")
