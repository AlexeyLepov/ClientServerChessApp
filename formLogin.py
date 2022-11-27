import pymysql
import tkinter
import customtkinter


import config


##############################
#                            #
#    Building a main form    #
#                            #
##############################
customtkinter.set_appearance_mode("dark")  # Modes: "System", "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"

WIDTH = HEIGHT = 240

formLogin = customtkinter.CTk()
formLogin.geometry(f"{WIDTH+100}x{HEIGHT+100}")
formLogin.title("Вход в систему")


##############################
#                            #
#    Building frame items    #
#                            #
##############################
frameLogin = customtkinter.CTkFrame(master=formLogin)
frameLogin.pack(pady=10, padx=10, fill="both", expand=True)

labelWelcome = customtkinter.CTkLabel(master=frameLogin, justify=tkinter.CENTER, width=WIDTH, text="Вход в систему")
labelWelcome.pack(pady=10, padx=10)

entryUser = customtkinter.CTkEntry(master=frameLogin, width=WIDTH, placeholder_text="Введите логин")
entryUser.pack(pady=10, padx=10)

entryPassword = customtkinter.CTkEntry(master=frameLogin, width=WIDTH, placeholder_text="Введите пароль", show="*")
entryPassword.pack(pady=10, padx=10)

buttonLogin = customtkinter.CTkButton(master=frameLogin, text="Войти", width=WIDTH)
buttonLogin.pack(pady=10, padx=10)

buttonGuest = customtkinter.CTkButton(master=frameLogin, text="Войти как гость", width=WIDTH)
buttonGuest.pack(pady=10, padx=10)

buttonRegister = customtkinter.CTkButton(master=frameLogin, text="Зарегистрироваться", width=WIDTH)
buttonRegister.pack(pady=10, padx=10)

labelError = customtkinter.CTkLabel(master=frameLogin, justify=tkinter.CENTER, width=WIDTH, text="")
labelError.pack(pady=10, padx=10)


##########################
#                        #
#    Connecting to DB    #
#                        #
##########################
try:
    conn = pymysql.connect(
        host = config.host,
        port = config.port,
        user = config.user,
        password = config.password,
        database = config.database,
        cursorclass = pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    cur.execute("select @@version")
    output = cur.fetchall()
    print(output)
    print("Connected successfully! ")
except Exception:
    print("Connection failure ... ")
    labelError.configure(text="Нет подключения к серверу... ")


################################
#                              #
#    Button click functions    #
#                              #
################################
def buttonLoginClick():
    try:
        query = "SELECT username, password FROM users WHERE username = '" + entryUser.get() + "' AND password = '" + entryPassword.get() + "'"
        cur.execute(query)
        # selectUsers = cur.fetchall()
        if cur.rowcount == 1:
            print("Вы вошли в систему! ")
            labelError.configure(text="Вы вошли в систему! ")
            ...
        else:                
            print("Неверные учетные данные! ") # credential
            labelError.configure(text="Неверные учетные данные! ")
    except Exception:
        labelError.configure(text="Ошибка")

def buttonGuestClick():
    try:
        query = "SELECT username, password FROM users WHERE username = guest'" + "' AND password = guest'" + "'"
        cur.execute(query)
        # selectUsers = cur.fetchall()
        if cur.rowcount == 1:
            print("Вы вошли в систему! ")
            labelError.configure(text="Вы вошли в систему! ")
            ...
        else:                
            print("Неверные учетные данные! ") # credential
            labelError.configure(text="Неверные учетные данные! ")
    except Exception:
        labelError.configure(text="Ошибка")

def buttonRegisterClick():
    ...


buttonLogin.command = lambda: buttonLoginClick()
buttonGuest.command = lambda: buttonGuestClick()
buttonRegister.command = lambda: buttonRegisterClick()


#############################
#                           #
#    Form initialization    #
#                           #
#############################
formLogin.mainloop()