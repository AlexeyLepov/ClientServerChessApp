#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#   Program module for building application and graphical interface
#
#################################################################################################################################################################################
#################################################################################################################################################################################

# importing external libraries
import os
import sys
import pymysql
import tkinter
import platform
import itertools
import threading
import customtkinter
import tkinter.messagebox
from types import CellType
from PIL import Image

# importing local files
import config
import chessEngine
import chessLogic


#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#  Setting login window parameters
#
#################################################################################################################################################################################
#################################################################################################################################################################################
class FormLogin(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark") # change theme to DARK
        customtkinter.set_default_color_theme("green") # theme change (COLOR PALETTE)
        ##############################
        #                            #
        #    Building a main form    #
        #                            #
        ##############################
        LOGIN_WIDTH = LOGIN_HEIGHT = 250
        self.geometry(f"{LOGIN_WIDTH+100}x{LOGIN_HEIGHT}")
        self.resizable(False, False)
        self.title("Вход в систему")
        self.protocol("WM_DELETE_WINDOW", self.on_closingLogForm)
        self.eval('tk::PlaceWindow . center')
        # self.withdraw() # hide window
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closingLogForm)
            self.bind("<Command-w>", self.on_closingLogForm)
            self.createcommand('tk::mac::Quit', self.on_closingLogForm)
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
                print("Connected successfully! ")
                try:
                    with conn.cursor() as cur:
                        query = "SELECT username, password FROM users WHERE username = '" + entryUser.get() + "' AND password = '" + entryPassword.get() + "'"
                        cur.execute(query)
                        conn.commit()
                    if cur:
                        print(cur)
                        print("User found!")
                    else:
                        print(cur)
                        print("No record has been added ...")
                        labelError.configure(text="Ошибка! ")
                    if cur.rowcount == 1:
                        App.USERNAME = entryUser.get()
                        App.PASSWORD = entryPassword.get()
                        print(f"Вы вошли в систему как {entryUser.get()}! ")
                        labelError.configure(text="Вход в систему выполнен! ")
                    else:
                        print("Неверные учетные данные! ") # credential
                        labelError.configure(text="Неверные учетные данные! ")
                except (pymysql.Error, pymysql.Warning) as e:
                    print(f'error! {e}')
                    labelError.configure(text=f'Ошибка! {e}')
                finally:
                    conn.close()
            except Exception:
                print("Connection failure ... ")
                labelError.configure(text="Нет подключения к серверу ... ")
        ##############################
        #                            #
        #    Building frame items    #
        #                            #
        ##############################
        frameLogin = customtkinter.CTkFrame(master=self)
        labelWelcome = customtkinter.CTkLabel(master=frameLogin, justify=tkinter.CENTER, width=LOGIN_WIDTH, text="Вход в систему")
        entryUser = customtkinter.CTkEntry(master=frameLogin, width=LOGIN_WIDTH, placeholder_text="Введите логин")
        entryPassword = customtkinter.CTkEntry(master=frameLogin, width=LOGIN_WIDTH, placeholder_text="Введите пароль", show="*")
        buttonLogin = customtkinter.CTkButton(master=frameLogin, text="Войти", width=LOGIN_WIDTH, command = buttonLoginClick)
        labelError = customtkinter.CTkLabel(master=frameLogin, justify=tkinter.CENTER, width=LOGIN_WIDTH, text="")
        # packing items
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
        labelError.pack(
            pady=10, padx=10)
    ########################
    #                      #
    #    operate window    #
    #                      #
    ########################
    def on_closingLogForm(self, event=0):
        app.deiconify()
        self.destroy()
    def startLogForm(self):
        self.mainloop()


