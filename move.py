from numpy import uint64

class Move(uint64):
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
