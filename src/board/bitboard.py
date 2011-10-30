"""A 64-bit bitboard object."""
import numpy as np


def divide(n, k):
  '''Divide n into sets of size of k or smaller.'''
  for i in range(0, len(n), k):
      yield n[i:i+k]


class Bitboard(np.uint64):
  """A 64-bit bitboard."""

  INDEX_64 = [
      63,  0, 58,  1, 59, 47, 53,  2,
      60, 39, 48, 27, 54, 33, 42,  3,
      61, 51, 37, 40, 49, 18, 28, 20,
      55, 30, 34, 11, 43, 14, 22,  4,
      62, 57, 46, 52, 38, 26, 32, 41,
      50, 36, 17, 19, 29, 10, 13, 21,
      56, 45, 25, 31, 35, 16,  9, 12,
      44, 24, 15,  8, 23,  7,  6,  5]
  DEBRUIJN = np.uint64(0x07EDD5E59A4E28C2)
  def bit_scan_forward(self):
    return Bitboard(self.INDEX_64[((np.uint64(self & -self) * self.DEBRUIJN) >> 58)])

  def clear_least_bit(self):
    """Set the rightmost 1 to a 0.
    
    In the case the bitboard is empty, do nothing."""
    return Bitboard(self & ~(np.uint64(1) << np.uint64(self.bit_scan_forward())))

  NOT_H_FILE = np.uint64(0x7f7f7f7f7f7f7f7f)
  def east(self, shift=1):
    """Shift all the bits to the right. Bits in the H-column will be truncated."""
    return Bitboard((self >> np.uint64(shift)) & self.NOT_H_FILE)

  NOT_A_FILE = np.uint64(0xfefefefefefefefe)
  def west(self, shift=1):
    """Shift all the bits to the left. Bits in the A-column will be truncated."""
    return Bitboard((self << np.uint64(shift)) & self.NOT_A_FILE)

  ROW_WIDTH = 8
  def north(self, shift=1):
    """Shift all the bits up. Bits in the 8-row will be truncated."""
    return Bitboard((self << np.uint64(self.ROW_WIDTH * shift)))

  def south(self, shift=1):
    """Shift all the bits down. Bits in the 1-row will be truncated."""
    return Bitboard((self >> np.uint64(self.ROW_WIDTH * shift)))

  def flip(self):
    """Flip the least significant bit."""
    return Bitboard(self ^ 1)

  def flip_diag_A1H8(self):
    """Flip the board along the A1-H8 diagonal."""
    t = np.uint64()
    k1 = np.uint64(0x5500550055005500)
    k2 = np.uint64(0x3333000033330000)
    k4 = np.uint64(0x0f0f0f0f00000000)
    t = k4 & (self ^ (self << np.uint64(28)))
    self ^= t ^ (t >> np.uint64(28))
    t = k2 & (self ^ (self << np.uint64(14)))
    self ^= t ^ (t >> np.uint64(14))
    t = k1 & (self ^ (self << np.uint64(7)))
    self ^= t ^ (t >> np.uint64(7))
    return Bitboard(np.uint64(self))

  def flip_vertical(self):
    """Flip the board along the horizontal axis."""
    k1 = np.uint64(0x00FF00FF00FF00FF)
    k2 = np.uint64(0x0000FFFF0000FFFF)
    self = ((self >>  np.uint64(8)) & k1) | ((self & k1) << np.uint64(8))
    self = ((self >> np.uint64(16)) & k2) | ((self & k2) << np.uint64(16))
    self = ( self >> np.uint64(32))       | ( self       << np.uint64(32))
    return Bitboard(self)

  def __repr__(self):
    return "\n".join(divide(np.binary_repr(self).zfill(64), self.ROW_WIDTH))