#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#  Setting register window parameters
#
#################################################################################################################################################################################
#################################################################################################################################################################################
class FormRegister(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        REG_WIDTH = REG_HEIGHT = 350
        customtkinter.set_appearance_mode("dark") # change theme to DARK
        customtkinter.set_default_color_theme("green") # theme change (COLOR PALETTE)
        ##############################
        #                            #
        #    Building a main form    #
        #                            #
        ##############################
        self.resizable(False, False)
        self.title("Регистрация")
        self.protocol("WM_DELETE_WINDOW", self.on_closingRegForm)
        self.geometry(f"{REG_WIDTH+100}x{REG_HEIGHT}")
        self.eval('tk::PlaceWindow . center')
        # self.withdraw() # hide window
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closingRegForm)
            self.bind("<Command-w>", self.on_closingRegForm)
            self.createcommand('tk::mac::Quit', self.on_closingRegForm)
        ################################
        #                              #
        #    Button click functions    #
        #                              #
        ################################
        def buttonRegisterClick():
            if entryPassword.get() == "" or entryPasswordRepeat.get() == "" or entryUser.get() == "":
                print("Заполните все поля! ")
                labelError.configure(text="Заполните все поля! ")
            elif entryPassword.get() == entryPasswordRepeat.get():
                score = 800 
                if comboboxScore.get() == "Новичок":
                    score = 500
                elif comboboxScore.get() == "Любитель":
                    score = 1000
                elif comboboxScore.get() == "Мастер":
                    score = 2000
                try:
                    conn = pymysql.connect(
                        host = config.host,
                        port = config.port,
                        user = config.user,
                        password = config.password,
                        database = config.database,
                        cursorclass = pymysql.cursors.DictCursor
                    )
                    print("Connected successfully! ")
                    try:
                        with conn.cursor() as cur:
                            query = "INSERT INTO `users` (`username`, `password`, `score`) VALUES ('" + entryUser.get() + "', '" + entryPassword.get() + "', '" + str(score) + "');"
                            cur.execute(query)
                            conn.commit()
                        if cur:
                            print(cur)
                            print("New record added! ")
                        else:
                            print(cur)
                            print("No record has been added ...")
                            labelError.configure(text="Ошибка! ")
                        if cur.rowcount == 1:
                            App.USERNAME = entryUser.get()
                            App.PASSWORD = entryPassword.get()
                            print("Вы успешно зарегистрированы! ")
                            labelError.configure(text="Вы успешно зарегистрированы! ")
                        else:                
                            print("Неверные учетные данные! ")
                            labelError.configure(text="Неверные учетные данные! ")
                    finally:
                        conn.close()
                except Exception:
                    print("Connection failure ... ")
                    labelError.configure(text="Нет подключения к серверу ... ")
            else:
                print("Пароли должны совпадать! ")
                labelError.configure(text="Пароли должны совпадать! ")
        ##############################
        #                            #
        #    Building frame items    #
        #                            #
        ##############################
        frameRegister = customtkinter.CTkFrame(master=self)
        labelWelcome = customtkinter.CTkLabel(master=frameRegister, justify=tkinter.CENTER, width=REG_WIDTH, text="Регистрация")
        entryUser = customtkinter.CTkEntry(master=frameRegister, width=REG_WIDTH, placeholder_text="Введите логин")
        entryPassword = customtkinter.CTkEntry(master=frameRegister, width=REG_WIDTH, placeholder_text="Введите пароль", show="*")
        entryPasswordRepeat = customtkinter.CTkEntry(master=frameRegister, width=REG_WIDTH, placeholder_text="Подтвердите пароль", show="*")
        comboboxScore = customtkinter.CTkComboBox(frameRegister, width=REG_WIDTH, values=["Новичок", "Любитель", "Мастер"])
        buttonRegister = customtkinter.CTkButton(master=frameRegister, width=REG_WIDTH, text="Зарегистрироваться", command = buttonRegisterClick)
        labelError = customtkinter.CTkLabel(master=frameRegister, width=REG_WIDTH, justify=tkinter.CENTER, text="")
        # packing items
        frameRegister.pack(
            pady=10, padx=10, fill="both", expand=True)
        labelWelcome.pack(
            pady=10, padx=10)
        entryUser.pack(
            pady=10, padx=10)
        entryPassword.pack(
            pady=10, padx=10)
        entryPasswordRepeat.pack(
            pady=10, padx=10)
        comboboxScore.pack(
            pady=12, padx=10)
        buttonRegister.pack(
            pady=10, padx=10)
        labelError.pack(
            pady=10, padx=10)
    ########################
    #                      #
    #    operate window    #
    #                      #
    ########################
    def on_closingRegForm(self, event=0):
        app.deiconify()
        self.destroy()
    def startRegForm(self):
        self.mainloop()


