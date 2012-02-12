import unittest

from board import Board
from move import Move
from piece import King, Knight
from player import Player, Color

class ChessTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(set())
        self.white = Player(Color.WHITE)
        self.black = Player(Color.BLACK)

class PlayerTest(ChessTest):
    def test_parse_square_a1(self):
        self.assertEquals((0, 0), self.white._parse_square('a1'))

    def test_parse_square_h8(self):
        self.assertEquals((7, 7), self.white._parse_square('h8'))

    def test_parse_move_no_piece(self):
        expected = Move(None, (7, 7))
        got = self.white._parse_move('h7 h8', self.board)
        self.assertEquals(got, expected)


class OnBoardTest(ChessTest):
    def test_on_board_center(self):
        self.assertTrue(self.board.on_board((4, 4)))

    def test_on_board_corner1(self):
        self.assertTrue(self.board.on_board((0, 0)))

    def test_on_board_corner2(self):
        self.assertTrue(self.board.on_board((7, 7)))

    def test_on_board_corner2_2(self):
        self.assertFalse(self.board.on_board((8, 8)))


class InCheckTest(ChessTest):
    def test_not_check(self):
        self.board.pieces.add(King(self.white, (4, 4)))
        self.assertFalse(self.board.in_check(self.white))

    def test_in_check(self):
        self.board.pieces.add(King(self.white, (1, 2)))
        self.board.pieces.add(Knight(self.black, (0, 0)))
        self.assertTrue(self.board.in_check(self.white))

class IsLegalTest(ChessTest):
    def test_reachable_not_check(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        move = Move(king, (2, 2))
        self.assertTrue(self.board.is_legal(move))

    def test_not_reachable_not_check(self):
        king = King(self.white, (1, 1))
        self.board.pieces.add(king)
        move = Move(king, (3, 3))
        self.assertFalse(self.board.is_legal(move))

    def test_reachable_is_check(self):
        king = King(self.white, (1, 1))
        knight = Knight(self.black, (0, 0))
        self.board.pieces.add(king)
        self.board.pieces.add(knight)
        move = Move(king, (1, 2))
        self.assertFalse(self.board.is_legal(move))


class KingTest(ChessTest):
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


class KnightTest(ChessTest):
    def test_reachable_center(self):
        knight = Knight(None, (4, 4))
        self.assertTrue(len([_ for _ in knight.reachable(self.board)]) == 8)

    def test_reachable_corner(self):
        knight = Knight(None, (0, 0))
        self.assertTrue(len([_ for _ in knight.reachable(self.board)]) == 2)

    def test_can_reach_normal(self):
        knight = Knight(None, (0, 0))
        self.assertTrue(knight.can_reach(self.board, (1, 2)))


if __name__ == "__main__":
    unittest.main()
