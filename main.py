####################################################################################################
#                                                                                                  #
#    ##########################################################################################    #
#    #                                                                                        #    #
#    #    Программный модуль инициализации приложения и построения графического интерфейса    #    #
#    #                                                                                        #    #
#    ##########################################################################################    #
#                                                                                                  #
####################################################################################################

from ctypes.wintypes import WPARAM
import os
import sys
import tkinter
import itertools
import threading
import subprocess
import customtkinter
import tkinter.messagebox
import tkinter.font as tkFont
import platform
if platform.system == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'

import chessBoard
import chessEngine


#####################################################
#                                                   #
#    Создание окна для работы пользователя - GUI    #
#                                                   #
#####################################################
class App(customtkinter.CTk):
    WIDTH = 990  # Задание ширины окна приложения
    HEIGHT = 770  # Задание высоты окна приложения

    def __init__(self):
        super().__init__()  # Определение родительского класса

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.resizable(False, False)
        B_WIDTH = B_HEIGHT = 720            # width and height of the chess board
        DIMENSION = 8                       # the dimensions of the chess board
        SQ_SIZE = B_HEIGHT // DIMENSION     # the size of each of the sWPquares in the board
        PIECE_DIR = "Assets/PiecesModern/"  # Стандартная папка для изображений фигур
        B_COLOR_WHITE = "#f9dcc4"           # Стандартный цвет для белых полей доски
        B_COLOR_BLACK = "#023047"           # Standart color for black chessboard fields (для черных)
        CURRENT_COLOR = chessEngine.Color.WHITE

        BB = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'bB.png')).subsample(DIMENSION, DIMENSION)
        BP = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'bp.png')).subsample(DIMENSION, DIMENSION)
        BN = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'bN.png')).subsample(DIMENSION, DIMENSION)
        BR = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'bR.png')).subsample(DIMENSION, DIMENSION)
        BQ = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'bQ.png')).subsample(DIMENSION, DIMENSION)
        BK = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'bK.png')).subsample(DIMENSION, DIMENSION)
        BLANCK = tkinter.PhotoImage(file = os.path.join("Assets/BLANK/", 'BLANK_512x512.png')).subsample(DIMENSION, DIMENSION)
        WB = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'wB.png')).subsample(DIMENSION, DIMENSION)
        WP = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'wp.png')).subsample(DIMENSION, DIMENSION)
        WN = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'wN.png')).subsample(DIMENSION, DIMENSION)
        WR = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'wR.png')).subsample(DIMENSION, DIMENSION)
        WQ = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'wQ.png')).subsample(DIMENSION, DIMENSION)
        WK = tkinter.PhotoImage(file = os.path.join(PIECE_DIR, 'wK.png')).subsample(DIMENSION, DIMENSION)

        self.title("Игра в Шахматы")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)


        ####################################
        #                                  #
        #    Создание родительских окон    #
        #                                  #
        ####################################
        # Настройка макета сетки (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        # Создание окон (1x2)
        self.frame_left_menu = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left_menu.grid(row=0, column=0, sticky="nswe")
        self.frame_right_play = customtkinter.CTkFrame(master=self)
        self.frame_right_play.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.frame_right_info = customtkinter.CTkFrame(master=self)
        self.frame_right_info.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)


        #######################
        #                     #
        #    Создание МЕНЮ    #
        #                     #
        #######################
        # Настройка макета сетки
        self.frame_left_menu.grid_rowconfigure(6, weight=1)
        self.frame_left_menu.grid_rowconfigure(11, minsize=10)
        self.label_menu = customtkinter.CTkLabel(master=self.frame_left_menu, text="МЕНЮ", text_font=("Roboto Medium", -16))
        self.label_menu.grid(row=0, column=0, pady=10, padx=10)
        # Кнопки
        self.button_play = customtkinter.CTkButton(master=self.frame_left_menu, text="Играть", fg_color=("gray75", "#64897e"), width=180, height=40, command=self.button_play_event)
        self.button_play.grid(row=1, column=0, pady=10, padx=20)
        self.button_info = customtkinter.CTkButton(master=self.frame_left_menu, text="О программе", fg_color=("gray75", "#64897e"), width=180, height=40, command=self.button_info_event)
        self.button_info.grid(row=2, column=0, pady=10, padx=20)
        # Переключатель темной темы
        self.switch_dark_theme = customtkinter.CTkSwitch(master=self.frame_left_menu, text="Темная тема", command=self.change_mode)
        self.switch_dark_theme.grid(row=10, column=0, pady=10, padx=20, sticky="w")


        #################################################
        #                                               #
        #    Создание окна с информацией о программе    #
        #                                               #
        #################################################
        # Настройка макета сетки
        # Настройка макета сетки
        self.frame_right_info.rowconfigure(14, weight=10)
        self.frame_right_info.columnconfigure(0, weight=1)

        self.label_info = customtkinter.CTkLabel(master=self.frame_right_info, text="Информация о программе",
                                                 text_font=("Roboto Medium", -16))
        self.label_info.grid(row=0, column=0, pady=10, padx=10)

        self.label_info_info = customtkinter.CTkLabel(master=self.frame_right_info, height=100,
                                                      text_font=("Roboto Medium", -16), fg_color=("white", "gray38"),
                                                      justify=tkinter.LEFT,
                                                      text=" \nРеализация клиент-серверной программной системы \"Игра в Шахматы\". \n")
        self.label_info_info.grid(row=1, column=0, sticky="we", padx=15, pady=15)

        self.label_info_authors = customtkinter.CTkLabel(master=self.frame_right_info, height=200,
                                                         text_font=("Roboto Medium", -16), fg_color=("white", "gray38"),
                                                         justify=tkinter.LEFT,
                                                         text="\nРазработкой занимались студенты СПбГЭТУ (ЛЭТИ), гр. 1308:\n\n" +
                                                              "Мельник Даниил" + "; \n" +
                                                              "Томилов Даниил" + "; \n" +
                                                              "Лепов Алексей" + ". \n")
        self.label_info_authors.grid(row=2, column=0, sticky="we", padx=15, pady=15)


        #########################################
        #                                       #
        #    Создание окна для игр в шахматы    #
        #                                       #
        #########################################
        # Настройка макета сетки
        self.frame_right_play.rowconfigure(14, weight=10)
        self.frame_right_play.columnconfigure(0, weight=1)
        self.frame_board = customtkinter.CTkFrame(master=self.frame_right_play, fg_color=(B_COLOR_WHITE, B_COLOR_BLACK), width=B_WIDTH, height=B_HEIGHT)
        self.frame_board.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)

        self.ButtonField = [[0 for _ in range(8)] for _ in range(8)]

        for i, j in itertools.product(range(8), range(8)):
            self.ButtonField[i][j] = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text="") if ((i + j) % 2) == 0 else customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text="")
            self.ButtonField[i][j].grid(row=7-i, column=j, sticky="sw", padx=0, pady=0)

        if CURRENT_COLOR == chessEngine.Color.WHITE:
            self.ButtonField[0][0].configure(image = WR)
            self.ButtonField[0][1].configure(image = WN)
            self.ButtonField[0][2].configure(image = WB)
            self.ButtonField[0][3].configure(image = WQ)
            self.ButtonField[0][4].configure(image = WK)
            self.ButtonField[0][5].configure(image = WB)
            self.ButtonField[0][6].configure(image = WN)
            self.ButtonField[0][7].configure(image = WR)
            for i in range(8):
                self.ButtonField[1][i].configure(image = WP)
            for i in range(8):
                self.ButtonField[6][i].configure(image = BP)
            self.ButtonField[7][0].configure(image = BR)
            self.ButtonField[7][1].configure(image = BN)
            self.ButtonField[7][2].configure(image = BB)
            self.ButtonField[7][3].configure(image = BQ)
            self.ButtonField[7][4].configure(image = BK)
            self.ButtonField[7][5].configure(image = BB)
            self.ButtonField[7][6].configure(image = BN)
            self.ButtonField[7][7].configure(image = BR)
        else:    
            self.ButtonField[7][0].configure(image = WR)
            self.ButtonField[7][1].configure(image = WN)
            self.ButtonField[7][2].configure(image = WB)
            self.ButtonField[7][3].configure(image = WQ)
            self.ButtonField[7][4].configure(image = WK)
            self.ButtonField[7][5].configure(image = WB)
            self.ButtonField[7][6].configure(image = WN)
            self.ButtonField[7][7].configure(image = WR)
            for i in range(8):
                self.ButtonField[1][i].configure(image = BP)
            for i in range(8):
                self.ButtonField[6][i].configure(image = WP)
            self.ButtonField[0][0].configure(image = BR)
            self.ButtonField[0][1].configure(image = BN)
            self.ButtonField[0][2].configure(image = BB)
            self.ButtonField[0][3].configure(image = BQ)
            self.ButtonField[0][4].configure(image = BK)
            self.ButtonField[0][5].configure(image = BB)
            self.ButtonField[0][6].configure(image = BN)
            self.ButtonField[0][7].configure(image = BR)

        ##########################################
        #                                        #
        #    Присвение значений по умолчанию     #
        #                                        #
        ##########################################
        self.hide_menu_frames()
        self.frame_right_play.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.switch_dark_theme.select()
        if self.switch_dark_theme.get() == 1:
            self.button_play.configure(fg_color=("gray75", "#5c8da4"))
        else:
            self.button_play.configure(fg_color=("#7db8d4"))


    ###################################################
    #                                                 #
    #    Функции для вызова окон и других функций     #
    #                                                 #
    ###################################################
    def hide_menu_frames(self):
        self.frame_right_info.grid_forget()
        self.frame_right_play.grid_forget()
        self.button_info.configure(fg_color=("gray75", "gray30"))
        self.button_play.configure(fg_color=("gray75", "gray30"))


    ##################################################
    #                                                #
    #    Функции для управления параметрами окон     #
    #                                                #
    ##################################################
    def button_info_event(self):
        self.hide_menu_frames()
        self.frame_right_info.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        if self.switch_dark_theme.get() == 1:
            self.button_info.configure(fg_color=("gray75", "#5c8da4"))
        else:
            self.button_info.configure(fg_color=("#7db8d4"))

    def button_play_event(self):
        self.hide_menu_frames()
        self.frame_right_play.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        if self.switch_dark_theme.get() == 1:
            self.button_play.configure(fg_color=("gray75", "#5c8da4"))
        else:
            self.button_play.configure(fg_color=("#7db8d4"))

    def change_mode(self):
        if self.switch_dark_theme.get() == 1:
            customtkinter.set_appearance_mode("Dark")
        else:
            customtkinter.set_appearance_mode("Light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

  
    ######################################################
    #                                                    #
    #    Функции для нажатия кнопок - шахматных полей    #
    #                                                    #
    ######################################################
    def button_field_event(self):
        self.configure(fg_color=("7db8d4", "#7db8d4"))

    def default_field_color(self):
        self.configure(fg_color=("7db8d4", "#7db8d4"))


##################################
#                                #
#    Инициализация программы     #
#                                #
##################################
if __name__ == "__main__":
    app = App()
    app.start()
    