"""Contains the move class."""

from numpy import uint16

class Move(uint16):
  """A move is a 16-bit integer consisting of all relevant information required for a move."""
  @property
  def from_(self):
    return self & 63

  @property
  def to(self):
   return  self >> 6 & 63

  @property
  def piece(self):
    return self >> 12 & 7

  @property
  def captured(self):
    return self >> 15 & 7

  @property
  def promoted(self):
    return self >> 18 & 7

  @property
  def flip(self):
    return self ^ 1
