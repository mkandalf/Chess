import unittest

from board import Board
from game import Game
from move import Move
from player import Player


class GameTest(unittest.TestCase):
  def setUp(self):
    self.board = Board(set())
    self.player = Player(None)

  def test_parse_square_a1(self):
    self.assertEquals((0, 0), self.player._parse_square('a1'))

  def test_parse_square_h8(self):
    self.assertEquals((7, 7), self.player._parse_square('h8'))

  def test_parse_move(self):
    expected = Move(None, (7, 7))
    self.assertEquals(self.player._parse_move('h7 h8', self.board), expected)


if __name__ == "__main__":
  unittest.main()
