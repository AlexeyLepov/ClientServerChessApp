#########################################################
#                                                       #
#    ###############################################    #
#    #                                             #    #
#    #    Классы для работы с шахматной логикой    #    #
#    #                                             #    #
#    ###############################################    #
#                                                       #
#########################################################

from enum import Enum
import copy




class Color(Enum):
    WHITE = 1
    BLACK = 2



class Position:
    """A position on a chess board. Has a row and column."""

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return f"({self.row}, {self.col})"

    def __repr__(self):
        return f"Position({self.row}, {self.col})"
    
    def __eq__(self, other): 
        return self.row == other.row and self.col == other.col


# class Move:
#     """A move in a chess game. Has a start and end position."""

#     def __init__(self, start: Position, end: Position):
#         """_summary_

#         Args:
#             start (Position): _description_
#             end (Position): _description_
#         """
#         self.start = start
#         self.end = end



class Piece:
    """
    Class for chess pieces

    color: Color.WHITE or Color.BLACK
    name: {pawn, rook, knight, bishop, queen, king}
    value: value of piece in pawns
    """


    def __init__(self, color: Color = Color.WHITE, name: str = "pawn", value: int = None, position: Position = None, first_move: bool = True):
        """_summary_

        Args:
            color (Color, optional): _description_. Defaults to Color.WHITE.
            name (str, optional): _description_. Defaults to "pawn".
            value (int, optional): _description_. Defaults to None.
            position (Position, optional): _description_. Defaults to None.
            first_move (bool, optional): _description_. Defaults to True.
        """
        self.color = color
        self.name = name
        self.value = value
        self.position = position
        self.first_move = first_move

    def __str__(self):
        return ("White" if self.color == Color.WHITE else "Black") + " *" + self.name + "* "

    def __repr__(self):
        return f"Piece({self.color}, {self.name}, {self.value})"

    def correct_moves(self, board_arr, prev_board_arr):
        """Returns a list of all possible moves for a piece

        Args:
            board_arr (_type_): _description_
            prev_board_arr (_type_): _description_

        Returns:
            _type_: _description_
        """
        pos = self.position
        moves = []
        if self.name == "pawn":
            if self.color == Color.WHITE:
                if self.position.row != 7 and board_arr[self.position.row+1][self.position.col] == None:
                    moves.append(
                        Position(self.position.row + 1, self.position.col))
                if self.position.row == 1 and board_arr[self.position.row+2][self.position.col] == None:
                    moves.append(
                        Position(self.position.row + 2, self.position.col))
            if self.color == Color.BLACK:
                if self.position.row != 0 and board_arr[self.position.row-1][self.position.col] == None:
                    moves.append(
                        Position(self.position.row - 1, self.position.col))
                if self.position.row == 6 and board_arr[self.position.row-2][self.position.col] == None:
                    moves.append(
                        Position(self.position.row - 2, self.position.col))

        if self.name == "rook" or self.name == "queen":
            for i in range(self.position.row+1, 8):
                if board_arr[i][self.position.col] == None:
                    moves.append(Position(i, self.position.col))
                else:
                    break
            for i in range(self.position.row-1, -1, -1):
                if board_arr[i][self.position.col] == None:
                    moves.append(Position(i, self.position.col))
                else:
                    break
            for i in range(self.position.col+1, 8):
                if board_arr[self.position.row][i] == None:
                    moves.append(Position(self.position.row, i))
                else:
                    break
            for i in range(self.position.col-1, -1, -1):
                if board_arr[self.position.row][i] == None:
                    moves.append(Position(self.position.row, i))
                else:
                    break

        if self.name == "knight":
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) == 3:
                        if 0 <= self.position.row + i < 8 and 0 <= self.position.col + j < 8 and (board_arr[self.position.row + i][self.position.col + j] == None):
                            moves.append(
                                Position(self.position.row + i, self.position.col + j))

        if self.name == "bishop" or self.name == "queen":
            for i in range(1, 9):
                print(i)
                if self.position.row + i <= 7 and self.position.col + i <= 7:
                    if board_arr[self.position.row + i][self.position.col + i] == None:
                        moves.append(
                            Position(self.position.row + i, self.position.col + i))
                    else:
                        break
                else:
                    break
            for i in range(1, 9):
                print(i)
                if self.position.row + i <= 7 and self.position.col - i >= 0:
                    if board_arr[self.position.row + i][self.position.col - i] == None:
                        moves.append(
                            Position(self.position.row + i, self.position.col - i))
                    else:
                        break
                else:
                    break
            for i in range(1, 9):
                print(i)
                if self.position.row - i >= 0 and self.position.col + i <= 7:
                    if board_arr[self.position.row - i][self.position.col + i] == None:
                        moves.append(
                            Position(self.position.row - i, self.position.col + i))
                    else:
                        break
                else:
                    break
            for i in range(1, 9):
                print(i)
                if self.position.row - i >= 0 and self.position.col - i >= 0:
                    if board_arr[self.position.row - i][self.position.col - i] == None:
                        moves.append(
                            Position(self.position.row - i, self.position.col - i))
                    else:
                        break
                else:
                    break            
        if self.name == "king":
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= self.position.row + i < 8 and 0 <= self.position.col + j < 8 and (board_arr[self.position.row + i][self.position.col + j] == None or board_arr[self.position.row + i][self.position.col + j].color != self.color):
                        moves.append(
                            Position(self.position.row + i, self.position.col + j))

        return moves

        # for move in moves:
        #    move.col -= 1
        #    move.row -= 1

        return moves

    def correct_captures(self, board_arr, prev_board_arr):
        captures = []
        
        if self.name == "pawn": # pawn captures
            if self.color == Color.WHITE:
                if self.position.row != 7 and self.position.col != 0 and board_arr[self.position.row+1][self.position.col-1] != None and board_arr[self.position.row+1][self.position.col-1].color == Color.BLACK:
                    captures.append(
                        Position(self.position.row + 1, self.position.col - 1))
                if self.position.row != 7 and self.position.col != 7 and board_arr[self.position.row+1][self.position.col+1] != None and board_arr[self.position.row+1][self.position.col+1].color == Color.BLACK:
                    captures.append(
                        Position(self.position.row + 1, self.position.col + 1))
            if self.color == Color.BLACK:
                if self.position.row != 0 and self.position.col != 0 and board_arr[self.position.row-1][self.position.col-1] != None and board_arr[self.position.row-1][self.position.col-1].color == Color.WHITE:
                    captures.append(
                        Position(self.position.row - 1, self.position.col - 1))
                if self.position.row != 0 and self.position.col != 7 and board_arr[self.position.row-1][self.position.col+1] != None and board_arr[self.position.row-1][self.position.col+1].color == Color.WHITE:
                    captures.append(
                        Position(self.position.row - 1, self.position.col + 1))
        if self.name == "knight":
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) == 3:
                        if 0 <= self.position.row + i < 8 and 0 <= self.position.col + j < 8 and (board_arr[self.position.row + i][self.position.col + j] is not None):
                            captures.append(
                                Position(self.position.row + i, self.position.col + j))
        if self.name == "rook" or self.name == "queen":
            for i in range(self.position.row+1, 8):
                if board_arr[i][self.position.col] is not None:
                    captures.append(Position(i, self.position.col))
                    break
            for i in range(self.position.row-1, -1, -1):
                if board_arr[i][self.position.col] is not None:
                    captures.append(Position(i, self.position.col))
                    break
            for i in range(self.position.col+1, 8):
                if board_arr[self.position.row][i] is not None:
                    captures.append(Position(self.position.row, i))
                    break
            for i in range(self.position.col-1, -1, -1):
                if board_arr[self.position.row][i] is not None:
                    captures.append(Position(self.position.row, i))
                    break
        if self.name == "bishop" or self.name == "queen":
            for i in range(1, 9):
                if self.position.row + i <= 7 and self.position.col + i <= 7:
                    if board_arr[self.position.row + i][self.position.col + i] is not None:
                        captures.append(Position(self.position.row + i, self.position.col + i))
                        break
                else:
                    break
            for i in range(1, 9):
                if self.position.row + i <= 7 and self.position.col - i >= 0:
                    if board_arr[self.position.row + i][self.position.col - i] is not None:
                        captures.append(Position(self.position.row + i, self.position.col - i))
                        break
                else:
                    break
            for i in range(1, 9):
                if self.position.row - i >= 0 and self.position.col + i <= 7:
                    if board_arr[self.position.row - i][self.position.col + i] is not None:
                        captures.append(Position(self.position.row - i, self.position.col + i))
                        break
                else:
                    break
            for i in range(1, 9):
                if self.position.row - i >= 0 and self.position.col - i >= 0:
                    if board_arr[self.position.row - i][self.position.col - i] is not None:
                        captures.append(Position(self.position.row - i, self.position.col - i))
                        break
                else:
                    break
        for move in captures:
            if board_arr[move.row][move.col].color == self.color:
                captures.remove(move)
        return captures


    @classmethod
    def get_value(cls, name):
        """
        Returns the value of a piece in pawns
        """
        if name == "pawn":
            return 1
        elif name == "knight" or name == "bishop":
            return 3
        elif name == "rook":
            return 5
        elif name == "queen":
            return 9
        elif name == "king":
            return 0
        else:
            raise ValueError("Invalid piece name")

    @classmethod
    def get_start_position(cls, name, color):
        """Retuns the starting position of a piece

        Args:
            name (_type_): _description_
            color (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if color == Color.WHITE:
            if name == "pawn":
                return [Position(1, i) for i in range(8)]
            elif name == "rook":
                return [Position(0, 0), Position(0, 7)]
            elif name == "knight":
                return [Position(0, 1), Position(0, 6)]
            elif name == "bishop":
                return [Position(0, 2), Position(0, 5)]
            elif name == "queen":
                return [Position(0, 3)]
            elif name == "king":
                return [Position(0, 4)]
        elif color == Color.BLACK:
            if name == "pawn":
                return [Position(6, i) for i in range(8)]
            elif name == "rook":
                return [Position(7, 0), Position(7, 7)]
            elif name == "knight":
                return [Position(7, 1), Position(7, 6)]
            elif name == "bishop":
                return [Position(7, 2), Position(7, 5)]
            elif name == "queen":
                return [Position(7, 3)]
            elif name == "king":
                return [Position(7, 4)]
        else:
            raise ValueError("Invalid color")


class Board:
    def __init__(self, pieces=None, active_color=Color.WHITE):
        if pieces is None:
            self.pieces = Board.new_board()
        else:
            self.pieces = pieces
        self.arr = self.get_piece_arr()
        self.prev_arr = copy.deepcopy(self.arr)
        self.score = {Color.BLACK: 0, Color.WHITE: 0}
        self.active_color = active_color
    @classmethod
    def new_board(cls):
        """Creates a new board with all pieces in their starting positions

        Returns:
            _type_: _description_
        """
        pieces_list = [[("rook", color), ("bishop", color),
                       ("pawn", color), ("king", color),
                       ("queen", color), ("knight", color)
                         ]for color in (Color.WHITE, Color.BLACK)]
        pieces_list = pieces_list[0] + pieces_list[1]
        pieces = []
        for piece in pieces_list:
            for pos in Piece.get_start_position(piece[0], piece[1]):
                pieces.append(Piece(piece[1], piece[0], Piece.get_value(piece[0]), pos))
        print(len(pieces))

        return pieces

    @classmethod
    def from_FEN(cls, str):
        """Generates a board from FEN notation
        Args:
            str (_type_): _description_

        Returns:
            _type_: _description_
        """
        FEN_pieces = {"r": ("rook", Color.BLACK), "n": ("knight", Color.BLACK), "b": ("bishop", Color.BLACK), "q": ("queen", Color.BLACK), "k": ("king", Color.BLACK), "p": ("pawn", Color.BLACK), "R": (
            
            "rook", Color.WHITE), "N": ("knight", Color.WHITE), "B": ("bishop", Color.WHITE), "Q": ("queen", Color.WHITE), "K": ("king", Color.WHITE), "P": ("pawn", Color.WHITE)}
        arr = list(map(list, str.split("/")))
        i = 0
        pieces = []
        while i in range(len(arr)):
            j = 0
            while j in range(len(arr[i])):
                if arr[i][j].isdigit():
                    n = arr[i].pop(j)
                    for _ in range(int(n)):
                        arr[i].insert(j, "")
                j += 1
            i += 1
        for i in range(8):
            for j in range(8):
                if arr[i][j] != "":
                    pieces.append(Piece(FEN_pieces[arr[i][j]][1], FEN_pieces[arr[i][j]][0], Piece.get_value(
                        FEN_pieces[arr[i][j]][0]), Position(7-i, j)))

        return cls(pieces)

    def check_check(self, color):
        """checks if a color is in check

        Args:
            color (COLOR): color of the player to check

        Returns:
            bool: True if the player is in check, False otherwise
        """
        for piece in self.pieces:
            if piece.color == color and piece.name == "king":
                king_pos = piece.position
                break
        
        for piece in self.pieces:
            if piece.color != color:
                if king_pos in piece.get_captures(self.arr):
                    return True
        return False
    
    def move_piece(self, piece,  new_pos):
        corr_moves = Piece.correct_moves(piece, self.arr, self.prev_arr)
        corr_captures = Piece.correct_captures(piece, self.arr, self.prev_arr)
        print(corr_moves)
        if piece.color != self.active_color:
            return False
        if new_pos in corr_moves:
            piece.position = new_pos
            self.arr = self.get_piece_arr()
            self.active_color = Color.BLACK if self.active_color == Color.WHITE else Color.WHITE
            return True
        
        elif new_pos in corr_captures:
            eaten_piece = self.arr[new_pos.row][new_pos.col]
            self.arr[new_pos.row][new_pos.col] = None
            self.pieces.remove(eaten_piece)
            self.score[piece.color] += eaten_piece.value
            
            piece.position = new_pos
            self.arr = self.get_piece_arr()
            self.active_color = Color.BLACK if self.active_color == Color.WHITE else Color.WHITE
            return True
        
        return False

    def get_piece_arr(self):
        """
        Returns a 2d array of the board
        """
        arr = [[None for _ in range(8)] for _ in range(8)]
        for piece in self.pieces:
            arr[piece.position.row][piece.position.col] = piece
        return arr

    def get_str_arr(self):
        """
        Returns a text 2d array of the board
        """
        arr = [["  " if (i+j) % 2 == 1 else "  " for i in range(8)]
               for j in range(8)]
        for piece in self.pieces:
            arr[7-piece.position.row][piece.position.col] = {Color.BLACK: "B", Color.WHITE: "W"}[piece.color] + {
                
                "pawn": "P", "rook": "R", "knight": "N", "bishop": "B", "queen": "Q", "king": "K"}[piece.name]
        return arr

    def __str__(self):
        arr = self.get_str_arr()
        return "\n".join([" ".join(i) for i in arr][::-1])


def main():
    board = Board()
    arr = board.get_str_arr()
    print(f"color: e" + ("White" if Color.WHITE else "Black") + f" W: {board.score[Color.WHITE]}, B: {board.score[Color.BLACK]}")
    for n, i in enumerate(arr):
        print(8-n, *i)
    print("  a  b  c  d  e  f  g  h")
    while True:
        move = input("your move: ").split()
        if move[0] == "exit":
            break
        first_pos = Position(int(move[0][1])-1, ord(move[0][0])-ord("a"))
        last_pos = Position(int(move[1][1])-1, ord(move[1][0])-ord("a"))
        print(first_pos, last_pos)
        print(board.arr[first_pos.row][first_pos.col].position)
        print(board.move_piece(board.arr[first_pos.row][first_pos.col], last_pos))
        arr = board.get_str_arr()
        print(f"color: {board.active_color}, W: {board.score[Color.WHITE]}, B: {board.score[Color.BLACK]}")
        for n, i in enumerate(arr):
            print(8-n, *i)
        print("  a  b  c  d  e  f  g  h")

if __name__ == "__main__":
    main()

