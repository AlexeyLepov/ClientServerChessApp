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
customtkinter.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"
WIDTH = HEIGHT = 240
formLogin = customtkinter.CTk()
formLogin.geometry(f"{WIDTH+100}x{HEIGHT+100}")
formLogin.resizable(False, False)
formLogin.title("Вход в систему")
formLogin.eval('tk::PlaceWindow . center')
# formLogin.withdraw()


################################
#                              #
#    Button click functions    #
#                              #
################################
def buttonLoginClick():
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
        try:
            username = entryUser.get()
            password = entryPassword.get()
            query = "SELECT username, password FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
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
        conn.close()
    except Exception:
        print("Connection failure ... ")
        labelError.configure(text="Нет подключения к серверу ... ")
    

def buttonGuestClick():
    username = "guest"
    password = "guest"
    ...


def buttonRegisterClick():
    ...


##############################
#                            #
#    Building frame items    #
#                            #
##############################
#creating elements
frameLogin = customtkinter.CTkFrame(master=formLogin)
labelWelcome = customtkinter.CTkLabel(master=frameLogin, justify=tkinter.CENTER, width=WIDTH, text="Вход в систему")
entryUser = customtkinter.CTkEntry(master=frameLogin, width=WIDTH, placeholder_text="Введите логин")
entryPassword = customtkinter.CTkEntry(master=frameLogin, width=WIDTH, placeholder_text="Введите пароль", show="*")
buttonLogin = customtkinter.CTkButton(master=frameLogin, text="Войти", width=WIDTH, command = lambda: buttonLoginClick())
buttonGuest = customtkinter.CTkButton(master=frameLogin, text="Войти как гость", width=WIDTH, command = lambda: buttonGuestClick())
buttonRegister = customtkinter.CTkButton(master=frameLogin, text="Зарегистрироваться", width=WIDTH, command = lambda: buttonRegisterClick())
labelError = customtkinter.CTkLabel(master=frameLogin, justify=tkinter.CENTER, width=WIDTH, text="")
#packing elements
frameLogin.pack(
    pady=10, padx=10, fill="both", expand=True)
labelWelcome.pack(
    pady=10, padx=10)
entryUser.pack(
    pady=10, padx=10)
entryPassword.pack(
    pady=10, padx=10)
buttonLogin.pack(
    pady=10, padx=10)
buttonGuest.pack(
    pady=10, padx=10)
buttonRegister.pack(
    pady=10, padx=10)
labelError.pack(
    pady=10, padx=10)


################################
#                              #
#    Test connection to DB     #
#                              #
################################
# try:
#     conn = pymysql.connect(
#         host = config.host,
#         port = config.port,
#         user = config.user,
#         password = config.password,
#         database = config.database,
#         cursorclass = pymysql.cursors.DictCursor
#     )
#     cur = conn.cursor()
#     cur.execute("select @@version")
#     output = cur.fetchall()
#     print(output)
#     print("Connected successfully! ")
#     conn.close()
# except Exception:
#     print("Connection failure ... ")
#     labelError.configure(text="Нет подключения к серверу ... ")


formLogin.mainloop()