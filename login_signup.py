from tkinter import *
from tkinter import messagebox


class Jugadores:
    """
    Clase jugadores para guardar los usernames de p1 y p2.
    #Maximo Utrera
    """
    p1 = ''
    p2 = ''

    def __init__(self, username):
        if Jugadores.p1 == '':
            Jugadores.p1 = username
        elif Jugadores.p2 == '':
            Jugadores.p2 = username


def read_file(filename):
    """
    Lee archivo.
    #Maximo Utrera
    """
    line = filename.readline()
    return line.rstrip('\n').split(',') if line else ['', '']


def validacion_usuario_para_login(username, password):
    """
    Abre el archivo de usuarios y corrobora que el nombre de usuario se encuentre en este,
    asi como la contraseña sea correcta.
    retorna un boolean dependiendo si se valida el usuario o no.
    #Maximo Utrera
    """
    with open("archivos/usuarios.csv") as users_file:
        username_leido, password_leido = read_file(users_file)
        while username_leido and username != username_leido:
            username_leido, password_leido = read_file(users_file)

    return username == username_leido and password == password_leido and Jugadores.p1 != username


def emergentwindow(username, password):
    """
    si se valido el usuario y contraseña llama a funcion successwindow sino a errorwindow.
    #Maximo Utrera
    """
    if validacion_usuario_para_login(username, password):
        Jugadores(username)
        successwindow()
    else:
        errorwindow()


def successwindow():
    """
    muestra mensaje de logueado correctamente en una ventana.
    #Maximo Utrera
    """
    if Jugadores.p2 == '':
        messagebox.showinfo('Success', 'Jugador 1 logueado correctamente. (Falta jugador 2!)')
    else:
        messagebox.showinfo('Success', 'Jugador 2 logueado correctamente. A JUGAR!')


def errorwindow():
    """
    muestra mensaje de error al loguearse en una ventana.
    #Maximo Utrera
    """
    messagebox.showerror('Error', 'Error, El usuario o la contraceña no son correctos.')


def aplicar_login(username, password, usernameEntry, passwordEntry):
    '''
    Se la llama en el boton de login. Llama a la funcion emergentwindow y limpia las entradas para usuario y clave.
    Florencia Russo
    '''
    emergentwindow(username, password)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)


def aplicar_register(username, password, password2, rootRegistro, nombre_archivo):
    '''
    Se la llama en el boton de enter de la ventana de registro.
    Llama a la funcion registrar_nuevo_usuario y cierra la ventana de registro al finalizar.
    Florencia Russo
    '''
    registrar_nuevo_usuario(username, password, password2, nombre_archivo)
    rootRegistro.destroy()


def emergent_windows_registro(tipo_msg, username, mensaje):
    """
    muestra los mendajes correspondientes segun los parametros.
    #Maximo Utrera
    """
    posibles_msg = {'username invalido': f'Nombre de usuario {username} invalido. '
                                         'Debe contener letras, numeros y _ unicamente',
                    'claves diferentes': 'Ambas claves deben ser iguales',
                    'clave invalida': 'Clave invalida. '
                                      'La clave debe tener una longitud de entre 8 y 15 caracteres, '
                                      'y estar formada por al menos una mayuscula, una minuscula y _ o -',
                    'usuario creado': f'Usuario {username} fue creado.',
                    'ya registrado': f'Usuario {username} ya registrado'}
    if tipo_msg == 'error':
        messagebox.showerror('error', posibles_msg[mensaje])
    elif tipo_msg == 'info':
        messagebox.showinfo('success', posibles_msg[mensaje])
    elif tipo_msg == 'warning':
        messagebox.showwarning('warning', posibles_msg[mensaje])


