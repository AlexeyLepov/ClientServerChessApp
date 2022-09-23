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


class Move:
    """A move in a chess game. Has a start and end position."""

    def __init__(self, start: Position, end: Position):
        """_summary_

        Args:
            start (Position): _description_
            end (Position): _description_
        """
        self.start = start
        self.end = end


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
        pos = [self.position.row, self.position.col]
        moves = []
        if self.name == "pawn":
            if self.color == Color.WHITE:
                if pos[0] != 7 and board_arr[pos[0]+1][pos[1]] == None:
                    moves.append(Position(pos[0] + 1, pos[1]))
                if pos[0] == 1 and board_arr[pos[0]+2][pos[1]] == None:
                    moves.append(Position(pos[0] + 2, pos[1]))
            if self.color == Color.BLACK:
                if pos[0] != 0 and board_arr[pos[0]-1][pos[1]] == None:
                    moves.append(Position(pos[0] - 1, pos[1]))
                if pos[0] == 6 and board_arr[pos[0]-2][pos[1]] == None:
                    moves.append(Position(pos[0] - 2, pos[1]))

        elif self.name == "rook" or self.name == "queen":
            for i in range(pos[0]+1, 8):
                if board_arr[i][pos[1]] == None:
                    moves.append(Position(i, pos[1]))
                else:
                    break
            for i in range(pos[0]-1, -1, -1):
                if board_arr[i][pos[1]] == None:
                    moves.append(Position(i, pos[1]))
                else:
                    break
            for i in range(pos[1]+1, 8):
                if board_arr[pos[0]][i] == None:
                    moves.append(Position(pos[0], i))
                else:
                    break
            for i in range(pos[1]-1, -1, -1):
                if board_arr[pos[0]][i] == None:
                    moves.append(Position(pos[0], i))
                else:
                    break

        elif self.name == "knight":
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) + abs(j) == 3:
                        if 0 <= pos[0] + i < 8 and 0 <= pos[1] + j < 8 and (board_arr[pos[0] + i][pos[1] + j] == None):
                            moves.append(Position(pos[0] + i, pos[1] + j))

        elif self.name == "bishop" or self.name == "queen":
            for i in range(1, 8):
                if pos[0] + i <= 7 and pos[1] + i <= 7:
                    if board_arr[pos[0] + i][pos[1] + i] == None:
                        moves.append(Position(pos[0] + i, pos[1] + i))
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                if pos[0] + i <= 7 and pos[1] - i >= 0:
                    if board_arr[pos[0] + i][pos[1] - i] == None:
                        moves.append(Position(pos[0] + i, pos[1] - i))
                    else:
                        break
                else:
                    break
            for i in range(1, 8):
                if pos[0] - i >= 0 and pos[1] + i <= 7:
                    if board_arr[pos[0] - i][pos[1] + i] == None:
                        moves.append(Position(pos[0] - i, pos[1] + i))
                    else:
                        break
                else:
                    break
            for i in range(1, 9):
                if pos[0] - i >= 0 and pos[1] - i >= 0:
                    if board_arr[pos[0] - i][pos[1] - i] == None:
                        moves.append(Position(pos[0] - i, pos[1] - i))
                    else:
                        break
                else:
                    break
        if self.name == "king":
            if pos[0] + 1 <= 7:
                moves.append(Position(pos[0] + 1, pos[1]))
            if pos[0] - 1 >= 0:
                moves.append(Position(pos[0] - 1, pos[1]))
            if pos[1] + 1 <= 7:
                moves.append(Position(pos[0], pos[1] + 1))
            if pos[1] - 1 >= 0:
                moves.append(Position(pos[0], pos[1] - 1))
            if pos[0] + 1 <= 7 and pos[1] + 1 <= 7:
                moves.append(Position(pos[0] + 1, pos[1] + 1))
            if pos[0] + 1 <= 7 and pos[1] - 1 >= 0:
                moves.append(Position(pos[0] + 1, pos[1] - 1))
            if pos[0] - 1 >= 0 and pos[1] + 1 <= 7:
                moves.append(Position(pos[0] - 1, pos[1] + 1))
            if pos[0] - 1 >= 0 and pos[1] - 1 >= 0:
                moves.append(Position(pos[0] - 1, pos[1] - 1))

        # for move in moves:
        #    move.col -= 1
        #    move.row -= 1

        return moves

    def correct_captures(self, board_arr, prev_board_arr):
        """Returns a list of all possible captures for a piece

        Args:
            board_arr (_type_): _description_
            prev_board_arr (_type_): _description_

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

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
            return -1
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
    def __init__(self, pieces=None):
        if pieces is None:
            self.pieces = Board.new_board()
        else:
            self.pieces = pieces
        self.arr = self.get_piece_arr()
        self.prev_arr = copy.deepcopy(self.arr)

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
                pieces.append(
                    Piece(piece[1], piece[0], Piece.get_value(piece[0]), pos))
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

    def move_piece(self, piece,  new_pos):
        """Moves a piece to a new position

        Args:
            piece (_type_): _description_
            new_pos (_type_): _description_

        Raises:
            NotImplementedError: _description_
        """
        Piece.correct_moves(piece, self.arr, self.prev_arr)
        piece.position = new_pos
        raise NotImplementedError

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
    board = Board.from_FEN("8/4B3/6N1/8/1B6/3n4/8/8 w KQkq ")
    arr = board.get_str_arr()
    for i in arr:
        print(*i)
    for piece in board.pieces:
        arr_ = copy.deepcopy(arr)
        moves = Piece.correct_moves(piece, board.arr, board.prev_arr)
        print(piece)
        for move in moves:
            arr_[7-move.row][move.col] = "XX"
        pos = piece.position
        arr_[7-pos.row][pos.col] = "OO"
        for i in arr_:
            print(*i)


if __name__ == "__main__":
    main()
