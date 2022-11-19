import tkinter
import customtkinter
import pymysql


from config import host, user, passwd, db 


try:
    connection = pymysql.connect(
        host = config.host,
        port = 3306,
        user = config.user,
        password = config.passwd,
        database = config.db,
        cursorclass = pymysql.cursors.DictCursor
    )
    print("Connection Connected successfully! ")
except Exception:
    print("Connection failure ... ")
    print(Exception)




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
formLogin.geometry("350x300")
formLogin.title("Вход в систему")


################################
#                              #
#    Button click functions    #
#                              #
################################
def buttonLoginClick():
    labelError.configure(text="Ошибка")
    
def buttonRegisterClick():
    labelError.configure(text="Ошибка")


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

entryPassword = customtkinter.CTkEntry(master=frameLogin, width=WIDTH, placeholder_text="Введите пароль")
entryPassword.pack(pady=10, padx=10)

buttonLogin = customtkinter.CTkButton(master=frameLogin, text="Войти", width=WIDTH, command=buttonLoginClick)
buttonLogin.pack(pady=10, padx=10)

buttonRegister = customtkinter.CTkButton(master=frameLogin, text="Зарегистрироваться", width=WIDTH, command=buttonRegisterClick)
buttonRegister.pack(pady=10, padx=10)

labelError = customtkinter.CTkLabel(master=frameLogin, justify=tkinter.CENTER, width=WIDTH, text="")
labelError.pack(pady=10, padx=10)


#############################
#                           #
#    Form initialization    #
#                           #
#############################
formLogin.mainloop()