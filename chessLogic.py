import chessEngine
import copy

counter = 0


class Node:
    def __init__(self, fen_notation: str, is_white: bool):
        self.fen: str = fen_notation
        self.alpha: float = 0
        self.beta: float = 0
        self.board: chessEngine.Board = None
        self.is_white: bool = is_white
        self.children: list = []
        self.evaluation: float = 0
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
        c1_1 = 5
        bishop_advantage = 0
        c1_2 = 3
        knight_advantage = 0
        c1_3 = 3
        queen_advantage = 0
        c1_4 = 9
        pawn_advantage = 0
        c1_5 = 1
        king_advantage = 0
        c1_6 = 300
        board_array = self.board.get_str_arr()
        piece_arr = self.board.get_piece_arr()
        for line in board_array:
            for tile in line:
                if tile == "BB":
                    bishop_advantage -= 1
                elif tile == "BK":
                    king_advantage -= 1
                elif tile == "BN":
                    knight_advantage -= 1
                elif tile == "BP":
                    pawn_advantage -= 1
                elif tile == "BQ":
                    queen_advantage -= 1
                elif tile == "BR":
                    rook_advantage -= 1
                elif tile == "WB":
                    bishop_advantage += 1
                elif tile == "WK":
                    king_advantage += 1
                elif tile == "WN":
                    knight_advantage += 1
                elif tile == "WP":
                    pawn_advantage += 1
                elif tile == "WQ":
                    queen_advantage += 1
                elif tile == "WR":
                    rook_advantage += 1
        c2_1 = 0.01
        rook_mobility_advantage = 0
        for piece in self.board.pieces:
            if piece.name == "rook":
                if piece.color == chessEngine.Color.WHITE:
                    for _ in piece.correct_moves(piece_arr,None):
                        rook_mobility_advantage+=1
                    for _ in piece.correct_captures(piece_arr,None):
                        rook_mobility_advantage+=1
                else:
                    for _ in piece.correct_moves(piece_arr, None):
                        rook_mobility_advantage -= 1
                    for _ in piece.correct_captures(piece_arr,None):
                        rook_mobility_advantage-=1

        c2_2 = 0.02
        bishop_mobility_advantage = 0
        for piece in self.board.pieces:
            if piece.name == "bishop":
                if piece.color == chessEngine.Color.WHITE:
                    for _ in piece.correct_moves(piece_arr, None):
                        bishop_mobility_advantage += 1
                    for _ in piece.correct_captures(piece_arr, None):
                        bishop_mobility_advantage += 1
                else:
                    for _ in piece.correct_moves(piece_arr, None):
                        bishop_mobility_advantage -= 1
                    for _ in piece.correct_captures(piece_arr, None):
                        bishop_mobility_advantage  -= 1

        c2_3 = 0.03
        knight_mobility_advantage = 0
        for piece in self.board.pieces:
            if piece.name == "knight":
                if piece.color == chessEngine.Color.WHITE:
                    for _ in piece.correct_moves(piece_arr, None):
                        knight_mobility_advantage  += 1
                    for move in piece.correct_captures(piece_arr, None):
                        knight_mobility_advantage  += 1
                else:
                    for move in piece.correct_moves(piece_arr, None):
                        knight_mobility_advantage  -= 1
                    for move in piece.correct_captures(piece_arr, None):
                        knight_mobility_advantage  -= 1

        c2_4 = 0.005
        queen_mobility_advantage = 0
        for piece in self.board.pieces:
            if piece.name == "queen":
                if piece.color == chessEngine.Color.WHITE:
                    queen_mobility_advantage += len(piece.correct_moves(piece_arr, None))
                    for move in piece.correct_captures(piece_arr, None):
                        queen_mobility_advantage+= 1
                else:
                    for move in piece.correct_moves(piece_arr, None):
                        queen_mobility_advantage -= 1
                    for move in piece.correct_captures(piece_arr, None):
                        queen_mobility_advantage -= 1

        evaluation += c1_1 * rook_advantage
        evaluation += c1_2 * bishop_advantage
        evaluation += c1_3 * knight_advantage
        evaluation += c1_4 * queen_advantage
        evaluation += c1_5 * pawn_advantage
        evaluation += c1_6 * king_advantage
        evaluation+= c2_1*rook_mobility_advantage
        evaluation+= c2_2*bishop_mobility_advantage
        evaluation+=c2_3*knight_mobility_advantage
        evaluation+= c2_4*queen_mobility_advantage
        return evaluation

    def alpha_beta_evaluation(self, depth, alpha, beta, is_white_player):
        global counter
        counter +=1
        if counter%10000 == 0:
            print(counter)

        # arr = self.board.get_str_arr()
        # print(depth, self.is_white, interesting)
        # for n, i in enumerate(arr):
        #     print(8 - n, *i)
        # print("  a  b  c  d  e  f  g  h")

        if depth <= 1:
            return self.quiscence_search(0,alpha,beta,is_white_player)

        self.moves = self.board.all_moves()
        if is_white_player:
            max_evaluation: float = - 10 ** 9
            for move in self.moves:
                self.move_straight(self.board,move)
                n: Node = Node(self.board.get_FEN(), not self.is_white)
                n.board = self.board
                self.children.append(n)
                self.evaluation: float = n.alpha_beta_evaluation(depth - 1, alpha, beta, not is_white_player)
                max_evaluation = max(max_evaluation, self.evaluation)
                alpha = max(alpha, self.evaluation)
                self.move_reverse(self.board,move)
                if beta <= alpha:
                    #print("pruned a")
                    break
            return max_evaluation
        else:
            min_evaluation: float = 10 ** 9
            for move in self.moves:
                self.move_straight(self.board, move)
                n: Node = Node(self.board.get_FEN(), not self.is_white)
                n.board = self.board
                self.children.append(n)
                self.evaluation: float = n.alpha_beta_evaluation(depth - 1, alpha, beta, not is_white_player)
                min_evaluation = min(min_evaluation, self.evaluation)
                beta = min(beta, min_evaluation)
                self.move_reverse(self.board,move)
                if beta <= alpha:
                    #print("pruned b")
                    break
            return min_evaluation

    def move_straight(self, board: chessEngine.Board, move):
        if board.active_color == chessEngine.Color.WHITE:
            board.active_color = chessEngine.Color.BLACK
        else:
            board.active_color = chessEngine.Color.WHITE
        self.dead_piece = None
        for i in range(len(board.pieces)):
            if board.pieces[i].position.row == move[1][0] and board.pieces[i].position.col == move[1][1]:
                self.dead_piece = board.pieces[i]
                board.pieces = board.pieces[:i] + board.pieces[i+1:]
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


    def move_reverse(self,board:chessEngine.Board,move):
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

    def quiscence_search(self,depth,alpha,beta,is_white_player):
        global counter
        counter += 1
        if counter % 10000 == 0:
            print(counter)
        delta = 2
        interesting = self.board.interesting_moves()

        # arr = self.board.get_str_arr()
        # print(depth, self.is_white, interesting)
        # for n, i in enumerate(arr):
        #     print(8 - n, *i)
        # print("  a  b  c  d  e  f  g  h")
        # print(depth, self.is_white, interesting)
        if depth <=-100:
            raise Exception

        if len(interesting) == 0 or depth:
            ret = self.get_static_evaluation()
            return ret
        else:
            if is_white_player:
                max_evaluation: float = - 10 ** 9
                for move in interesting:
                    self.move_straight(self.board,move)
                    n: Node = Node(self.board.get_FEN(), not self.is_white)
                    n.board = self.board
                    self.children.append(n)
                    if self.get_static_evaluation()+delta > alpha:
                        self.evaluation: float = n.quiscence_search(depth - 1, alpha, beta, not is_white_player)
                        max_evaluation = max(max_evaluation, self.evaluation)
                        alpha = max(alpha, self.evaluation)
                    self.move_reverse(self.board,move)
                    if beta <= alpha:
                        # print("pruned a in q")
                        break
                if max_evaluation >-10**7:
                    return max_evaluation
                else:
                    return self.get_static_evaluation()
            else:
                min_evaluation: float = 10 ** 9
                for move in interesting:
                    self.move_straight(self.board, move)
                    n: Node = Node(self.board.get_FEN(), not self.is_white)
                    n.board = self.board
                    self.children.append(n)
                    if self.get_static_evaluation() - delta < beta:
                        self.evaluation: float = n.quiscence_search(depth - 1, alpha, beta, not is_white_player)
                        min_evaluation = min(min_evaluation, self.evaluation)
                        beta = min(beta, min_evaluation)
                    self.move_reverse(self.board, move)
                    if beta <= alpha:
                        # print("pruned b in q")
                        break
                if min_evaluation < 10**7:
                    return min_evaluation
                else:
                    return self.get_static_evaluation()
