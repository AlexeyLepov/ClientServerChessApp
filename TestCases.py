import unittest
import main

class TestStringMethods(unittest.TestCase):

    def test_kingValue(self):
        self.assertEqual(main.chessEngine.Piece.get_value("king"), 0)

    def test_queenValue(self):
        self.assertEqual(main.chessEngine.Piece.get_value("queen"), 9)

    def test_getStartWhitePownPos(self):
        self.assertEqual(main.chessEngine.Piece.get_start_position("pawn", main.chessEngine.Color.WHITE), [main.chessEngine.Position(1, i) for i in range(8)])

    def test_getStartBlackPownPos(self):
        self.assertEqual(main.chessEngine.Piece.get_start_position("pawn", main.chessEngine.Color.BLACK), [main.chessEngine.Position(6, i) for i in range(8)])
    
    def test_isupper(self):
        self.assertFalse((main.chessEngine.Piece.__str__(main.chessEngine.Piece(main.chessEngine.Color.BLACK,"pawn",1,None,True))=="White"))
    
if __name__ == '__main__':
    unittest.main()