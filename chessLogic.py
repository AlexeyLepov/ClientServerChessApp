import chessEngine
import copy
import bpt
BLACK = chessEngine.Color.BLACK
WHITE = chessEngine.Color.WHITE

counter = 0
t_table = dict()
mmax = 0

fen_number = 0

class Node:
    def __init__(self, fen_notation: str, is_white: bool):
        global fen_number
        self.fen: str = str(fen_number)
        fen_number += 1
        self.alpha: float = 0
        self.beta: float = 0
        self.board: chessEngine.Board = None
        self.is_white: bool = is_white
        self.children: list = []
        if not self.is_white:
            self.evaluation: float = -10 ** 9
        else:
            self.evaluation: float = -10 ** 9
        self.dead_piece = None
        self.first_move = None
        self.moves = []
        self.stand_pat = 0

    def get_static_evaluation(self):
        """
        c1_1*Rook_advantage + c1_2*bishop_advantage + c1_3*knight_advantage + c1_4*queen_advantage +c1_5*pawn_advantage
        + c1_6 * king_advantage
        + c2_1*rook_Mobility_advantage + c2_2*bishop_mobility_advantage + c2_3*knight_mobility_advantage +
        + c2_4*queen_mobility_advantage + c5*own_center_pawns + c6*enemy's_center_pawns +
        + c7*own_king_pawn_shield + c8*enemy_king_pawn_shield + c9*own_iso_pawns + c10*enemy_iso_pawns +
        + c11*own_pass_pawns + c12*enemy_pass_pawns +c13*own_attackers + c14*enemy's_attackers +
        + c15*own_defenders + c16*enemy's_defenders
        """
        evaluation = 0
        rook_advantage = 0
        c1_1 = 500
        bishop_advantage = 0
        c1_2 = 320
        knight_advantage = 0
        c1_3 = 330
        queen_advantage = 0
        c1_4 = 900
        pawn_advantage = 0
        c1_5 = 100
        king_advantage = 0
        c1_6 = 20000
        bq = 0
        bk = 0
        bn = 0
        br = 0
        bb = 0
        bp = 0
        wq = 0
        wk = 0
        wn = 0
        wr = 0
        wb = 0
        wp = 0
        #board_array = self.board.get_str_arr()
        piece_arr = self.board.pieces
        bk = None
        wk = None
        for piece in piece_arr:
            if piece:
                if piece.name == "bishop" and piece.color == chessEngine.Color.BLACK:
                    bb += 1
                    bishop_advantage -= 1
                    evaluation -= bpt.BISHOPS_TABLE[piece.position.row][7-piece.position.col]
                elif piece.name == "knight" and piece.color == chessEngine.Color.BLACK:
                    bn += 1
                    knight_advantage -= 1
                    evaluation -= bpt.KNIGHTS_TABLE[piece.position.row][7-piece.position.col]
                elif piece.name == "pawn" and piece.color == chessEngine.Color.BLACK:
                    bp += 1
                    pawn_advantage -= 1
                    evaluation -= bpt.PAWN_TABLE[piece.position.row][7-piece.position.col]
                elif piece.name == "queen" and piece.color == chessEngine.Color.BLACK:
                    bq += 1
                    queen_advantage -= 1
                    evaluation -= bpt.QUEENS_TABLE[piece.position.row][7-piece.position.col]
                elif piece.name == "rook" and piece.color == chessEngine.Color.BLACK:
                    br += 1
                    rook_advantage -= 1
                    evaluation -= bpt.ROOKS_TABLE[7-piece.position.row][7-piece.position.col]
                elif piece.name == "bishop" and piece.color == chessEngine.Color.WHITE:
                    wb += 1
                    bishop_advantage += 1
                    evaluation += bpt.BISHOPS_TABLE[7-piece.position.row][piece.position.col]
                elif piece.name == "knight" and piece.color == chessEngine.Color.WHITE:
                    wn += 1
                    knight_advantage += 1
                    evaluation += bpt.KNIGHTS_TABLE[7-piece.position.row][piece.position.col]
                elif piece.name == "pawn" and piece.color == chessEngine.Color.WHITE:
                    wp += 1
                    pawn_advantage += 1
                    evaluation += bpt.PAWN_TABLE[7-piece.position.row][piece.position.col]
                elif piece.name == "queen" and piece.color == chessEngine.Color.WHITE:
                    wq += 1
                    queen_advantage += 1
                    evaluation += bpt.QUEENS_TABLE[7-piece.position.row][piece.position.col]
                elif piece.name == "rook" and piece.color == chessEngine.Color.WHITE:
                    wr += 1
                    rook_advantage += 1
                    evaluation += bpt.ROOKS_TABLE[7-piece.position.row][piece.position.col]
                elif piece.name == "king" and piece.color == chessEngine.Color.WHITE:
                    wk = piece
                elif piece.name == "king" and piece.color == chessEngine.Color.BLACK:
                    bk = piece

        if bk != None:
            king_advantage -= 1
            if bq+wq == 0 or (bq == 0 and wb + wn <= 1) or (wq == 0 and bb + bn <= 1) or (wb + wn <= 1 and bb + bn <= 1):
                evaluation -= bpt.KINGS_ENDGAME_TABLE[bk.position.row][7-bk.position.col]
                #print("endgame", wq, bq, bb, bn, wb, wn)
            else:
                evaluation -= bpt.KINGS_TABLE[bk.position.row][7-bk.position.col]
        if wk != None:
            king_advantage += 1
            if bq+wq == 0 or (bq == 0 and wb + wn <= 1) or (wq == 0 and bb + bn <= 1) or (wb + wn <= 1 and bb + bn <= 1):
                #print("endgame")
                evaluation += bpt.KINGS_ENDGAME_TABLE[7-wk.position.row][7-wk.position.col]
            else:
                evaluation += bpt.KINGS_TABLE[7-wk.position.row][7-wk.position.col]
        
        # c2_1 = 0.01
        # rook_mobility_advantage = 0
        # for piece in self.board.pieces:
        #     if piece.name == "rook":
        #         cm = piece.correct_moves(piece_arr, None)
        #         cc = piece.correct_captures(piece_arr, None)
        #         if piece.color == chessEngine.Color.WHITE:
        #             rook_mobility_advantage += len(cm) + len(cc)
        #         else:
        #             rook_mobility_advantage -= len(cm) + len(cc)

        # c2_2 = 0.01
        # bishop_mobility_advantage = 0
        # for piece in self.board.pieces:
        #     if piece.name == "bishop":
        #         cm = piece.correct_moves(piece_arr, None)
        #         cc = piece.correct_captures(piece_arr, None)
        #         if piece.color == chessEngine.Color.WHITE:
        #             rook_mobility_advantage += len(cm) + len(cc)
        #         else:
        #             rook_mobility_advantage -= len(cm) + len(cc)

        # c2_3 = 0.01
        # knight_mobility_advantage = 0
        # for piece in self.board.pieces:
        #     if piece.name == "knight":
        #         cm = piece.correct_moves(piece_arr, None)
        #         cc = piece.correct_captures(piece_arr, None)
        #         if piece.color == chessEngine.Color.WHITE:
        #             rook_mobility_advantage += len(cm) + len(cc)
        #         else:
        #             rook_mobility_advantage -= len(cm) + len(cc)

        # c2_4 = 0.005
        # queen_mobility_advantage = 0
        # for piece in self.board.pieces:
        #     if piece.name == "queen":
        #         cm = piece.correct_moves(piece_arr, None)
        #         cc = piece.correct_captures(piece_arr, None)
        #         if piece.color == chessEngine.Color.WHITE:
        #             rook_mobility_advantage += len(cm) + len(cc)
        #         else:
        #             rook_mobility_advantage -= len(cm) + len(cc)

        evaluation += c1_1 * rook_advantage
        evaluation += c1_2 * bishop_advantage
        evaluation += c1_3 * knight_advantage
        evaluation += c1_4 * queen_advantage
        evaluation += c1_5 * pawn_advantage
        evaluation += c1_6 * king_advantage
        # evaluation += c2_1 * rook_mobility_advantage
        # evaluation += c2_2 * bishop_mobility_advantage
        # evaluation += c2_3 * knight_mobility_advantage
        # evaluation += c2_4 * queen_mobility_advantage
        return evaluation

    def alpha_beta_evaluation(self, depth, alpha, beta, is_white_player, last_tile) -> float:
        global counter
        global t_table
        counter += 1
        if counter % 10000 == 0:
            print(counter)

        w = self.is_won()
        if w != 0:
            return is_white_player * self.get_static_evaluation()
        if depth <= 0:
            return self.quiscence_search(0,alpha,beta,is_white_player,is_white_player*self.get_static_evaluation())

        self.moves = self.board.all_moves()

        value: float = - 10 ** 9
        for move in self.moves:
            self.move_straight(self.board, move)
            n: Node = Node("self.board.get_FEN()", not self.is_white)
            n.board = self.board
            self.children.append(n)

            try:
                entry = t_table[n.fen]
                t_a, t_b, t_val, t_age = entry[0], entry[1], entry[2], entry[3]
            except KeyError:
                t_a, t_b, t_val, t_age = None, None, None, None
            if t_val is None:
                self.evaluation: float = - n.alpha_beta_evaluation(depth - 1, -beta, -alpha, -is_white_player, move[1])
            else:
                self.evaluation = -t_val
            value = max(value, self.evaluation)
            alpha = max(alpha, value)
            self.move_reverse(self.board, move)
            if alpha >= beta:
                self.evaluation = value
                # print("pruned a")
                break
        self.evaluation = value
        # if round(value,7) == 0:
        #     print(depth, self.is_white, self.moves,exch_tile)
        #     for n, i in enumerate(arr):
        #         print(8 - n, *i)
        #     print("  a  b  c  d  e  f  g  h")
        #
        #     raise Exception

        try:
            entry = t_table[self.fen]
            t_a,t_b,t_val,t_age = entry[0],entry[1],entry[2],entry[3]

            t_table[self.fen] = (max(t_a,alpha),min(t_b,beta),max(t_val,self.evaluation),counter)
        except KeyError:
            t_table[self.fen] = (alpha, beta, self.evaluation,counter)

        return value

    def move_straight(self, board: chessEngine.Board, move):
        if board.active_color == chessEngine.Color.WHITE:
            board.active_color = chessEngine.Color.BLACK
        else:
            board.active_color = chessEngine.Color.WHITE
        self.dead_piece = None
        for i in range(len(board.pieces)):
            if board.pieces[i].position.row == move[1][0] and board.pieces[i].position.col == move[1][1]:
                self.dead_piece = board.pieces[i]
                board.pieces = board.pieces[:i] + board.pieces[i + 1:]
                break
        for i in range(len(board.pieces)):
            if board.pieces[i].position.row == move[0][0] and board.pieces[i].position.col == move[0][1]:
                board.pieces[i].position.row = move[1][0]
                board.pieces[i].position.col = move[1][1]
                if board.pieces[i].first_move:
                    self.first_move = True
                    board.pieces[i].first_move = False
                else:
                    self.first_move = False
                break

    def move_reverse(self, board: chessEngine.Board, move):
        if board.active_color == chessEngine.Color.WHITE:
            board.active_color = chessEngine.Color.BLACK
        else:
            board.active_color = chessEngine.Color.WHITE
        for i in range(len(board.pieces)):
            if board.pieces[i].position.row == move[1][0] and board.pieces[i].position.col == move[1][1]:
                board.pieces[i].position.row = move[0][0]
                board.pieces[i].position.col = move[0][1]
                if self.first_move is not None:
                    board.pieces[i].first_move = self.first_move
                    self.first_move = None
                else:
                    raise Exception
                if self.dead_piece != None:
                    board.pieces.append(self.dead_piece)
                    self.dead_piece = None
                return
        raise Exception

    def quiscence_search(self, depth: int, alpha: float, beta: float, is_white_player, stand_pat: float):
        global counter,mmax
        if mmax>depth:
            print("max: ",mmax)
            mmax = depth
        counter += 1
        if counter % 10000 == 0:
            print(counter, "q")
        delta = 2
        self.board: chessEngine.Board
        moves = self.board.all_moves()
        self.moves = []
        board_arr = self.board.get_str_arr()

        if self.is_won() != 0 or depth <= -6:
            return is_white_player*self.get_static_evaluation()


        value = stand_pat
        for move in moves:
            is_capture = False
            f_pos = board_arr[move[0][0]][move[0][1]]
            s_pos = board_arr[move[1][0]][move[1][1]]
            if (f_pos[0] !=" ") and (s_pos[0] !=" ") and (f_pos[0] != s_pos[0]):
                # arr = board_arr
                # print(
                #     f"color: {self.board.active_color}, W: {self.board.score[chessEngine.Color.WHITE]}, B: {self.board.score[chessEngine.Color.BLACK]}")
                # for n_, i in enumerate(arr):
                #     print(8 - n_, *i)
                # print("  a  b  c  d  e  f  g  h")
                # print("("+f_pos+")"+" "+"("+s_pos+")")
                # print(move)
                is_capture = True
            self.move_straight(self.board,move)
            n = Node("self.board.get_FEN()", not self.is_white)
            n.board = self.board

            child_evaluation = is_white_player*n.get_static_evaluation()
            if is_capture and child_evaluation + delta >= stand_pat:
            # if (not n.board.check_check(BLACK if n.board.active_color == WHITE else WHITE)) and (n.board.check_check(BLACK if n.board.active_color == BLACK else WHITE) or (is_capture and child_evaluation + delta >= stand_pat)):
                # if n.board.check_check(BLACK if n.board.active_color == BLACK else WHITE):
                #
                #
                #     arr = board_arr
                #     print(
                #         f"color: {n.board.active_color}, W: {n.board.score[chessEngine.Color.WHITE]}, B: {n.board.score[chessEngine.Color.BLACK]}")
                #     for n_, i in enumerate(arr):
                #         print(8 - n_, *i)
                #     print("  a  b  c  d  e  f  g  h")


                self.children.append(n)
                self.moves.append(move)


                try:
                    entry = t_table[n.fen]
                    t_a,t_b,t_val,t_age = entry[0],entry[1],entry[2],entry[3]
                except KeyError:
                    t_a,t_b,t_val,t_age = None,None,None,None
                if t_val is None:
                    self.evaluation = -n.quiscence_search(depth-1,-beta,-alpha,-is_white_player,-child_evaluation)
                else:
                    self.evaluation = -t_val


                value = max(self.evaluation,value)
                alpha = max(alpha,value)

            self.move_reverse(self.board,move)
            if alpha >= beta:
                self.evaluation = value
                break
        self.evaluation = value

        try:
            entry = t_table[self.fen]
            t_a,t_b,t_val,t_age = entry[0],entry[1],entry[2],entry[3]

            t_table[self.fen] = (max(t_a,alpha),min(t_b,beta),max(t_val,self.evaluation),counter)
        except KeyError:
            t_table[self.fen] = (alpha, beta, self.evaluation,counter)


        #print(in_len,len(self.moves))
        # if len(self.moves) >=20:
        #     arr = board_arr
        #     print(
        #         f"color: {self.board.active_color}, W: {self.board.score[chessEngine.Color.WHITE]}, B: {self.board.score[chessEngine.Color.BLACK]}")
        #     for n_, i in enumerate(arr):
        #         print(8 - n_, *i)
        #     print("  a  b  c  d  e  f  g  h")
        #     for move in self.moves:
        #         print(move)
        #     raise Exception
        return value

    def get_static_exchange_evaluation(self, depth: int, alpha: float, beta: float, is_white_player, exch_tile):
        global counter
        counter += 1
        if counter % 10000 == 0:
            print(counter, "e")

        # arr = self.board.get_str_arr()
        # print(depth, self.is_white, self.moves,exch_tile)
        # for n, i in enumerate(arr):
        #     print(8 - n, *i)
        # print("  a  b  c  d  e  f  g  h")
        moves = self.board.all_captures()
        self.moves = []
        for move in moves:
            if move[1][0] == exch_tile[0] and move[1][1] == exch_tile[1]:
                self.moves.append(move)

        w = self.is_won()
        if w != 0 or len(self.moves) == 0:
            return is_white_player * self.get_static_evaluation()

        value: float = - 10 ** 9
        for move in self.moves:
            self.move_straight(self.board, move)
            n: Node = Node("self.board.get_FEN()", not self.is_white)
            n.board = self.board
            self.children.append(n)

            self.evaluation: float = - n.alpha_beta_evaluation(depth - 1, -beta, -alpha, -is_white_player, move[1])
            value = max(value, self.evaluation)
            alpha = max(alpha, value)
            self.move_reverse(self.board, move)
            if beta <= alpha:
                self.evaluation = value
                # print("pruned a")
                break
        self.evaluation = value
        # if round(value,7) == 0:
        #     print(depth, self.is_white, self.moves,exch_tile)
        #     for n, i in enumerate(arr):
        #         print(8 - n, *i)
        #     print("  a  b  c  d  e  f  g  h")
        #
        #     raise Exception
        return value

    def is_won(self):
        king_advantage = 0
        board_array = self.board.get_str_arr()

        for line in board_array:
            for tile in line:
                if tile == "BK":
                    king_advantage -= 1
                elif tile == "WK":
                    king_advantage += 1
        return king_advantage