def registrar_nuevo_usuario(usuario, clave, clave2, nombre_archivo):
    '''
    Guarda un nuevo usuario en el archivo de usuarios.csv
    si no existe y si no genera mensaje de usuario existente
    Florencia Russo
    '''
    if not validar_nombre_usuario(usuario):
        emergent_windows_registro('error', usuario, 'username invalido')
    elif clave != clave2:
        emergent_windows_registro('error', usuario, 'claves diferentes')
    elif not validar_clave(clave):
        emergent_windows_registro('error', usuario, 'clave invalida')
    elif not validacion_usuario_para_login(usuario, clave):
        with open(nombre_archivo, 'a', encoding="utf8") as archivo:
            archivo.write(f'{usuario},{clave}\n')
        emergent_windows_registro('info', usuario, 'usuario creado')
    else:
        emergent_windows_registro('warning', usuario, 'ya registrado')


def validar_nombre_usuario(nombre_usuario):
    '''
    Valida que el nombre de usuario ingresado tenga la longitud deseada y este formado solo por letras,
    numeros y _ o -.
    Florencia Russo
    '''
    nombre_valido = False
    largo_min = 4
    largo_max = 15
    nombre_letras = nombre_usuario.replace('_', '')
    if ((largo_min <= len(nombre_usuario) <= largo_max) and
            nombre_letras.isalnum() and '_' in nombre_usuario):
        nombre_valido = True

    return nombre_valido


def validar_clave(clave):
    '''
    Valida que la clave sea de la longitud adecuada, este formada por al menos una mayuscula, minuscula y numero, que tenga _ o - y que no tenga caracteres especiales o tildes.
    Florencia Russo
    '''
    clave_valida = False
    numero = 0
    mayuscula = 0
    minuscula = 0
    caracteres = 0
    tildes = 0
    largo_min = 8
    largo_max = 12
    clave_sin_guion = clave.replace('_', '')
    clave_sin_guion = clave_sin_guion.replace('-', '')
    if ((largo_min <= len(clave) <= largo_max) and ('_' in clave or '-' in clave)):
        i = 0
        while (i < len(clave_sin_guion) and not clave_valida):
            if (clave_sin_guion[i].isupper()):
                mayuscula += 1
            elif (clave_sin_guion[i].islower()):
                minuscula += 1
            elif (clave_sin_guion[i].isnumeric()):
                numero += 1
            elif (not clave_sin_guion[i].isalnum()):
                caracteres += 1
            elif (clave_sin_guion[i] in 'áéíóú'):
                tildes += 1

            i += 1

            if (numero > 0 and mayuscula > 0 and minuscula > 0 and caracteres == 0 and tildes == 0):
                clave_valida = True

    return clave_valida


def gui_registro():
    '''
    Crea la pantalla con el formulario de registro.
    #Florencia Russo
    el "look" de la interfaz.
    #Maximo Utrera
    '''

    rootRegistro = Toplevel()
    rootRegistro.iconbitmap('archivos/pikachu.ico')
    rootRegistro.title("Wordle G1 | Sign-up")
    rootRegistro.resizable(0, 0)
    rootRegistro.geometry("350x150")
    rootRegistro.config(bg='sky blue')

    frameRegistro = Frame(rootRegistro)
    frameRegistro.pack()
    frameRegistro.config(bg='black')
    frameRegistro.config(relief='groove')
    frameRegistro.config(bd=5)
    frameRegistro.grid(rowspan=5, columnspan=5, padx=50, pady=20)

    usuarioRegistro = StringVar()
    contrasenaRegistro = StringVar()
    contrasenaReingreso = StringVar()

    etiquetaUsuario = Label(frameRegistro, text='Nombre de Usuario')
    etiquetaUsuario.grid(row=0, column=0, sticky='w')
    etiquetaUsuario.config(bg='black')
    etiquetaUsuario.config(fg='white')
    textBoxUsuario = Entry(frameRegistro, textvariable=usuarioRegistro)
    textBoxUsuario.grid(row=0, column=1, sticky='w')
    textBoxUsuario.config(bg='black')
    textBoxUsuario.config(fg='white')

    etiquetaContrasena = Label(frameRegistro, text='Contraseña')
    etiquetaContrasena.grid(row=1, column=0, sticky='w')
    etiquetaContrasena.config(bg='black')
    etiquetaContrasena.config(fg='white')
    textBoxContrasena = Entry(frameRegistro, textvariable=contrasenaRegistro)
    textBoxContrasena.grid(row=1, column=1, sticky='w')
    textBoxContrasena.config(show='*')
    textBoxContrasena.config(bg='black')
    textBoxContrasena.config(fg='white')

    etiquetaContrasenaReingreso = Label(frameRegistro, text='Reingrese Contraseña')
    etiquetaContrasenaReingreso.grid(row=2, column=0, sticky='w')
    etiquetaContrasenaReingreso.config(bg='black')
    etiquetaContrasenaReingreso.config(fg='white')
    textBoxContrasenaReingreso = Entry(frameRegistro, textvariable=contrasenaReingreso)
    textBoxContrasenaReingreso.grid(row=2, column=1, sticky='w')
    textBoxContrasenaReingreso.config(show='*')
    textBoxContrasenaReingreso.config(bg='black')
    textBoxContrasenaReingreso.config(fg='white')

    botonRegistro = Button(rootRegistro,
                           text="Enter",
                           command=lambda: aplicar_register(usuarioRegistro.get(),
                                                            contrasenaRegistro.get(),
                                                            contrasenaReingreso.get(),
                                                            rootRegistro, 'archivos/usuarios.csv'))
    botonRegistro.grid(row=5, column=2)


