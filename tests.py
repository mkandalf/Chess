import unittest

from board import Board
from game import Game
from move import Move
from piece import King, Knight
from player import Player, Color


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(set())
        self.player = Player(None)

    def test_parse_square_a1(self):
        self.assertEquals((0, 0), self.player._parse_square('a1'))

    def test_parse_square_h8(self):
        self.assertEquals((7, 7), self.player._parse_square('h8'))

    def test_parse_move_no_piece(self):
        self.assertEquals(self.player._parse_move('h7 h8', self.board), Move(None, (7, 7)))


class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(set())


class OnBoardTest(BoardTest):
    def test_on_board_center(self):
        self.assertTrue(self.board.on_board((4, 4)))

    def test_on_board_corner1(self):
        self.assertTrue(self.board.on_board((0, 0)))

    def test_on_board_corner2(self):
        self.assertTrue(self.board.on_board((7, 7)))

    def test_on_board_corner2_2(self):
        self.assertFalse(self.board.on_board((8, 8)))


class InCheckTest(BoardTest):
    def setUp(self):
        super(InCheckTest, self).setUp()
        self.white = Player(Color.WHITE)
        self.black = Player(Color.BLACK)

    def test_not_check(self):
        self.board.pieces.add(King(self.white, (4, 4)))
        self.assertFalse(self.board.in_check(self.white))

    def test_in_check(self):
        self.board.pieces.add(King(self.white, (4, 4)))
        self.board.pieces.add(Knight(self.black, (3, 2)))
        self.assertFalse(self.board.in_check(self.white))


class PieceTest(unittest.TestCase):
    def setUp(self):
        self.player = Player(Color.WHITE)
        self.board = Board(set())


class KingTest(PieceTest):
    def test_reachable_center(self):
        king = King(None, (4, 4))
        reachable = len([_ for _ in king.reachable(self.board)])
        self.assertTrue(reachable == 8, reachable)

    def test_reachable_corner(self):
        king = King(None, (0, 0))
        reachable = len([_ for _ in king.reachable(self.board)])
        self.assertTrue(reachable == 3, reachable)

    def test_can_reach_normal(self):
        king = King(None, (4, 4))
        self.assertTrue(king.can_reach(self.board, (3, 3)))


class KnightTest(PieceTest):
    def test_reachable_center(self):
        knight = Knight(None, (4, 4))
        self.assertTrue(len([_ for _ in knight.reachable(self.board)]) == 8)

    def test_reachable_corner(self):
        knight = Knight(None, (0, 0))
        self.assertTrue(len([_ for _ in knight.reachable(self.board)]) == 2)

    def test_can_reach_normal(self):
        knight = Knight(None, (1, 0))
        self.assertTrue(knight.can_reach(self.board, (2, 2)))


if __name__ == "__main__":
  unittest.main()