class GameTree:
    def __init__(self, fen_notation, is_white):
        self.root: Node = Node(fen_notation, is_white)
        self.root.fen = fen_notation
        if is_white:
            self.evaluation: float = -10 ** 9
        else:
            self.evaluation: float = 10 ** 9
        self.is_white = is_white

    def alpha_beta_evaluation(self, depth):
        self.root.board = chessEngine.Board.from_FEN(self.root.fen)
        self.evaluation = self.root.alpha_beta_evaluation(depth, -10 ** 9, 10 ** 9, 1 if self.root.is_white else -1,
                                                          None)
        print('a')
        return self.evaluation

    def suggest_move(self, depth=None):
        global t_table
        t_table.clear()
        self.evaluation = 10 ** 9
        move = None
        child = None
        for i in range(len(self.root.children)):

            if self.root.children[i].evaluation < self.evaluation:
                self.evaluation = self.root.children[i].evaluation
                move = self.root.moves[i]
                child = self.root.children[i]

        # fout = open("bestMoveLogger.txt","w")
        # arr = self.root.board.get_str_arr()

        # for n, i in enumerate(arr):
        #     fout.write(str(8 - n) + " ")
        #     for j in i:
        #         fout.write(str(j) + " ")
        #     fout.write("\n")
        # print("\n" + "  a  b  c  d  e  f  g  h" + "\n" + "\n")

        # go = True
        # node = child
        # while go:
        #     go = False
        #     arr = chessEngine.Board.from_FEN(node.fen).get_str_arr()
        #     for n, i in enumerate(arr):
        #         fout.write(str(8 - n) + " ")
        #         for j in i:
        #             fout.write(str(j) + " ")
        #         fout.write("\n")
        #     fout.write("  a  b  c  d  e  f  g  h" + "\n" + "\n")
        #     for ch in node.children:
        #         print(node.evaluation, " ", ch.evaluation)
        #         if round(ch.evaluation,5) == round(-node.evaluation,5):
        #             go = True
        #             node = ch
        #             break



        #fout.close()



        return move, child