#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#  Setting initial main window parameters
#
#################################################################################################################################################################################
#################################################################################################################################################################################
class App(customtkinter.CTk):
    ######################################################################
    #                                                                    #
    #    Setting the parameters and the class for working with colors    #
    #                                                                    #
    ######################################################################
    WIDTH = 880                             # Setting the Application Window Width
    HEIGHT = 680                            # Setting the Application Window height
    DIMENSION = 8.25                        # dimensions count of the chess board
    B_WIDTH = B_HEIGHT = 650                # width and height of the chess board
    SQ_SIZE = B_HEIGHT / DIMENSION          # the size of each of the sWPquares in the board
    PIECE_DIR = "Assets/PiecesModern/"      # Standard piece Image Folder
    PIECE_SIZE = 48
    # virtual board
    board: chessEngine.Board = None
    # profile info
    global USERNAME
    global PASSWORD
    # color class
    class Colors:
        Board_White = "#f9dcc4"                 # Standard color for white board margins
        Board_Black = "#023047"                 # Standart color for black chessboard fields (for black ones)
        Field_Correct_Move = "#a7c957"          # Color for fields that a piece can move to
        Field_Correct_Capture = "#f28482"       # The color of the fields in which the enemy piece stands
        Moving_Piece = "#87a937"                # The color of the selected piece
        Users_Current = chessEngine.Color.WHITE # Player Color
        Menu_Button = "#6a994e"
        Signs = "#2b2d42"
        HighlightedSigns = "#013a63"
    # selected button class
    class SelectedButtonField:
        selected = False
        row = 0
        col = 0
    ################################################
    #                                              #
    #    Class initialization - object creation    #
    #                                              #
    ################################################
    def __init__(self):
        super().__init__() # Parent class definition
        # Setting initial window settings
        customtkinter.set_appearance_mode("dark") # change theme to DARK
        customtkinter.set_default_color_theme("green") # theme change (COLOR PALETTE)
        self.resizable(False, False)
        self.title("Игра в Шахматы")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.eval('tk::PlaceWindow . center')
        # self.withdraw() # hide window
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)
        # Reading the image of pieces and "fitting" to the size of one cell of the virtual chessboard
        self.BB = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bB.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bB.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.BP = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bp.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bp.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.BN = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bN.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bN.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.BR = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bR.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bR.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.BQ = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bQ.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bQ.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.BK = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bK.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bK.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.WB = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wB.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wB.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.WP = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wp.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wp.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.WN = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wN.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wN.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.WR = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wR.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wR.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.WQ = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wQ.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wQ.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
        self.WK = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wK.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wK.png')), size=(App.PIECE_SIZE,App.PIECE_SIZE))
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
            conn.close()
        except Exception:
            print("Connection failure ... ")


