from chessEngine import Board, Position
import copy


class Node:
    def __init__(self, fen_notation: str, is_white: bool):
        self.fen: str = fen_notation
        self.alpha: float = 0
        self.beta: float = 0
        self.board: Board = None
        self.is_white: bool = is_white
        self.moves: list = []
        self.children: list = []
        self.evaluation: float = 0

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
        for line in board_array:
            for tile in line:
                if tile == "WR":
                    rook_advantage += 1
                elif tile == "BR":
                    rook_advantage -= 1
                elif tile == "WB":
                    bishop_advantage += 1
                elif tile == "BB":
                    bishop_advantage -= 1
                elif tile == "WN":
                    knight_advantage += 1
                elif tile == "BN":
                    knight_advantage -= 1
                elif tile == "WQ":
                    queen_advantage += 1
                elif tile == "BQ":
                    queen_advantage -= 1
                elif tile == "WP":
                    pawn_advantage += 1
                elif tile == "BP":
                    pawn_advantage -= 1
                elif tile == "WK":
                    king_advantage += 1
                elif tile == "BK":
                    king_advantage -= 1

        evaluation += c1_1 * rook_advantage
        evaluation += c1_2 * bishop_advantage
        evaluation += c1_3 * knight_advantage
        evaluation += c1_4 * queen_advantage
        evaluation += c1_5 * pawn_advantage
        evaluation += c1_6 * king_advantage
        return evaluation

    def alpha_beta_evaluation(self, depth, alpha, beta, is_white_player):
        interesting = self.board.interesting_moves()

        # arr = self.board.get_str_arr()
        # print(depth, self.is_white, interesting)
        # for n, i in enumerate(arr):
        #     print(8 - n, *i)
        # print("  a  b  c  d  e  f  g  h")

        if depth <= 0:


            if len(interesting) == 0 or depth <= -6:
                ret = self.get_static_evaluation()
                del self.board
                self.board = None
                return ret
            else:
                if is_white_player:
                    max_evaluation: float = - 10 ** 9
                    for move in interesting:
                        b: Board = copy.deepcopy(self.board)
                        b.move_piece(b.arr[int(move[0][0])][int(move[0][1])],
                                     Position(int(move[1][0]), int(move[1][1])))
                        n: Node = Node(b.get_FEN(), not self.is_white)
                        n.board = b
                        b = None
                        self.children.append(n)
                        self.evaluation: float = n.alpha_beta_evaluation(depth - 1, alpha, beta, not is_white_player)
                        max_evaluation = max(max_evaluation, self.evaluation)
                        alpha = max(alpha, self.evaluation)
                        if beta <= alpha:
                            print("pruned a in q")
                            break
                    del self.board
                    self.board = None
                    return max_evaluation
                else:
                    min_evaluation: float = 10 ** 9
                    for move in interesting:
                        b: Board = copy.deepcopy(self.board)
                        b.move_piece(b.arr[move[0][0]][move[0][1]], Position(move[1][0], move[1][1]))
                        n: Node = Node(b.get_FEN(), not self.is_white)
                        n.board = b
                        b = None
                        self.children.append(n)
                        self.evaluation: float = n.alpha_beta_evaluation(depth - 1, alpha, beta, not is_white_player)
                        min_evaluation = min(min_evaluation, self.evaluation)
                        beta = min(beta, min_evaluation)
                        if beta <= alpha:
                            print("pruned b in q")
                            break
                    del self.board
                    self.board = None
                    return min_evaluation



        self.moves = self.board.all_moves()
        if is_white_player:
            max_evaluation: float = - 10 ** 9
            for move in self.moves:
                b: Board = copy.deepcopy(self.board)
                b.move_piece(b.arr[int(move[0][0])][int(move[0][1])], Position(int(move[1][0]), int(move[1][1])))
                n: Node = Node(b.get_FEN(), not self.is_white)
                n.board = b
                b = None
                self.children.append(n)
                self.evaluation: float = n.alpha_beta_evaluation(depth - 1, alpha, beta, not is_white_player)
                max_evaluation = max(max_evaluation, self.evaluation)
                alpha = max(alpha, self.evaluation)
                if beta <= alpha:
                    print("pruned a")
                    break
            del self.board
            self.board = None
            return max_evaluation
        else:
            min_evaluation: float = 10 ** 9
            for move in self.moves:
                b: Board = copy.deepcopy(self.board)
                b.move_piece(b.arr[move[0][0]][move[0][1]], Position(move[1][0], move[1][1]))
                n: Node = Node(b.get_FEN(), not self.is_white)
                n.board = b
                b = None
                self.children.append(n)
                self.evaluation: float = n.alpha_beta_evaluation(depth - 1, alpha, beta, not is_white_player)
                min_evaluation = min(min_evaluation, self.evaluation)
                beta = min(beta, min_evaluation)
                if beta <= alpha:
                    print("pruned b")
                    break
            del self.board
            self.board = None
            return min_evaluation


class GameTree:
    def __init__(self, fen_notation, is_white):
        self.root: Node = Node(fen_notation, is_white)
        if is_white:
            self.evaluation: float = -10 ** 9
        else:
            self.evaluation: float = 10 ** 9
        self.is_white = is_white

    def alpha_beta_evaluation(self, depth):
        self.root.board = Board.from_FEN(self.root.fen)
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