def gui():
    """
    la intefaz grafica Main del modulo usada para el login de cada usuario, y trabaja en conjunto,
    con la otra gui (la de registro).
    #Maximo Utrera
    los botones de registro y exit.
    #Florencia russo
    """
    # Root of GUI
    root = Tk()
    root.iconbitmap('archivos/pikachu.ico')
    root.title('Wordle G1 | Log-in')
    root.resizable(False, False)
    root.geometry('350x200')
    root.config(bg='hot pink')

    # Frame of GUI
    frame = Frame(root)
    frame.config(bg='black')
    frame.config(relief='groove')
    frame.config(bd=5)
    frame.grid(rowspan=5, columnspan=5, padx=70, pady=20)

    # All the labels below
    LabelUser = Label(frame, text='Username:')
    LabelUser.config(bg='black')
    LabelUser.config(fg='white')
    LabelUser.grid(row=0, column=0, padx=5, pady=10)

    LabelPassword = Label(frame, text='Password:')
    LabelPassword.config(bg='black')
    LabelPassword.config(fg='white')
    LabelPassword.grid(row=1, column=0, padx=5, pady=5)

    # All the entries below
    UsernameEntry = Entry(frame)
    UsernameEntry.config(bg='black')
    UsernameEntry.config(fg='white')
    UsernameEntry.grid(row=0, column=1, padx=5, pady=10)

    PasswordEntry = Entry(frame)
    PasswordEntry.config(bg='black')
    PasswordEntry.config(fg='white')
    PasswordEntry.config(show='*')
    PasswordEntry.grid(row=1, column=1, padx=5, pady=5)

    # Buttons
    ButtonEnter = Button(root, text='Enter',
                         command=lambda: aplicar_login(UsernameEntry.get(), PasswordEntry.get(), UsernameEntry,
                                                       PasswordEntry))
    ButtonEnter.grid(row=5, column=1, padx=5, pady=5)

    ButtonRegister = Button(root, text='Register',
                            command=gui_registro)
    ButtonRegister.grid(row=5, column=3, padx=5, pady=5)

    ButtonOut = Button(root, text='Exit login',
                       command=lambda: root.destroy())
    ButtonOut.grid(row=6, column=2, padx=5, pady=5)

    root.mainloop()


def main_login():
    """
    funcion principal, la cual debe ser llamada para correr tod0 el modulo,
    retorna una lista con los nombres del p1 y p2 (obtenidos de la clase Jugadores).
    #Maximo Utrera
    """
    gui()
    l_jugadores = [Jugadores.p1, Jugadores.p2]
    return l_jugadores
