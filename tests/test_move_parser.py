import unittest

from board import Board
from color import Color
from move import Move
from move_parser import MoveParser
from player import Player
from piece import King, Knight, Rook, Bishop, Queen, Pawn


class ParseMoveTest(unittest.TestCase):
    def setUp(self):
        self.white = Player(Color.WHITE)
        self.move_parser = MoveParser()
        self.board = Board(set())

    def test_parse_square_a1(self):
        """Ensure a1 is correctly parsed as (0, 0)."""
        self.assertEquals((0, 0), self.move_parser._parse_square('a1'))

    def test_parse_square_h8(self):
        """Ensure a1 is correctly parsed as (7, 7)."""
        self.assertEquals((7, 7), self.move_parser._parse_square('h8'))

    def test_parse_move_no_piece(self):
        """Ensure a move with no piece can be parsed."""
        expected = Move(None, (7, 6), (7, 7))
        got = self.move_parser.parse_move('h7 h8', self.board)
        self.assertEquals(got, expected)

    def test_parse_move_piece(self):
        """Ensure a move with a piece can be parsed."""
        king = King(self.white, (4, 4))
        self.board.add_piece(king)
        expected = Move(king, (4, 4), (5, 5))
        got = self.move_parser.parse_move('e5 f6', self.board)
        self.assertEquals(got, expected)

    def test_one_squares(self):
        """Ensure supplying one square raises a ValueError."""
        self.assertRaises(ValueError, self.move_parser.parse_move,
                'e4', self.board)

    def test_bad_squares(self):
        """Ensure supplying bad square raises a ValueError."""
        self.assertRaises(ValueError, self.move_parser.parse_move,
                'e4 h9', self.board)

    def test_parse_move_promotion_queen(self):
        """Ensure queen promotion is valid."""
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        expected = Move(pawn, (0, 6), (0, 7), None, Queen)
        got = self.move_parser.parse_move('a7 a8 Q', self.board)
        self.assertEquals(got, expected)

    def test_parse_move_promotion_knight(self):
        """Ensure knight promotion is valid."""
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        expected = Move(pawn, (0, 6), (0, 7), None, Knight)
        got = self.move_parser.parse_move('a7 a8 N', self.board)
        self.assertEquals(got, expected)

    def test_parse_move_promotion_bishop(self):
        """Ensure bishop promotion is valid."""
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        expected = Move(pawn, (0, 6), (0, 7), None, Bishop)
        got = self.move_parser.parse_move('a7 a8 B', self.board)
        self.assertEquals(got, expected)

    def test_parse_move_promotion_rook(self):
        """Ensure rook promotion is valid."""
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        expected = Move(pawn, (0, 6), (0, 7), None, Rook)
        got = self.move_parser.parse_move('a7 a8 R', self.board)
        self.assertEquals(got, expected)

    def test_parse_move_promotion_bad(self):
        """Ensure an invalid promotion raises a ValueError."""
        pawn = Pawn(self.white, (0, 6))
        self.board.add_piece(pawn)
        self.assertRaises(ValueError, self.move_parser.parse_move, 
                'a7 a8 K', self.board)



if __name__ == "__main__":
    unittest.main()
