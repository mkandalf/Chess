import unittest

from board import Board
from color import Color
from move import Move
from player import Player
from game import Game
from piece import King, Knight, Rook, Bishop, Queen, Pawn


class ChessTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(dict())
        self.white = Player(Color.WHITE)
        self.black = Player(Color.BLACK)
        self.white.opponent, self.black.opponent = self.black, self.white
        self.game = Game(self.board, (self.white, self.black))


class InCheckTest(ChessTest):
    def test_not_check(self):
        self.board.add_piece(King(self.white, (4, 4)))
        self.assertFalse(self.white.is_in_check(self.board))

    def test_not_check_pawn(self):
        self.board.add_piece(King(self.white, (4, 4)))
        self.board.add_piece(Pawn(self.black, (4, 5)))
        self.assertFalse(self.white.is_in_check(self.board))

    def test_not_check_pawn_unmoved(self):
        self.board.add_piece(King(self.white, (4, 5)))
        self.board.add_piece(Pawn(self.black, (4, 7)))
        self.assertFalse(self.white.is_in_check(self.board))

    def test_is_in_check(self):
        self.board.add_piece(King(self.white, (1, 2)))
        self.board.add_piece(Knight(self.black, (0, 0)))
        self.assertTrue(self.white.is_in_check(self.board))


if __name__ == "__main__":
    unittest.main()
