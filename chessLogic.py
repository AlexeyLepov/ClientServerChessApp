from chessEngine import Board


class Node:
    def __init__(self, fen_notation: str, is_white: bool):
        self.fen: str = fen_notation
        self.alpha: float = 0
        self.beta: float = 0
        self.board: Board = None
        self.is_white: bool = is_white
        self.moves: list = []

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
        self.moves = self.board.all_moves()
        if depth == 0:
            return self.get_static_evaluation()
        elif is_white_player:
            max_evaluation = - 10**9
            for move in self.moves:
                pass


class GameTree:
    def __init__(self, fen_notation, is_white):
        self.root = Node(fen_notation, is_white)
        evaluation = 0
