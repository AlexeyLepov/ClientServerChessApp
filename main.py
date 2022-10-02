####################################################################################################
#                                                                                                  #
#    ##########################################################################################    #
#    #                                                                                        #    #
#    #    Программный модуль инициализации приложения и построения графического интерфейса    #    #
#    #                                                                                        #    #
#    ##########################################################################################    #
#                                                                                                  #
####################################################################################################

import os
import sys
import cv2
import glob
import copy
import time
import numpy
import queue
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

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

###################################
#                                 #
#    Параметры шахматной доски    #
#                                 #
###################################
B_WIDTH = B_HEIGHT = 640            # width and height of the chess board
DIMENSION = 8                       # the dimensions of the chess board
SQ_SIZE = B_HEIGHT // DIMENSION     # the size of each of the sWPquares in the board
IMAGES = {}                         # images for the chess pieces
pieceDir = "Assets/PiecesSimple/"   # Стандартная папка для изображений фигур

# photo = tkinter.PhotoImage(file = r"Assets/PiecesModern/bB.png") # Creating a photoimage object to use image
# photoimage = photo.subsample(8, 8) # Resizing image to fit on button

def load_images():
    '''Load images for the chess pieces
    '''
    files = glob.glob(f"{pieceDir}*.png")
    for myFile in files:
        image = cv2.imread(myFile)
        IMAGES.append(image)

#####################################################
#                                                   #
#    Создание окна для работы пользователя - GUI    #
#                                                   #
#####################################################
class App(customtkinter.CTk):
    WIDTH = 910  # Задание ширины окна приложения
    HEIGHT = 690  # Задание высоты окна приложения

    def __init__(self):
        super().__init__()  # Определение родительского класса
        self.resizable(False, False)
        B_COLOR_WHITE = "#edede9"
        B_COLOR_BLACK = "#457b9d"

        ##########################################
        #                                        #
        #    Присвение значений по умолчанию     #
        #                                        #
        ##########################################
        self.title("Игра в Шахматы")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        ########################
        #                      #
        #    Создание окон     #
        #                      #
        ########################
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

        ############################
        #                          #
        #    Левое окно - МЕНЮ     #
        #                          #
        ############################
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

        ###############################################
        #                                             #
        #    Правое окно - информация о программе     #
        #                                             #
        ###############################################
        # Настройка макета сетки
        self.frame_right_info.rowconfigure(14, weight=10)
        self.frame_right_info.columnconfigure(0, weight=1)
        self.label_info = customtkinter.CTkLabel(master=self.frame_right_info, text="Информация о программе", text_font=("Roboto Medium", -16))
        self.label_info.grid(row=0, column=0, pady=10, padx=10)
        self.label_info_info = customtkinter.CTkLabel(master=self.frame_right_info, height=100, text_font=("Roboto Medium", -16), fg_color=("white", "gray38"), justify=tkinter.LEFT, text="\n \n")
        self.label_info_info.grid(row=1, column=0, sticky="we", padx=15, pady=15)
        self.label_info_authors = customtkinter.CTkLabel(master=self.frame_right_info, height=200, text_font=("Roboto Medium", -16), fg_color=("white", "gray38"), text="\n \n")
        self.label_info_authors.grid(row=2, column=0, sticky="we", padx=15, pady=15)
        
        ################################
        #                              #
        #    Окно для игр в шахматы    #
        #                              #
        ################################
        # Настройка макета сетки
        
        self.frame_right_play.rowconfigure(14, weight=10)
        self.frame_right_play.columnconfigure(0, weight=1)
        self.frame_board = customtkinter.CTkFrame(master=self.frame_right_play, fg_color=(B_COLOR_WHITE, B_COLOR_BLACK))
        self.frame_board.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)
        self.ButtonA1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonA2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonA3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonA4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonA5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonA6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonA7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonA8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonA1.grid(row=0, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonA2.grid(row=0, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonA3.grid(row=0, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonA4.grid(row=0, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonA5.grid(row=0, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonA6.grid(row=0, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonA7.grid(row=0, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonA8.grid(row=0, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonB1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonB2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonB3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonB4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonB5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonB6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonB7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonB8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonB1.grid(row=1, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonB2.grid(row=1, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonB3.grid(row=1, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonB4.grid(row=1, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonB5.grid(row=1, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonB6.grid(row=1, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonB7.grid(row=1, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonB8.grid(row=1, column=7, sticky="sw", padx=0, pady=0)        
        self.ButtonC1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonC2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonC3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonC4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonC5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonC6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonC7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonC8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonC1.grid(row=2, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonC2.grid(row=2, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonC3.grid(row=2, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonC4.grid(row=2, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonC5.grid(row=2, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonC6.grid(row=2, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonC7.grid(row=2, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonC8.grid(row=2, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonD1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonD2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonD3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonD4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonD5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonD6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonD7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonD8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonD1.grid(row=3, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonD2.grid(row=3, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonD3.grid(row=3, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonD4.grid(row=3, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonD5.grid(row=3, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonD6.grid(row=3, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonD7.grid(row=3, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonD8.grid(row=3, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonE1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonE2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonE3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonE4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonE5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonE6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonE7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonE8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonE1.grid(row=4, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonE2.grid(row=4, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonE3.grid(row=4, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonE4.grid(row=4, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonE5.grid(row=4, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonE6.grid(row=4, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonE7.grid(row=4, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonE8.grid(row=4, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonF1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonF2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonF3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonF4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonF5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonF6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonF7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonF8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonF1.grid(row=5, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonF2.grid(row=5, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonF3.grid(row=5, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonF4.grid(row=5, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonF5.grid(row=5, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonF6.grid(row=5, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonF7.grid(row=5, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonF8.grid(row=5, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonG1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonG2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonG3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonG4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonG5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonG6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonG7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonG8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonG1.grid(row=6, column=0, sticky="sw", padx=0, pady=0)
        self.ButtonG2.grid(row=6, column=1, sticky="sw", padx=0, pady=0)
        self.ButtonG3.grid(row=6, column=2, sticky="sw", padx=0, pady=0)
        self.ButtonG4.grid(row=6, column=3, sticky="sw", padx=0, pady=0)
        self.ButtonG5.grid(row=6, column=4, sticky="sw", padx=0, pady=0)
        self.ButtonG6.grid(row=6, column=5, sticky="sw", padx=0, pady=0)
        self.ButtonG7.grid(row=6, column=6, sticky="sw", padx=0, pady=0)
        self.ButtonG8.grid(row=6, column=7, sticky="sw", padx=0, pady=0)
        self.ButtonH1 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonH2 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonH3 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonH4 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonH5 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonH6 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonH7 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_BLACK, B_COLOR_BLACK), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
        self.ButtonH8 = customtkinter.CTkButton(master=self.frame_board, fg_color=(B_COLOR_WHITE, B_COLOR_WHITE), width=SQ_SIZE, height=SQ_SIZE, command=self.button_play_event, text = "")
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


##################################
#                                #
#    Инициализация программы     #
#                                #
##################################
if __name__ == "__main__":
    app = App()
    app.start()
    