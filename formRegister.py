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

WIDTH = HEIGHT = 350

formRegister = customtkinter.CTk()
formRegister.geometry(f"{WIDTH+100}x{HEIGHT+100}")
formRegister.resizable(False, False)
formRegister.title("Регистрация")


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
    conn.close()


################################
#                              #
#    Button click functions    #
#                              #
################################
def buttonLoginClick():
    ...
    conn.close()

def buttonRegisterClick():
    try:
        if entryEmail.get() == "" or entryPassword.get() == "" or entryPasswordRepeat.get() == "" or entryUser.get() == "":
            print("Заполните все поля! ")
            labelError.configure(text="Заполните все поля! ")

        elif entryPassword.get() == entryPasswordRepeat.get():
            score = 800
            if comboboxScore.get() == "Новичок":
                score = 600
            elif comboboxScore.get() == "Любитель":
                score = 1000
            elif comboboxScore.get() == "Мастер":
                score = 1400
            # INSERT INTO `chess`.`users` (`username`, `email`, `password`, `score`) VALUES ('test', 'test', 'test', '800');
            query = f"INSERT INTO `chess`.`users` (`username`, `email`, `password`, `score`) VALUES ('{entryUser.get()}', '{entryEmail.get()}', '{entryPassword.get()}', '{score}');"
            
            try:
                cur.execute(query)
                if cur:
                    print(cur)
                    print("Запись добавлена. ")
                else:
                    print(cur)
                    print("Запись не добавлена.")
                    labelError.configure(text="Ошибка! ")
            except (pymysql.Error, pymysql.Warning) as e:
                print(f'error! {e}')
            
            if cur.rowcount == 1:
                print("Вы успешно зарегистрированы! ")
                ...
                conn.close()
            else:                
                print("Неверные учетные данные! ")
                labelError.configure(text="Неверные учетные данные! ")
        else:
            print("Пароли должны совпадать! ")
            labelError.configure(text="Пароли должны совпадать! ")
    except Exception:
        labelError.configure(text="Ошибка")


##############################
#                            #
#    Building frame items    #
#                            #
##############################
frameRegister = customtkinter.CTkFrame(master=formRegister)
frameRegister.pack(pady=10, padx=10, fill="both", expand=True)

labelWelcome = customtkinter.CTkLabel(master=frameRegister, justify=tkinter.CENTER, width=WIDTH, text="Регистрация")
labelWelcome.pack(pady=10, padx=10)

entryUser = customtkinter.CTkEntry(master=frameRegister, width=WIDTH, placeholder_text="Введите логин")
entryUser.pack(pady=10, padx=10)

entryEmail = customtkinter.CTkEntry(master=frameRegister, width=WIDTH, placeholder_text="Введите электронную почту")
entryEmail .pack(pady=10, padx=10)

entryPassword = customtkinter.CTkEntry(master=frameRegister, width=WIDTH, placeholder_text="Введите пароль", show="*")
entryPassword.pack(pady=10, padx=10)

entryPasswordRepeat = customtkinter.CTkEntry(master=frameRegister, width=WIDTH, placeholder_text="Подтвердите пароль", show="*")
entryPasswordRepeat.pack(pady=10, padx=10)

comboboxScore = customtkinter.CTkComboBox(frameRegister, width=WIDTH, values=["Новичок", "Любитель", "Мастер"])
comboboxScore.pack(pady=12, padx=10)

buttonRegister = customtkinter.CTkButton(master=frameRegister, width=WIDTH, text="Зарегистрироваться", command=buttonRegisterClick)
buttonRegister.pack(pady=10, padx=10)

buttonLogin = customtkinter.CTkButton(master=frameRegister, width=WIDTH, text="Войти (если уже есть аккаунт)", command=buttonLoginClick)
buttonLogin.pack(pady=10, padx=10)

labelError = customtkinter.CTkLabel(master=frameRegister, width=WIDTH, justify=tkinter.CENTER, text="")
labelError.pack(pady=10, padx=10)


#############################
#                           #
#    Form initialization    #
#                           #
#############################
formRegister.mainloop()