class GameTree:
    def __init__(self, fen_notation, is_white):
        self.root: Node = Node(fen_notation, is_white)
        if is_white:
            self.evaluation: float = -10 ** 9
        else:
            self.evaluation: float = 10 ** 9
        self.is_white = is_white

    def alpha_beta_evaluation(self, depth):
        self.root.board = chessEngine.Board.from_FEN(self.root.fen)
        self.evaluation = self.root.alpha_beta_evaluation(depth, -10 ** 9, 10 ** 9, self.root.is_white)
        return self.evaluation

    def suggest_move(self, depth=None):
        move = None
        child = None
        if self.is_white:
            self.evaluation = -10 ** 9
        else:
            self.evaluation = 10 ** 9
        for i in range(len(self.root.children)):
            if self.is_white:
                if self.root.children[i].evaluation > self.evaluation:
                    self.evaluation = self.root.children[i].evaluation
                    move = self.root.moves[i]
                    child = self.root.children[i]
            else:
                if self.root.children[i].evaluation < self.evaluation:
                    self.evaluation = self.root.children[i].evaluation
                    move = self.root.moves[i]
                    child = self.root.children[i]
        return move, child


def main():
    board = chessEngine.Board.from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e3 0 1")
    #board = Board.from_FEN("rnbqkbnr/8/8/8/PPPPPPPP/8/8/K7 w KQkq e3 0 1")
    #board = Board.from_FEN("1nbqkbnr/8/8/8/1KPPPPPP/8/8/8 b KQkq e3 0 1")
    #board = Board.from_FEN("1n2kbnr/8/8/8/2PKPPbP/8/8/8 b KQkq e3 0 1")
    #board = Board.from_FEN("1n2kbnr/8/8/8/2PPPPbP/8/8/8 b KQkq e3 0 1")
    #board = Board.from_FEN("rnbqkbnr/8/8/8/KKKKKKKK/KKKKKKKK/8/K7 w KQkq e3 0 1")
    #board = Board.from_FEN("2bqkbn1/2pppp2/np2N3/r3P1p1/p2N2B1/5Q2/PPPPKPP1/RNB2r2 w KQkq - 0 1")
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
            game_tree = GameTree(board.get_FEN(),True)
            game_tree.alpha_beta_evaluation(5)
            move,_ = game_tree.suggest_move()
            print("-----------------------------------------------------")
            #print(_.board)
            print(move)
            for i in game_tree.root.children:
                print(i.evaluation,end=" ")
            print("\n")
            for i in game_tree.root.moves:
                print(i,end=" ")
            print("\n")
            print("-----------------------------------------------------")
            # first_pos = Position(int(move[0][1]) - 1, ord(move[0][0]) - ord("a"))
            # last_pos = Position(int(move[1][1]) - 1, ord(move[1][0]) - ord("a"))
            # print(first_pos, last_pos)
            # print(board.arr[first_pos.row][first_pos.col].position)
            print(board.move_piece(board.arr[move[0][0]][move[0][1]], chessEngine.Position(move[1][0],move[1][1])))
        arr = board.get_str_arr()
        print(f"color: {board.active_color}, W: {board.score[chessEngine.Color.WHITE]}, B: {board.score[chessEngine.Color.BLACK]}")
        for n, i in enumerate(arr):
            print(8 - n, *i)
        print("  a  b  c  d  e  f  g  h")


if __name__ == "__main__":
    main()
