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
import customtkinter
import tkinter.messagebox
from types import CellType
from PIL import Image

# importing local files
import config
import chessEngine
import chessLogic
import formLogin

global username
global password


#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#  Setting initial window parameters
#
#################################################################################################################################################################################
#################################################################################################################################################################################
class App(customtkinter.CTk):
    ######################################################################
    #                                                                    #
    #    Setting the parameters and the class for working with colors    #
    #                                                                    #
    ######################################################################
    WIDTH = 1160                            # Setting the Application Window Width
    HEIGHT = 680                            # Setting the Application Window height
    DIMENSION = 8                           # dimensions count of the chess board
    B_WIDTH = B_HEIGHT = 560                # width and height of the chess board
    SQ_SIZE = B_HEIGHT // DIMENSION         # the size of each of the sWPquares in the board
    PIECE_DIR = "Assets/PiecesModern/"      # Standard piece Image Folder
    # virtual board
    board = None
    # color class
    class Colors:
        Board_White = "#f9dcc4"                 # Standard color for white board margins
        Board_Black = "#023047"                 # Standart color for black chessboard fields (for black ones)
        Field_Correct_Move = "#a7c957"          # Color for fields that a piece can move to
        Field_Correct_Capture = "#f28482"       # The color of the fields in which the enemy piece stands
        Moving_Piece = "#87a937"                # The color of the selected piece
        Users_Current = chessEngine.Color.WHITE # Player Color
        Menu_Button = "#6a994e"
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
        self.title("")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.eval('tk::PlaceWindow . center')
        # self.withdraw() # hide window
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)
        # Reading the image of pieces and "fitting" to the size of one cell of the virtual chessboard
        self.BB = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bB.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bB.png')), size=(54,54))
        self.BP = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bp.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bp.png')), size=(54,54))
        self.BN = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bN.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bN.png')), size=(54,54))
        self.BR = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bR.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bR.png')), size=(54,54))
        self.BQ = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bQ.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bQ.png')), size=(54,54))
        self.BK = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'bK.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'bK.png')), size=(54,54))
        self.WB = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wB.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wB.png')), size=(54,54))
        self.WP = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wp.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wp.png')), size=(54,54))
        self.WN = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wN.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wN.png')), size=(54,54))
        self.WR = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wR.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wR.png')), size=(54,54))
        self.WQ = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wQ.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wQ.png')), size=(54,54))
        self.WK = customtkinter.CTkImage(light_image=Image.open(os.path.join(App.PIECE_DIR, 'wK.png')), dark_image=Image.open(os.path.join(App.PIECE_DIR, 'wK.png')), size=(54,54))
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
#   Creation of panels (frames)
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
        self.button_playClient = customtkinter.CTkButton(master=self.frame_menu, text="Играть", fg_color=("gray75", "#64897e"), width=180, height=60, command=self.button_playClient_event)
        self.button_profile = customtkinter.CTkButton(master=self.frame_menu, text="Профиль", fg_color=("gray75", "#64897e"), width=180, height=60, command=self.button_profile_event)
        self.button_info = customtkinter.CTkButton(master=self.frame_menu, text="О программе", fg_color=("gray75", "#64897e"), width=180, height=60, command=self.button_info_event)
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
        self.frame_chat = customtkinter.CTkFrame(master=self.frame_playClient, width=365, height=App.B_HEIGHT, fg_color=("#C0C2C5","#343638"))
        self.frame_top_timeClient = customtkinter.CTkLabel(master=self.frame_chessClient, height=40, text="", fg_color=("#C0C2C5","#343638"))
        self.frame_board = customtkinter.CTkFrame(master=self.frame_chessClient, fg_color=(App.Colors.Board_White, App.Colors.Board_Black), width=App.B_WIDTH, height=App.B_HEIGHT)
        self.frame_bottom_timeClient = customtkinter.CTkLabel(master=self.frame_chessClient, height=40, text="",  fg_color=("#C0C2C5","#343638"))
        # Packing elements
        self.frame_chessClient.grid(
            row=0, column=0, padx=0, pady=0, sticky="nswe")
        self.frame_chat.grid(
            row=0, column=1, padx=5, pady=5, sticky="nswe")
        self.frame_top_timeClient.grid(
            row=0, column=0, padx=5, pady=5, sticky="nswe")
        self.frame_board.grid(
            row=1, column=0, padx=5, pady=0, sticky="nswe")
        self.frame_bottom_timeClient.grid(
            row=2, column=0, padx=5, pady=5, sticky="nswe")
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
        self.frame_profileUser = customtkinter.CTkLabel(master=self.frame_profile, height=40, text="Hello, ",  fg_color=("#C0C2C5","#343638"))
        # Packing elements
        self.frame_profileUser.grid(
            row=2, column=0, sticky="nswe", padx=5, pady=5)


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
            self.ButtonField = [[0 for _ in range(8)] for _ in range(8)]
            for i, j in itertools.product(range(8), range(8)):
                self.ButtonField[i][j] = customtkinter.CTkButton(master=self.frame_board, width=App.SQ_SIZE, height=App.SQ_SIZE, text="", hover_color=(App.Colors.Field_Correct_Move,App.Colors.Field_Correct_Move))
                self.ButtonField[i][j].grid(row=7-i, column=j, sticky="sw", padx=0, pady=0)
            self.RecolorBoard()
            self.board = chessEngine.Board()
            self.UpdateBoard()
            for i, j in itertools.product(range(8), range(8)):
                self.ButtonField[i][j].configure(command = lambda row=i,col=j: self.ButtonField_event(row,col))
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
    def ButtonField_event(self,row,col):
        ''' Some of the functions from chessEngine.py used:
        correct_moves - list of moves that a piece can operate on - except for those in which it is possible to capture the enemy
        correct_captures - list of all possible captures of enemy pieces
        move_piece - piece moving
        '''
        position = self.SelectedField()
        # print(self.board) # debbug
        # if no button is selected
        if position is None: 
            if self.board.get_piece_arr()[row][col] is None:
                return
            if self.board.get_piece_arr()[row][col].color != self.board.active_color:
                return
            piece = self.board.get_piece_arr()[row][col]
            self.ButtonField[row][col].configure(fg_color=(App.Colors.Moving_Piece, App.Colors.Moving_Piece))
            App.SelectedButtonField.selected = True
            App.SelectedButtonField.row = row
            App.SelectedButtonField.col = col
            correct_moves = piece.correct_moves(self.board.arr, self.board.prev_arr)
            correct_captures = piece.correct_captures(self.board.arr, self.board.prev_arr)
            for move in correct_moves:
                self.ButtonField[move.row][move.col].configure(fg_color=(App.Colors.Field_Correct_Move, App.Colors.Field_Correct_Move))
            for capture in correct_captures:
                self.ButtonField[capture.row][capture.col].configure(fg_color=(App.Colors.Field_Correct_Capture, App.Colors.Field_Correct_Capture))
        # if there is a selected one
        else:
            self._extracted_from_ButtonField_event_21(position, row, col) 
    def _extracted_from_ButtonField_event_21(self, position, row, col):
        self.ButtonField[position.row][position.col].configure(image = None)
        App.SelectedButtonField.selected = False
        App.SelectedButtonField.row = row
        App.SelectedButtonField.col = col
        piece = self.board.get_piece_arr()[position.row][position.col]
        if self.board.move_piece(piece, chessEngine.Position(row, col)):
            game_tree = chessLogic.GameTree(self.board.get_FEN(),False)
            game_tree.alpha_beta_evaluation(5)
            move,_ = game_tree.suggest_move()
            self.board.move_piece(self.board.get_piece_arr()[move[0][0]][move[0][1]],chessEngine.Position(move[1][0],move[1][1]))
            self.ButtonField[move[0][0]][move[0][1]].configure(image = None)
        self.UpdateBoard()
        str = self.board.get_str_arr()
    #######################################################
    #                                                     #
    #    Function to paint the board in default colors    #
    #                                                     #
    #######################################################
    def RecolorBoard(self):
        for i, j in itertools.product(range(8), range(8)):
            if ((i + j) % 2) == 0:
                self.ButtonField[i][j].configure(fg_color=(App.Colors.Board_Black, App.Colors.Board_Black))
            else:
                self.ButtonField[i][j].configure(fg_color=(App.Colors.Board_White, App.Colors.Board_White))
    def ClearBoard(self):
        for i, j in itertools.product(range(8), range(8)):
            self.ButtonField[i][j].configure(image = None)
    def UpdateBoard(self):
        self.RecolorBoard()
        self.ButtonField[0][0].configure(image = None)
        self.ButtonField[0][7].configure(image = None)
        self.ButtonField[7][0].configure(image = None)
        self.ButtonField[7][7].configure(image = None)
        for piece in self.board.pieces:
            position = piece.position
            self.ButtonField[position.row][position.col].configure(image = self.pieceImage(piece.name, piece.color))
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