import unittest
import main

class TestStringMethods(unittest.TestCase):

    def test_castling_1(self):
        board = main.chessEngine.Board.from_FEN("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
        board_arr = board.get_piece_arr()
        self.assertTrue(board.move_piece(board_arr[0][4], main.chessEngine.Position(0,6)))
        
    def test_false_castling_2(self):
        board = main.chessEngine.Board.from_FEN("rrrrkrrr/8/8/8/8/8/8/RRRRKRRR w KQkq - 0 1")
        board_arr = board.get_piece_arr()
        self.assertFalse(board.move_piece(board_arr[0][4], main.chessEngine.Position(0,2)))
        
    def test_castling_3(self):
        board = main.chessEngine.Board.from_FEN("r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1")
        board_arr = board.get_piece_arr()
        self.assertTrue(board.move_piece(board_arr[7][4], main.chessEngine.Position(7,6)))
        
    def test_false_castling_4(self):
        board = main.chessEngine.Board.from_FEN("rrrrkrrr/8/8/8/8/8/8/RRRRKRRR b KQkq - 0 1")
        board_arr = board.get_piece_arr()
        self.assertFalse(board.move_piece(board_arr[7][4], main.chessEngine.Position(7,2)))
        
    def test_piece_eat(self):
        board = main.chessEngine.Board.from_FEN("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        board_arr = board.get_piece_arr()
        self.assertTrue(board.move_piece(board_arr[3][4], main.chessEngine.Position(4,3)))
        
    def test_false_piece_eat(self):
        board = main.chessEngine.Board.from_FEN("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        board_arr = board.get_piece_arr()
        self.assertFalse(board.move_piece(board_arr[4][3], main.chessEngine.Position(3,4)))
    
    def test_queenValue(self):
        self.assertEqual(main.chessEngine.Piece.get_value("queen"), 9)

    def test_getStartWhitePownPos(self):
        self.assertEqual(main.chessEngine.Piece.get_start_position("pawn", main.chessEngine.Color.WHITE), [main.chessEngine.Position(1, i) for i in range(8)])

    def test_isupper(self):
        self.assertFalse((main.chessEngine.Piece.__str__(main.chessEngine.Piece(main.chessEngine.Color.BLACK,"pawn",1,None,True))=="White"))
    
if __name__ == '__main__':
    unittest.main()