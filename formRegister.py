import tkinter
import customtkinter


##############################
#                            #
#    Building a main form    #
#                            #
##############################
customtkinter.set_appearance_mode("dark")  # Modes: "System", "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"

WIDTH = HEIGHT = 340

formRegister = customtkinter.CTk()
formRegister.geometry(f"{WIDTH+100}x{HEIGHT+100}")
formRegister.resizable(False, False)
formRegister.title("Регистрация")


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
frameRegister = customtkinter.CTkFrame(master=formRegister)
frameRegister.pack(pady=10, padx=10, fill="both", expand=True)

labelWelcome = customtkinter.CTkLabel(master=frameRegister, justify=tkinter.CENTER, width=WIDTH, text="Регистрация")
labelWelcome.pack(pady=10, padx=10)

entryUser = customtkinter.CTkEntry(master=frameRegister, width=WIDTH, placeholder_text="Введите логин")
entryUser.pack(pady=10, padx=10)

entryEmail = customtkinter.CTkEntry(master=frameRegister, width=WIDTH, placeholder_text="Введите электронную почту")
entryEmail .pack(pady=10, padx=10)

entryPassword = customtkinter.CTkEntry(master=frameRegister, width=WIDTH, placeholder_text="Введите пароль")
entryPassword.pack(pady=10, padx=10)

entryPasswordRepeat = customtkinter.CTkEntry(master=frameRegister, width=WIDTH, placeholder_text="Подтвердите пароль")
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