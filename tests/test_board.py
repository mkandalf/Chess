import unittest

from board import Board
from color import Color
from move import Move
from move_parser import MoveParser
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


class PiecesTest(ChessTest):
    def test_ensure_board_has_added_piece(self):
        pawn = Pawn(self.white, (0, 1))
        self.board.add_piece(pawn)
        self.assertTrue(pawn in self.board.pieces)

    def test_ensure_player_has_added_piece(self):
        pawn = Pawn(self.white, (0, 1))
        self.board.add_piece(pawn)
        self.assertTrue(pawn in self.white.pieces)

    def test_ensure_board_does_not_have_removed_piece(self):
        pawn = Pawn(self.white, (0, 1))
        self.board.add_piece(pawn)
        self.board.remove_piece(pawn)
        self.assertTrue(pawn not in self.board.pieces)

    def test_ensure_player_does_not_have_removed_piece(self):
        pawn = Pawn(self.white, (0, 1))
        self.board.add_piece(pawn)
        self.board.remove_piece(pawn)
        self.assertTrue(pawn not in self.white.pieces)

    def test_ensure_moving_piece_changes_piece_location(self):
        pawn = Pawn(self.white, (0, 1))
        self.board.add_piece(pawn)
        self.board.move_piece(pawn, (0, 2))
        self.assertTrue(pawn.location == (0, 2))

    def test_ensure_moving_piece_does_not_break_invariants(self):
        pawn = Pawn(self.white, (0, 1))
        self.board.add_piece(pawn)
        self.board.move_piece(pawn, (0, 2))
        self.assertTrue(pawn in self.white.pieces and pawn in self.board.pieces)

class OnBoardTest(ChessTest):
    def test_is_on_board_center(self):
        self.assertTrue(self.board.is_on_board((4, 4)))

    def test_is_on_board_corner1(self):
        self.assertTrue(self.board.is_on_board((0, 0)))

    def test_is_on_board_corner2(self):
        self.assertTrue(self.board.is_on_board((7, 7)))

    def test_off_board(self):
        self.assertFalse(self.board.is_on_board((8, 8)))


class PieceAtTest(ChessTest):
    def test_no_piece(self):
        self.assertEquals(self.board.piece_at((0, 0)), None)

    def test_piece(self):
        king = King(self.white, (0, 0))
        self.board.add_piece(king)
        self.assertEquals(self.board.piece_at((0, 0)), king)


if __name__ == "__main__":
    unittest.main()