#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#   Create panels (frames)
#
#################################################################################################################################################################################
#################################################################################################################################################################################
        # Grid layout setting (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        ###################################
        #                                 #
        #    Creating a sidebar (MENU)    #
        #                                 #
        ###################################
        self.frame_menu = customtkinter.CTkFrame(master=self, width=140, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nswe")
        self.frame_menu.grid_rowconfigure(6, weight=1)
        self.frame_menu.grid_rowconfigure(11, minsize=10)
        # Adding elements to the menu
        self.label_menu = customtkinter.CTkLabel(master=self.frame_menu, text="МЕНЮ", font=("Roboto Medium", -16)) # Label
        self.button_playClient = customtkinter.CTkButton(master=self.frame_menu, text="Тренироваться", fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.button_playClient_event)
        self.button_profile = customtkinter.CTkButton(master=self.frame_menu, text="Профиль", fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.button_profile_event)
        self.button_info = customtkinter.CTkButton(master=self.frame_menu, text="О программе", fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.button_info_event)
        self.switch_dark_theme = customtkinter.CTkSwitch(master=self.frame_menu, text="Темная тема", command=self.change_theme_mode) # Dark theme switcher
        # Packing elements
        self.label_menu.grid(
            row=0, column=0, pady=10, padx=10)
        self.button_playClient.grid(
            row=1, column=0, pady=10, padx=10)
        self.button_profile.grid(
            row=2, column=0, pady=10, padx=10)
        self.button_info.grid(
            row=3, column=0, pady=10, padx=10)
        self.switch_dark_theme.grid(
            row=10, column=0, pady=10, padx=10, sticky="w")
        ###########################################
        #                                         #
        #    Creating an "about program" frame    #
        #                                         #
        ###########################################
        self.frame_info = customtkinter.CTkFrame(master=self)
        self.frame_info.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.frame_info.rowconfigure(14, weight=10)
        self.frame_info.columnconfigure(0, weight=1)
        # Adding elements to the form
        self.label_info = customtkinter.CTkLabel(master=self.frame_info, text="О программе", font=("Roboto Medium", -16))
        self.label_info_info = customtkinter.CTkLabel(master=self.frame_info, height=100, font=("Roboto Medium", -16), fg_color=("white", "gray38"), justify=tkinter.LEFT,
            text=" \nРеализация клиент-серверной программной системы \"Игра в Шахматы\". \n")
        self.label_info_authors = customtkinter.CTkLabel(master=self.frame_info, height=200, font=("Roboto Medium", -16), fg_color=("white", "gray38"), justify=tkinter.LEFT,
            text="\n\nРазработкой занимались студенты СПбГЭТУ \"ЛЭТИ\", гр. 1308:\n\n" +
                " - Томилов Даниил" + "; \n" +
                " - Макаров Максим" + "; \n" +
                " - Мельник Даниил" + "; \n" +
                " - Лепов Алексей"  + ". \n" )
        # Packing elements
        self.label_info.grid(
            row=0, column=0, pady=10, padx=10, sticky="we")
        self.label_info_info.grid(
            row=1, column=0, padx=10, pady=10, sticky="we")
        self.label_info_authors.grid(
            row=2, column=0, padx=10, pady=10, sticky="we")
        ############################################
        #                                          #
        #    Creating a frame for playing chess    #
        #                                          #
        ############################################
        self.frame_playClient = customtkinter.CTkFrame(master=self)
        self.frame_playClient.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.frame_playClient.rowconfigure(14, weight=10)
        self.frame_playClient.columnconfigure(0, weight=1)
        # Adding elements to the form
        self.frame_chessClient = customtkinter.CTkFrame(master=self.frame_playClient, width=App.B_WIDTH, height=App.B_HEIGHT, fg_color=("#D1D5D8","#2A2D2E"))
        self.frame_board = customtkinter.CTkFrame(master=self.frame_chessClient, fg_color=(App.Colors.Signs, App.Colors.Signs), width=App.B_WIDTH, height=App.B_HEIGHT)
        # Packing elements
        self.frame_chessClient.grid(
            row=0, column=0, padx=0, pady=0, sticky="nswe")
        self.frame_board.grid(
            row=1, column=0, padx=5, pady=0, sticky="nswe")
        ###################################
        #                                 #
        #    Creating a profile frame     #
        #                                 #
        ###################################
        self.frame_profile = customtkinter.CTkFrame(master=self)
        self.frame_profile.rowconfigure(14, weight=10)
        self.frame_profile.columnconfigure(0, weight=1)
        self.frame_profile.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        # Adding elements to the form
        self.frame_profileInfo = customtkinter.CTkLabel(master=self.frame_profile, height=100, fg_color=("#C0C2C5","#343638"))
        self.frame_profileButtonLogin = customtkinter.CTkButton(master=self.frame_profile, text="Войти", 
            fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonLogin_event)
        self.frame_profileButtonReg = customtkinter.CTkButton(master=self.frame_profile, text="Зарегистрироваться", 
            fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonReg_event)
        self.frame_profileButtonLogout = customtkinter.CTkButton(master=self.frame_profile, text="Выйти", 
            fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonLogout_event)
        self.frame_profileButtonPlay = customtkinter.CTkButton(master=self.frame_profile, text="Играть", 
            fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonPlay_event)
        # Packing elements
        self.frame_profileInfo.grid(
            row=0, column=0, sticky="nswe", padx=5, pady=5)
        # self.frame_profileButtonLogin.grid(
        #     row=1, column=0, sticky="nswe", padx=5, pady=5)
        # self.frame_profileButtonReg.grid(
        #     row=2, column=0, sticky="nswe", padx=5, pady=5)
        

#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#   Setting default parameters
#
#################################################################################################################################################################################
#################################################################################################################################################################################
        ##########################################
        #                                        #
        #    Displaying the starting position    #
        #                                        #
        ##########################################
        
        def displayStartingPosition():
            alphabeticalNumeration = ['a','b','c','d','e','f','g','h']
            self.ButtonField = [[0 for _ in range(8)] for _ in range(8)]
            self.ButtonFieldSign = [[0 for _ in range(2)] for _ in range(8)]
            for i, j in itertools.product(range(8), range(8)):
                self.ButtonField[i][j] = customtkinter.CTkButton(master=self.frame_board, width=App.SQ_SIZE, height=App.SQ_SIZE, text="", hover_color=(App.Colors.Field_Correct_Move,App.Colors.Field_Correct_Move))
                self.ButtonField[i][j].grid(row=7-i, column=j+1, sticky="sw", padx=0, pady=0)
            for i, j in itertools.product(range(8), range(2)):
                if j==0:
                    self.ButtonFieldSign[i][j] = customtkinter.CTkButton(master=self.frame_board, width=App.SQ_SIZE, height=App.SQ_SIZE/4, text=f"{alphabeticalNumeration[i]}", hover_color=(App.Colors.Signs,App.Colors.Signs), fg_color=(App.Colors.Signs,App.Colors.Signs))
                    self.ButtonFieldSign[i][j].grid(row=8-j, column=i+1, sticky="sw", padx=0, pady=0)
                else:
                    self.ButtonFieldSign[i][j] = customtkinter.CTkButton(master=self.frame_board, width=App.SQ_SIZE/4, height=App.SQ_SIZE, text=f"{i+1}", hover_color=(App.Colors.Signs,App.Colors.Signs), fg_color=(App.Colors.Signs,App.Colors.Signs))
                    self.ButtonFieldSign[i][j].grid(row=7-i, column=0, sticky="sw", padx=0, pady=0)
            self.RecolorBoard()
            self.board = chessEngine.Board()
            self.UpdateBoard()
            for i, j in itertools.product(range(8), range(8)):
                self.ButtonField[i][j].configure(command = lambda row=i,col=j: self.ButtonField_event(row,col))
                # command = lambda row=i,col=j: self.thread(row,col,self.ButtonField,self)
            # for i, j in itertools.product(range(8), range(8)):
            #     self.ButtonField[i][j].bind("<Enter>", lambda event,row=i,col=j: self.onhover(event,row,col), add='+')
            #     self.ButtonField[i][j].bind("<Leave>", lambda event,row=i,col=j: self.onleave(event,row,col), add='+')
        displayStartingPosition()
        ##################################
        #                                #
        #    Assigning Default Values    #
        #                                #
        ##################################
        self.hide_menu_frames()
        self.frame_playClient.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
        self.switch_dark_theme.select()
        if self.switch_dark_theme.get() == 1:
            self.button_playClient.configure(fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button))
        else:
            self.button_playClient.configure(fg_color=(App.Colors.Menu_Button))


