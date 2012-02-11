import random
import re

from move import Move


class Color(object):
  WHITE = 0
  BLACK = 1


class Player(object):
  def __init__(self, color):
    self.color = color

  _SQUARE_LOOKUP = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
      'e': 4, 'f': 5, 'g': 6, 'h': 7}
  def _parse_square(self, square):
    """Try to convert a square into a tuple.
    Raises a ValueError if no tuple can be parsed."""
    if not len(square) == 2:
      raise ValueError()
    f, r = square
    return self._SQUARE_LOOKUP[f], int(r) - 1 

  def _parse_move(self, string, board):
    """Try to convert a string to move.
    Raises a ValueError if no move can be decoded."""
    matches = re.search("([a-h][1-8]).*([a-h][1-8])", string)
    if matches is not None:
      start, end = matches.groups()
      return Move(board.piece_at(self._parse_square(start)), self._parse_square(end))

  def get_move(self, board):
    while True:
      try:
        return self._parse_move(raw_input("Please enter your move: "), board)
      except ValueError:
        print "Could not parse input. Try again."

  def __eq__(self, other):
    return self.color == other.color
  
  def __ne__(self, other):
    return not self == other
