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
        self.ButtonA1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BR)
        self.ButtonA2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BN)
        self.ButtonA3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BB)
        self.ButtonA4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BQ)
        self.ButtonA5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BK)
        self.ButtonA6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BB)
        self.ButtonA7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BN)
        self.ButtonA8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BR)
        self.ButtonA1.grid(row=0, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonA2.grid(row=0, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonA3.grid(row=0, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonA4.grid(row=0, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonA5.grid(row=0, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonA6.grid(row=0, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonA7.grid(row=0, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonA8.grid(row=0, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonB1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BP)
        self.ButtonB2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BP)
        self.ButtonB3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BP)
        self.ButtonB4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BP)
        self.ButtonB5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BP)
        self.ButtonB6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BP)
        self.ButtonB7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BP)
        self.ButtonB8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BP)
        self.ButtonB1.grid(row=1, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonB2.grid(row=1, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonB3.grid(row=1, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonB4.grid(row=1, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonB5.grid(row=1, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonB6.grid(row=1, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonB7.grid(row=1, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonB8.grid(row=1, column=7, sticky="sw", padx=0, pady=0)        
        self.ButtonC1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonC2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonC3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonC4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonC5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonC6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonC7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonC8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonC1.grid(row=2, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonC2.grid(row=2, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonC3.grid(row=2, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonC4.grid(row=2, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonC5.grid(row=2, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonC6.grid(row=2, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonC7.grid(row=2, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonC8.grid(row=2, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonD1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonD2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonD3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonD4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonD5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonD6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonD7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonD8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonD1.grid(row=3, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonD2.grid(row=3, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonD3.grid(row=3, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonD4.grid(row=3, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonD5.grid(row=3, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonD6.grid(row=3, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonD7.grid(row=3, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonD8.grid(row=3, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonE1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonE2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonE3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonE4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonE5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonE6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonE7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonE8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonE1.grid(row=4, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonE2.grid(row=4, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonE3.grid(row=4, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonE4.grid(row=4, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonE5.grid(row=4, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonE6.grid(row=4, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonE7.grid(row=4, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonE8.grid(row=4, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonF1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonF2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonF3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonF4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonF5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonF6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonF7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonF8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = BLANCK)
        self.ButtonF1.grid(row=5, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonF2.grid(row=5, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonF3.grid(row=5, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonF4.grid(row=5, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonF5.grid(row=5, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonF6.grid(row=5, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonF7.grid(row=5, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonF8.grid(row=5, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonG1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WP)
        self.ButtonG2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WP)
        self.ButtonG3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WP)
        self.ButtonG4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WP)
        self.ButtonG5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WP)
        self.ButtonG6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WP)
        self.ButtonG7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WP)
        self.ButtonG8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WP)
        self.ButtonG1.grid(row=6, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonG2.grid(row=6, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonG3.grid(row=6, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonG4.grid(row=6, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonG5.grid(row=6, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonG6.grid(row=6, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonG7.grid(row=6, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonG8.grid(row=6, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonH1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WR)
        self.ButtonH2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WN)
        self.ButtonH3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WB)
        self.ButtonH4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WQ)
        self.ButtonH5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WK)
        self.ButtonH6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WB)
        self.ButtonH7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WN)
        self.ButtonH8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_field_event, text = "", image = WR)
        self.ButtonH1.grid(row=7, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonH2.grid(row=7, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonH3.grid(row=7, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonH4.grid(row=7, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonH5.grid(row=7, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonH6.grid(row=7, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonH7.grid(row=7, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonH8.grid(row=7, column=7, sticky="sw", padx=0, pady=0)


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
    