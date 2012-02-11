import unittest

from board import Board
from game import Game
from move import Move
from piece import King
from player import Player, Color


class PlayerTest(unittest.TestCase):
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


class KingTest(unittest.TestCase):
  def setUp(self):
    self.player = Player(Color.WHITE)
    self.board = Board(set())

  def test_reachable_normal(self):
    king = King(self.player, (4, 4))
    reachable = len([_ for _ in king.reachable(self.board)])
    self.assertTrue(reachable == 8, reachable)

  def test_can_reach_normal(self):
    king = King(self.player, (4, 4))
    self.assertTrue(king.can_reach(self.board, (3, 3)))



if __name__ == "__main__":
  unittest.main()