def main():
    board = chessEngine.Board.from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e3 0 1")
    # board = chessEngine.Board.from_FEN("rnbqkbnr/pppp1ppp/8/4p3/8/5N2/PPPPPPPP/RNBQKB1R w KQkq e3 0 1")
    # board = chessEngine.Board.from_FEN("rnbqkbnr/8/8/8/8/8/8/K7 w KQkq e3 0 1")
    # board = Board.from_FEN("rnbqkbnr/8/8/8/PPPPPPPP/8/8/K7 w KQkq e3 0 1")
    # board = Board.from_FEN("1nbqkbnr/8/8/8/1KPPPPPP/8/8/8 b KQkq e3 0 1")
    # board = Board.from_FEN("1n2kbnr/8/8/8/2PKPPbP/8/8/8 b KQkq e3 0 1")
    # board = Board.from_FEN("1n2kbnr/8/8/8/2PPPPbP/8/8/8 b KQkq e3 0 1")
    # board = chessEngine.Board.from_FEN("rnbqkbnr/8/8/8/8/8/8/K7 w KQkq e3 0 1")
    #board = chessEngine.Board.from_FEN("2bqkbn1/2pppp2/np2N3/r3P1p1/p2N2B1/5Q2/PPPPKPP1/RNB2r2 w KQkq - 0 1")
    arr = board.get_str_arr()
    print(arr)
    print(board.get_FEN())

    print(f"color: e" + (
        "White" if chessEngine.Color.WHITE else "Black") + f" W: {board.score[chessEngine.Color.WHITE]}, B: {board.score[chessEngine.Color.BLACK]}")
    for n, i in enumerate(arr):
        print(8 - n, *i)
    print("  a  b  c  d  e  f  g  h")
    while True:
        print(board.get_FEN())
        print(board.all_moves())
        if board.active_color == chessEngine.Color.BLACK:

            move = input("your move: ").split()
            if move[0] == "exit":
                break
            first_pos = chessEngine.Position(int(move[0][1]) - 1, ord(move[0][0]) - ord("a"))
            last_pos = chessEngine.Position(int(move[1][1]) - 1, ord(move[1][0]) - ord("a"))
            print(first_pos, last_pos)
            print(board.arr[first_pos.row][first_pos.col].position)
            print(board.move_piece(board.arr[first_pos.row][first_pos.col], last_pos))
        else:
            game_tree = GameTree(board.get_FEN(), True)
            game_tree.alpha_beta_evaluation(5)
            move, _ = game_tree.suggest_move()
            print("-----------------------------------------------------")

            for i in range(len(game_tree.root.children)):
                print(game_tree.root.moves[i], game_tree.root.children[i].evaluation)

            print("-----------------------------------------------------")

            print(move)
            print(board.move_piece(board.arr[move[0][0]][move[0][1]], chessEngine.Position(move[1][0], move[1][1])))
        arr = board.get_str_arr()
        print(
            f"color: {board.active_color}, W: {board.score[chessEngine.Color.WHITE]}, B: {board.score[chessEngine.Color.BLACK]}")
        for n, i in enumerate(arr):
            print(8 - n, *i)
        print("  a  b  c  d  e  f  g  h")


if __name__ == "__main__":
    main()