#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#   Functions for working with windows and panels (frames)
#
#################################################################################################################################################################################
#################################################################################################################################################################################
    def updateProfileInfo(self):
        try:
            conn = pymysql.connect(
                host = config.host,
                port = config.port,
                user = config.user,
                password = config.password,
                database = config.database,
                cursorclass = pymysql.cursors.DictCursor
            )
            print("Connected successfully! ")
            try:
                with conn.cursor() as cur:
                    query = f"SELECT * FROM `users` WHERE `username` = '{App.USERNAME}' and `password` = '{App.PASSWORD}'"
                    cur.execute(query)
                    conn.commit()
                    print(cur)
                if cur.rowcount == 1:
                    self.frame_profileInfo.configure(text=f"Добро пожаловать, {App.USERNAME}!")
                    print(f"Добро пожаловать, {App.USERNAME}!")
                    # self.frame_profileButtonLogin.configure(text="Выйти", command=self.frame_profileButtonLogout)
                    # self.frame_profileButtonLogin.grid(
                    #     row=1, column=0, sticky="nswe", padx=5, pady=5)
                    # self.frame_profileButtonReg.grid(
                    #     row=2, column=0, sticky="nswe", padx=5, pady=5)
                    self.frame_profileButtonLogin.destroy
                    self.frame_profileButtonReg.destroy
                    self.frame_profileButtonLogout = customtkinter.CTkButton(master=self.frame_profile, text="Выйти", 
                        fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonLogout_event)
                    self.frame_profileButtonPlay = customtkinter.CTkButton(master=self.frame_profile, text="Играть", 
                        fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonPlay_event)
                    self.frame_profileButtonLogout.grid(
                        row=1, column=0, sticky="nswe", padx=5, pady=5)
                    self.frame_profileButtonPlay.grid(
                        row=2, column=0, sticky="nswe", padx=5, pady=5)
                else:                
                    print("Добро пожаловать, гость! - else")
                    self.frame_profileButtonLogin = customtkinter.CTkButton(master=self.frame_profile, text="Войти", 
                        fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonLogin_event)
                    self.frame_profileButtonReg = customtkinter.CTkButton(master=self.frame_profile, text="Зарегистрироваться", 
                        fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonReg_event)
                    self.frame_profileInfo.configure(text="Добро пожаловать, гость!")
                    self.frame_profileButtonLogin.grid(
                        row=1, column=0, sticky="nswe", padx=5, pady=5)
                    self.frame_profileButtonReg.grid(
                        row=2, column=0, sticky="nswe", padx=5, pady=5)
                    self.frame_profileButtonLogout.destroy
                    self.frame_profileButtonPlay.destroy
            finally:
                conn.close()
        except Exception:
            print("Добро пожаловать, гость! - Exception")
            self.frame_profileInfo.configure(text="Добро пожаловать, гость!")
            self.frame_profileButtonLogin = customtkinter.CTkButton(master=self.frame_profile, text="Войти", 
                fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonLogin_event)
            self.frame_profileButtonReg = customtkinter.CTkButton(master=self.frame_profile, text="Зарегистрироваться", 
                fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button), width=180, height=60, command=self.frame_profileButtonReg_event)
            self.frame_profileButtonLogin.grid(
                row=1, column=0, sticky="nswe", padx=5, pady=5)
            self.frame_profileButtonReg.grid(
                row=2, column=0, sticky="nswe", padx=5, pady=5)
            self.frame_profileButtonLogout.destroy
            self.frame_profileButtonPlay.destroy
    #####################################
    #                                   #
    #    Piece image return function    #
    #                                   #
    #####################################
    def pieceImage(self, name, color):
        if color == chessEngine.Color.WHITE:
            if name == "pawn":
                return self.WP
            elif name == "knight":
                return self.WN
            elif name == "bishop":
                return self.WB
            elif name == "rook":
                return self.WR
            elif name == "queen":
                return self.WQ
            elif name == "king":
                return self.WK
            else:
                raise ValueError("Invalid piece name")
        elif color == chessEngine.Color.BLACK:
            if name == "pawn":
                return self.BP
            elif name == "knight":
                return self.BN
            elif name == "bishop":
                return self.BB
            elif name == "rook":
                return self.BR
            elif name == "queen":
                return self.BQ
            elif name == "king":
                return self.BK
            else:
                raise ValueError("Invalid piece name")
        else:
            raise ValueError("Invalid color")
    ###########################################################
    #                                                         #
    #    Functions for calling windows and other functions    #
    #                                                         #
    ###########################################################
    def hide_menu_frames(self):
        self.frame_info.grid_forget()
        self.frame_profile.grid_forget()
        self.frame_playClient.grid_forget()
        self.button_info.configure(fg_color=("gray75", "gray30"))
        self.button_profile.configure(fg_color=("gray75", "gray30"))
        self.button_playClient.configure(fg_color=("gray75", "gray30"))
    ################################################
    #                                              #
    #    Functions for managing window settings    #
    #                                              #
    ################################################
    def button_info_event(self):
        self.hide_menu_frames()
        self.frame_info.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        if self.switch_dark_theme.get() == 1:
            self.button_info.configure(fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button))
        else:
            self.button_info.configure(fg_color=(App.Colors.Menu_Button))
    def button_playClient_event(self):
        self.hide_menu_frames()
        self.frame_playClient.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        if self.switch_dark_theme.get() == 1:
            self.button_playClient.configure(fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button))
        else:
            self.button_playClient.configure(fg_color=(App.Colors.Menu_Button))
    def button_profile_event(self):
        self.hide_menu_frames()
        self.frame_profile.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.updateProfileInfo()
        if self.switch_dark_theme.get() == 1:
            self.button_profile.configure(fg_color=(App.Colors.Menu_Button, App.Colors.Menu_Button))
        else:
            self.button_profile.configure(fg_color=(App.Colors.Menu_Button))
    ###############################
    #                             #
    #    theme change function    #
    #                             #
    ###############################
    def change_theme_mode(self):
        if self.switch_dark_theme.get() == 1:
            customtkinter.set_appearance_mode("Dark")
        else:
            customtkinter.set_appearance_mode("Light")
    #########################################################
    #                                                       #
    #    cleaning the window and exiting the application    #
    #                                                       #
    #########################################################
    def on_closing(self, event=0):
        self.destroy()
    def start(self):
        self.mainloop()
    ###################################################
    #                                                 #
    #    clocking on login button on profile frame    #
    #                                                 #
    ###################################################
    def frame_profileButtonLogin_event(self):
        self.button_playClient_event()
        App.withdraw(self)
        form_log = FormLogin()
        form_log.startLogForm()
        self.updateProfileInfo() 
    def frame_profileButtonReg_event(self):
        App.withdraw(self)
        form_reg = FormRegister()
        form_reg.startRegForm()
    def frame_profileButtonLogout_event(self):
        App.USERNAME = App.PASSWORD = None
        self.updateProfileInfo()            
    def frame_profileButtonPlay_event(self):
        ...

    ####################################
    #                                  #
    #    threaded bot turn function    #
    #                                  #
    ####################################
    def thread(self):
        def _bot_turn():
            try:
                for i, j in itertools.product(range(8), range(8)):
                    self.ButtonField[i][j].configure(state="disabled")

                game_tree = chessLogic.GameTree(self.board.get_FEN(),False)
                game_tree.alpha_beta_evaluation(3)
                move,_ = game_tree.suggest_move()
                self.board.move_piece(self.board.get_piece_arr()[move[0][0]][move[0][1]],chessEngine.Position(move[1][0],move[1][1]))
                self.ButtonField[move[0][0]][move[0][1]].configure(image = None)
                self.UpdateBoard()

                for i, j in itertools.product(range(8), range(8)):
                    self.ButtonField[i][j].configure(state="normal")
            except Exception as e:
                print(e)
                for i, j in itertools.product(range(8), range(8)):
                    self.ButtonField[i][j].configure(state="normal")
                popup = tkinter.Tk()
                popup.wm_title("Ошибка!")
                label = tkinter.Label(popup, text=f"У бота проблемы: \n{e}", font=("Verdana", 10))
                label.pack(side="top", fill="x", pady=10)
                B1 = tkinter.Button(popup, text="Okay", command = popup.destroy)
                B1.pack()
                popup.mainloop()
        threading.Thread(target=_bot_turn).start()
        

