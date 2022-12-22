import customtkinter
import itertools
import sys

import main
import chessEngine

#################################################################################################################################################################################
#################################################################################################################################################################################
# 
#  Setting "Play" window parameters
#
#################################################################################################################################################################################
#################################################################################################################################################################################
class FormPlay(customtkinter.CTk):    # color class
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
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark") # change theme to DARK
        customtkinter.set_default_color_theme("green") # theme change (COLOR PALETTE)
        ##############################
        #                            #
        #    Building a main form    #
        #                            #
        ##############################
        PLAY_WIDTH = PLAY_HEIGHT = 670
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
        self.geometry(f"{PLAY_WIDTH}x{PLAY_HEIGHT}")
        self.resizable(False, False)
        self.title("Вход в систему")
        self.protocol("WM_DELETE_WINDOW", self.on_closingLogForm)
        self.eval('tk::PlaceWindow . center')
        # self.withdraw() # hide window
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closingLogForm)
            self.bind("<Command-w>", self.on_closingLogForm)
            self.createcommand('tk::mac::Quit', self.on_closingLogForm)
        ##############################
        #                            #
        #    Building frame items    #
        #                            #
        ##############################

        frame_playClient = customtkinter.CTkFrame(master=self)
        frame_playClient.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        frame_playClient.rowconfigure(14, weight=10)
        frame_playClient.columnconfigure(0, weight=1)
        # Adding elements to the form
        frame_chessClient = customtkinter.CTkFrame(master=frame_playClient, width=B_WIDTH, height=B_HEIGHT, fg_color=("#D1D5D8","#2A2D2E"))
        frame_board = customtkinter.CTkFrame(master=frame_chessClient, fg_color=(FormPlay.Colors.Signs, FormPlay.Colors.Signs), width=B_WIDTH, height=B_HEIGHT)
        # Packing elements
        frame_chessClient.grid(
            row=0, column=0, padx=0, pady=0, sticky="nswe")
        frame_board.grid(
            row=1, column=0, padx=5, pady=0, sticky="nswe")

        alphabeticalNumeration = ['a','b','c','d','e','f','g','h']
        ButtonField = [[0 for _ in range(8)] for _ in range(8)]
        ButtonFieldSign = [[0 for _ in range(2)] for _ in range(8)]
        for i, j in itertools.product(range(8), range(8)):
            ButtonField[i][j] = customtkinter.CTkButton(master=frame_board, width=SQ_SIZE, height=SQ_SIZE, text="", hover_color=(FormPlay.Colors.Field_Correct_Move,FormPlay.Colors.Field_Correct_Move))
            ButtonField[i][j].grid(row=7-i, column=j+1, sticky="sw", padx=0, pady=0)
        for i, j in itertools.product(range(8), range(2)):
            if j==0:
                ButtonFieldSign[i][j] = customtkinter.CTkButton(master=frame_board, width=SQ_SIZE, height=SQ_SIZE/4, text=f"{alphabeticalNumeration[i]}", hover_color=(FormPlay.Colors.Signs,FormPlay.Colors.Signs), fg_color=(FormPlay.Colors.Signs,FormPlay.Colors.Signs))
                ButtonFieldSign[i][j].grid(row=8-j, column=i+1, sticky="sw", padx=0, pady=0)
            else:
                ButtonFieldSign[i][j] = customtkinter.CTkButton(master=frame_board, width=SQ_SIZE/4, height=SQ_SIZE, text=f"{i+1}", hover_color=(FormPlay.Colors.Signs,FormPlay.Colors.Signs), fg_color=(FormPlay.Colors.Signs,FormPlay.Colors.Signs))
                ButtonFieldSign[i][j].grid(row=7-i, column=0, sticky="sw", padx=0, pady=0)
        self.RecolorBoard()
        board = chessEngine.Board()
        self.UpdateBoard()
        for i, j in itertools.product(range(8), range(8)):
            ButtonField[i][j].configure(command = lambda row=i,col=j: ButtonField_event(row,col))

    ########################
    #                      #
    #    operate window    #
    #                      #
    ########################
    def on_closingLogForm(self, event=0):
        # app.deiconify()
        self.destroy()
    def startPlayForm(self):
        self.mainloop()

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
                if self.ButtonField[i][j].cget("fg_color") != (FormPlay.Colors.Board_Black, FormPlay.Colors.Board_Black):
                    self.ButtonField[i][j].configure(fg_color=(FormPlay.Colors.Board_Black, FormPlay.Colors.Board_Black))
            else:
                if self.ButtonField[i][j].cget("fg_color") != (FormPlay.Colors.Board_Black, FormPlay.Colors.Board_Black):
                    self.ButtonField[i][j].configure(fg_color=(FormPlay.Colors.Board_White, FormPlay.Colors.Board_White))

    def UpdateBoard(self):
        self.RecolorBoard()
        arr = self.board.get_piece_arr()
        for i in range(8):
            for j in range(8):
                piece = arr[i][j]
                if piece == None:
                    image = None
                else:
                    image = App.pieceImage(self.piece.name, self.piece.color)
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
        return None

playForm = FormPlay()
playForm.startPlayForm()