from numpy import uint64

class Move(uint64):
  @property
  def from_(self):
    return self & uint64(63)

  @property
  def to(self):
   return  self >> uint64(6) & uint64(63)

  @property
  def piece(self):
    return self >> uint64(12) & uint64(7)

  @property
  def captured(self):
    return self >> uint64(15) & uint64(7)

  @property
  def promoted(self):
    return self >> uint64(18) & uint64(7)

  @property
  def flip(self):
    return self ^ uint64(1)