#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#   Functions for moving pieces
#
#################################################################################################################################################################################
#################################################################################################################################################################################
    #######################################################
    #                                                     #
    #    Functions for pressing buttons - chess fields    #
    #                                                     #
    #######################################################
    # def onleave(self,event,row,col):
    #     self.ButtonFieldSign[col][0].configure(fg_color=(App.Colors.Signs,App.Colors.Signs))
    #     self.ButtonFieldSign[row][1].configure(fg_color=(App.Colors.Signs,App.Colors.Signs))
    # def onhover(self,event,row,col):
    #     self.ButtonFieldSign[col][0].configure(fg_color=(App.Colors.HighlightedSigns,App.Colors.HighlightedSigns))
    #     self.ButtonFieldSign[row][1].configure(fg_color=(App.Colors.HighlightedSigns,App.Colors.HighlightedSigns))
    def ButtonField_event(self,row,col):
        ''' Some of the functions from chessEngine.py used:
        correct_moves - list of moves that a piece can operate on - except for those in which it is possible to capture the enemy
        correct_captures - list of all possible captures of enemy pieces
        move_piece - piece moving
        '''
        self.RecolorBoard()
        position = self.SelectedField()
        # print(self.board) # debbug
        # if no button is selected
        
        arr = self.board.get_piece_arr()
        if position is None: 
            if arr[row][col] is None:
                return
            if arr[row][col].color != self.board.active_color:
                return
            piece = arr[row][col]
            self.ButtonField[row][col].configure(fg_color=(App.Colors.Moving_Piece, App.Colors.Moving_Piece))
            App.SelectedButtonField.selected = True
            App.SelectedButtonField.row = row
            App.SelectedButtonField.col = col
            correct_moves = piece.correct_moves(arr)
            correct_captures = piece.correct_captures(arr)
            for move in correct_moves:
                self.ButtonField[move.row][move.col].configure(fg_color=(App.Colors.Field_Correct_Move, App.Colors.Field_Correct_Move))
            for capture in correct_captures:
                self.ButtonField[capture.row][capture.col].configure(fg_color=(App.Colors.Field_Correct_Capture, App.Colors.Field_Correct_Capture))
        # if there is a selected one
        else:
            App.SelectedButtonField.selected = False
            App.SelectedButtonField.row = row
            App.SelectedButtonField.col = col
            piece = self.board.get_piece_arr()[position.row][position.col]
            if self.board.move_piece(piece, chessEngine.Position(row, col)):
                self.UpdateBoard()
                self.thread()
            str = self.board.get_str_arr()
    #######################################################
    #                                                     #
    #    Function to paint the board in default colors    #
    #                                                     #
    #######################################################
    def RecolorBoard(self):
        for i, j in itertools.product(range(8), range(8)):
            if ((i + j) % 2) == 0:
                if self.ButtonField[i][j].cget("fg_color") != (App.Colors.Board_Black, App.Colors.Board_Black):
                    self.ButtonField[i][j].configure(fg_color=(App.Colors.Board_Black, App.Colors.Board_Black))
            else:
                if self.ButtonField[i][j].cget("fg_color") != (App.Colors.Board_Black, App.Colors.Board_Black):
                    self.ButtonField[i][j].configure(fg_color=(App.Colors.Board_White, App.Colors.Board_White))

    def UpdateBoard(self):
        self.RecolorBoard()
        arr = self.board.get_piece_arr()
        for i in range(8):
            for j in range(8):
                piece = arr[i][j]
                if piece == None:
                    image = None
                else:
                    image = self.pieceImage(piece.name, piece.color)
                if self.ButtonField[i][j].cget("image") != image:
                    self.ButtonField[i][j].configure(image = None)
                    self.ButtonField[i][j].configure(image = image)

    ###############################################################
    #                                                             #
    #    Function to return null if no shape has been selected    #
    #                                                             #
    ###############################################################
    def SelectedField(self):
        if App.SelectedButtonField.selected == True:
            position = chessEngine.Position
            position.row = App.SelectedButtonField.row
            position.col = App.SelectedButtonField.col
            return position
        # if clicked piece has the same color as selected one
        # elif App.SelectedButtonField.selected == False and ...: 
            # position = chessEngine.Position
            # position.row = App.SelectedButtonField.row
            # position.col = App.SelectedButtonField.col
            # return position 
        return None

 
#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#   Program initialization
#
#################################################################################################################################################################################
#################################################################################################################################################################################
############################
#                          #
#    Application launch    #
#                          #
############################
if __name__ == "__main__":
    app = App()
    app.start()
