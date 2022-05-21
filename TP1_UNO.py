from utiles import obtener_color
import utiles

def validar_aciertos(palabra_a_adivinar, palabra_arriesgada):
    '''
    Recibe la palabra a adivinar y la palabra ingresada por el usuario, ambas en mayusculas. Retorna la palabra arriesgada, cada letra con su color correspondiente segun si esta en la palabra a adivinar y en la posicion adecuada (verde), si aparece en la palabra a adivinar pero en otra posicion (amarillo) o si no esta en la palabra (gris oscuro). Cada letra esta separada por espacios para mejor lectura
    '''

    palabra_pintada = ""

    for letra in range(len(palabra_a_adivinar)):
        if (palabra_arriesgada[letra] in palabra_a_adivinar and palabra_arriesgada[letra] == palabra_a_adivinar[letra]):
            palabra_pintada += obtener_color("Verde") + palabra_arriesgada[letra] + " "
        elif (palabra_arriesgada[letra] in palabra_a_adivinar and palabra_arriesgada[letra] != palabra_a_adivinar[letra]):
            palabra_pintada += obtener_color("Amarillo") + palabra_arriesgada[letra] + " "
        else:
            palabra_pintada += obtener_color("GrisOscuro") + palabra_arriesgada[letra] + " "

    palabra_pintada += obtener_color("Defecto")

    return palabra_pintada
    
palabra_a_adivinar = "queso"
palabra_arriesgada = "prsnO"

palabra = validar_aciertos(palabra_a_adivinar, palabra_arriesgada)

print(palabra)

