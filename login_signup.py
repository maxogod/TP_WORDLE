from tkinter import *
from tkinter import messagebox

class Jugadores:
    p1 = ''
    p2 = ''

    def __init__(self, username):
        if Jugadores.p1 == '':
            Jugadores.p1 = username
        elif Jugadores.p2 == '':
            Jugadores.p2 = username

def read_file(filename):
    #Puede ser reemplazada por otra funcion que haga lo mismo,
    #pero cuidado con el return default ['', '']
    line = filename.readline()
    return line.rstrip('\n').split(',') if line else ['', '']


def validacion(username, password):
    with open("usuarios.csv") as users_file:
        username_leido, password_leido = read_file(users_file)
        while username_leido and username != username_leido:
            username_leido, password_leido = read_file(users_file)

    return username == username_leido and password == password_leido and Jugadores.p1 != username


def emergentwindow(username, password):
    if validacion(username, password):
        Jugadores(username)
        successwindow()
    else:
        errorwindow()


def successwindow():
    messagebox.showinfo('Success', 'Logueado correctamente')


def errorwindow():
    messagebox.showerror('Error', 'Error, No pudo loguearse, o no esta registrado '
                                  'o ya esta logueado')

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
    Se la llama en el boton de aceptar de la ventana de registro. Llama a la funcion registrar_nuevo_usuario y cierra la ventana de registro al finalizar.
    Florencia Russo
    '''
    registrar_nuevo_usuario(username, password, password2, nombre_archivo)
    rootRegistro.destroy()

def registrar_nuevo_usuario(usuario, clave, clave2, nombre_archivo):
    '''
    Guarda un nuevo usuario en el archivo de usuarios.csv si no existe y si no genera mensaje de usuario existente 
    Florencia Russo
    '''
    if(not validar_nombre_usuario(usuario)):
        messagebox.showerror('', f'Nombre de usuario {usuario} invalido. Debe contener letras, numeros y _ unicamente')
    elif(clave != clave2):
        messagebox.showerror('', f'Ambas claves deben ser iguales')
    elif(not validar_clave(clave)):
       messagebox.showerror('', f'Clave invalida. La clave debe tener una longitud de entre 8 y 15 caracteres, y estar formada por al menos una mayuscula, una minuscula y _ o -')
    elif (not validacion(usuario, clave)):
        with open(nombre_archivo, 'a', encoding = "utf8") as archivo:
            archivo.write(f'{usuario},{clave}\n')
        messagebox.showinfo("", f'Usuario {usuario} creado')
    else: 
        messagebox.showwarning('', f'Usuario {usuario} ya registrado')

def validar_nombre_usuario(nombre_usuario):
    '''
    Valida que el nombre de usuario ingresado tenga la longitud deseada y este formado solo por letras, numeros y _ o -.
    Florencia Russo
    '''
    nombre_valido = False
    largo_min = 4
    largo_max = 15
    nombre_letras = nombre_usuario.replace('_', '')
    if ((largo_min <= len(nombre_usuario) <= largo_max) and nombre_letras.isalnum() and '_' in nombre_usuario):
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
            if(clave_sin_guion[i].isupper()):
                mayuscula += 1
            elif(clave_sin_guion[i].islower()):
                minuscula += 1
            elif(clave_sin_guion[i].isnumeric()):
                numero += 1
            elif(not clave_sin_guion[i].isalnum()):
                caracteres +=1
            elif(clave_sin_guion[i] in 'áéíóú'):
                tildes += 1
            
            i += 1

            if(numero>0 and mayuscula>0 and minuscula>0 and caracteres == 0 and tildes == 0):
                clave_valida = True
        
    return clave_valida

def gui_registro():
    '''
    Crea la pantalla con el formulario de registro.
    Florencia Russo
    '''
    rootRegistro = Toplevel()
    rootRegistro.title("Wordle G1 - Registrar nuevo usuario")
    rootRegistro.resizable(0,0)
    rootRegistro.geometry("350x350")

    frameRegistro = Frame(rootRegistro)
    frameRegistro.pack()

    usuarioRegistro = StringVar()
    contraseñaRegistro = StringVar()
    contraseñaReingreso = StringVar()

    etiquetaUsuario = Label(frameRegistro, text = 'Nombre de Usuario')
    etiquetaUsuario.grid(row = 0, column = 0, sticky = 'w')
    textBoxUsuario = Entry(frameRegistro, textvariable = usuarioRegistro)
    textBoxUsuario.grid(row = 0, column = 1, sticky = 'w')

    etiquetaContraseña = Label(frameRegistro, text = 'Contraseña')
    etiquetaContraseña.grid(row = 1, column = 0, sticky = 'w')
    textBoxContraseña = Entry(frameRegistro, textvariable = contraseñaRegistro)
    textBoxContraseña.grid(row = 1, column = 1, sticky = 'w')
    textBoxContraseña.config(show = '*')

    etiquetaContraseñaReingreso = Label(frameRegistro, text = 'Reingrese Contraseña')
    etiquetaContraseñaReingreso.grid(row = 2, column = 0, sticky = 'w')
    textBoxContraseñaReingreso = Entry(frameRegistro, textvariable = contraseñaReingreso)
    textBoxContraseñaReingreso.grid(row = 2, column = 1, sticky = 'w')
    textBoxContraseñaReingreso.config(show = '*')

    botonRegistro = Button(frameRegistro, text = "Aceptar", command = lambda : aplicar_register(usuarioRegistro.get(), contraseñaRegistro.get(), contraseñaReingreso.get(), rootRegistro, 'usuarios.csv'))
    botonRegistro.grid(row = 3, column = 1, sticky = 'w')


def gui():
    #Root of GUI
    root = Tk()
    root.iconbitmap('archivos/icono.ico')
    root.title('Wordle G1 Log-in')
    root.resizable(False, False)
    root.geometry('350x200')
    root.config(bg= 'hot pink')

    #Frame of GUI
    frame = Frame(root)
    frame.config(bg= 'black')
    frame.config(relief='groove')
    frame.config(bd=5)
    frame.grid(rowspan = 5, columnspan = 5, padx=60, pady=20)

    #All the labels below
    LabelUser = Label(frame, text='Username:')
    LabelUser.config(bg= 'black')
    LabelUser.config(fg= 'white')
    LabelUser.grid(row = 0, column= 0, padx= 5, pady= 10)

    LabelPassword = Label(frame, text= 'Password:')
    LabelPassword.config(bg= 'black')
    LabelPassword.config(fg= 'white')
    LabelPassword.grid(row=1, column=0, padx=5, pady=5)

    #All the entries below
    UsernameEntry = Entry(frame)
    UsernameEntry.config(bg='black')
    UsernameEntry.config(fg='white')
    UsernameEntry.grid(row = 0, column= 1, padx= 5, pady= 10)

    PasswordEntry = Entry(frame)
    PasswordEntry.config(bg='black')
    PasswordEntry.config(fg='white')
    PasswordEntry.config(show='*')
    PasswordEntry.grid(row = 1, column= 1, padx= 5, pady= 5)

    #Buttons
    ButtonEnter = Button(root, text='Enter',
                         command= lambda: aplicar_login(UsernameEntry.get(), PasswordEntry.get(), UsernameEntry, PasswordEntry))
    ButtonEnter.grid(row = 5, column= 1, padx= 5, pady= 5)
    
    ButtonRegister = Button(root, text='Register',
                         command = gui_registro)
    ButtonRegister.grid(row = 5, column= 3, padx= 5, pady= 5)

    ButtonOut = Button(root, text='Exit login',
                         command = lambda: root.destroy())
    ButtonOut.grid(row = 6, column= 4, padx= 5, pady= 5)
    

    root.mainloop()


def main_login():
    gui()
    l_jugadores = [Jugadores.p1, Jugadores.p2]
    return l_jugadores
