from tkinter import *
from tkinter import messagebox

def read_file(filename):
    #Puede ser reemplazada por otra funcion que haga lo mismo,
    #pero cuidado con el return default ['', '']
    line = filename.readline()
    return line.rstrip('\n').split(',') if line else ['', '']


def validacion(username, password, users_file):

    username_leido, password_leido = read_file(users_file)
    while username_leido and username != username_leido:
        username_leido, password_leido = read_file(users_file)

    return username == username_leido and password == password_leido


def emergentwindow(username, password, users_file):
    if validacion(username, password, users_file):
        successwindow()
    else:
        errorwindow()


def successwindow():
    messagebox.showinfo('Success', 'Logueado correctamente')


def errorwindow():
    messagebox.showerror('Error', 'Error, No pudo loguearse, o no esta registrado')


def gui(users_file):
    #Root of GUI
    root = Tk()
    root.iconbitmap(r'C:\Users\TAI DING\Desktop\Utilities\ICONS\pokemon.ico')
    root.title('Wordle G1 Log-in')
    root.resizable(False, False)
    root.geometry('350x150')
    root.config(bg= 'hot pink')

    #Frame of GUI
    frame = Frame(root)
    frame.config(bg= 'black')
    frame.config(relief='groove')
    frame.config(bd=5)
    frame.pack(fill="both", expand=True, padx=60, pady=20)

    #All the labels bellow
    LabelUser = Label(frame, text='Username:')
    LabelUser.config(bg= 'black')
    LabelUser.config(fg= 'white')
    LabelUser.grid(row = 0, column= 0, padx= 5, pady= 10)

    LabelPassword = Label(frame, text= 'Password:')
    LabelPassword.config(bg= 'black')
    LabelPassword.config(fg= 'white')
    LabelPassword.grid(row=1, column=0, padx=5, pady=5)

    #All the entries bellow
    UsernameEntry = Entry(frame)
    UsernameEntry.config(bg='black')
    UsernameEntry.config(fg='white')
    UsernameEntry.grid(row = 0, column= 1, padx= 5, pady= 10)

    PasswordEntry = Entry(frame)
    PasswordEntry.config(bg='black')
    PasswordEntry.config(fg='white')
    PasswordEntry.config(show='*')
    PasswordEntry.grid(row = 1, column= 1, padx= 5, pady= 5)

    #Button
    ButtonEnter = Button(root, text='Enter',
                         command= lambda:
                         emergentwindow(UsernameEntry.get(), PasswordEntry.get(), users_file))
    ButtonEnter.pack()


    root.mainloop()


def main_login():
    with open("usuarios.csv") as users_file:
        gui(users_file)

main_login()
