"""A collection of functions for manipulating 64-bit bitboards."""
import numpy as np
from numpy import uint64 as bitboard


ROW_WIDTH = 8

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

NOT_A_FILE = np.uint64(0xfefefefefefefefe)
NOT_H_FILE = np.uint64(0x7f7f7f7f7f7f7f7f)


#TODO: Add a meaningful doctest
def bit_scan_forward(bitboard):
  """Get the index of the first bit set to True."""
  return INDEX_64[((np.uint64(bitboard & -bitboard) * DEBRUIJN) >> 58)]


#TODO: Might make more sense to throw an exception.
def clear_least_bit(bitboard):
  """Set the rightmost 1 to a 0.
  In the case the bitboard is empty, do nothing.
  >>> bb = bitboard(0xf0f0f0f000000000)
  >>> print_bb(bb)
  11110000
  11110000
  11110000
  11110000
  00000000
  00000000
  00000000
  00000000
  >>> print_bb(clear_least_bit(bb))
  11110000
  11110000
  11110000
  11100000
  00000000
  00000000
  00000000
  00000000
  """
  return bitboard & ~(np.uint64(1) << np.uint64(bit_scan_forward(bitboard)))


def shift(bitboard, x, y):
  """Shift the bitboard by the specified x and y.
  >>> bb = bitboard(0xf0f0f0f000000000)
  >>> print_bb(bb)
  11110000
  11110000
  11110000
  11110000
  00000000
  00000000
  00000000
  00000000
  >>> print_bb(shift(bb, 4, 0))
  00001111
  00001111
  00001111
  00001111
  00000000
  00000000
  00000000
  00000000
  >>> print_bb(shift(bb, 0, -4))
  00000000
  00000000
  00000000
  00000000
  11110000
  11110000
  11110000
  11110000
  >>> print_bb(shift(bb, 4, -4))
  00000000
  00000000
  00000000
  00000000
  00001111
  00001111
  00001111
  00001111
  >>> print_bb(shift(bb, 8, 0))
  00000000
  00000000
  00000000
  00000000
  00000000
  00000000
  00000000
  00000000
  """
  while x > 0:
    bitboard = (bitboard >> np.uint64(1)) & NOT_H_FILE
    x -= 1
  while x < 0:
    bitboard = (bitboard << np.uint64(1)) & NOT_A_FILE
    x += 1
  while y > 0:
    bitboard <<= ROW_WIDTH
    y -= 1
  while y < 0:
    bitboard >>= ROW_WIDTH
    y += 1
  return bitboard


def flip(bitboard):
  """Flip the least significant bit.
  >>> bb = bitboard(0xf0f0f0f000000000)
  >>> print_bb(bb)
  11110000
  11110000
  11110000
  11110000
  00000000
  00000000
  00000000
  00000000
  >>> print_bb(flip(bb))
  11110000
  11110000
  11110000
  11110000
  00000000
  00000000
  00000000
  00000001
  """
  return bitboard ^ 1


def flip_diag_A1H8(bitboard):
  """Flip the board along the A1-H8 diagonal.
  >>> bb = bitboard(0xfefefefefefefefe)
  >>> print_bb(bb)
  11111110
  11111110
  11111110
  11111110
  11111110
  11111110
  11111110
  11111110
  >>> print_bb(flip_diag_A1H8(bb))
  11111111
  11111111
  11111111
  11111111
  11111111
  11111111
  11111111
  00000000
  """
  t = np.uint64()
  k1 = np.uint64(0x5500550055005500)
  k2 = np.uint64(0x3333000033330000)
  k4 = np.uint64(0x0f0f0f0f00000000)
  t = k4 & (bitboard ^ (bitboard << np.uint64(28)))
  bitboard ^= t ^ (t >> np.uint64(28))
  t = k2 & (bitboard ^ (bitboard << np.uint64(14)))
  bitboard ^= t ^ (t >> np.uint64(14))
  t = k1 & (bitboard ^ (bitboard << np.uint64(7)))
  bitboard ^= t ^ (t >> np.uint64(7))
  return np.uint64(bitboard)


def flip_vertical(bitboard):
  """Flip the board along the horizontal axis.
  >>> bb = bitboard(0xf0f0f0f0fefefefe)
  >>> print_bb(bb)
  11110000
  11110000
  11110000
  11110000
  11111110
  11111110
  11111110
  11111110
  >>> print_bb(flip_vertical(bb))
  11111110
  11111110
  11111110
  11111110
  11110000
  11110000
  11110000
  11110000
  """
  k1 = np.uint64(0x00FF00FF00FF00FF)
  k2 = np.uint64(0x0000FFFF0000FFFF)
  bitboard = ((bitboard >> np.uint64(8)) & k1) \
      | ((bitboard & k1) << np.uint64(8))
  bitboard = ((bitboard >> np.uint64(16)) & k2) \
      | ((bitboard & k2) << np.uint64(16))
  bitboard = (bitboard >> np.uint64(32)) | (bitboard << np.uint64(32))
  return bitboard


def _divide(n, k):
  '''Divide n into sets of size of k or smaller.'''
  for i in range(0, len(n), k):
      yield n[i:i + k]


def print_bb(bitboard):
  """Prints a bitboard in human-readable form.
  >>> bb = bitboard(0xfefefefefefefefe)
  >>> print_bb(bb)
  11111110
  11111110
  11111110
  11111110
  11111110
  11111110
  11111110
  11111110
  """
  print "\n".join(_divide(np.binary_repr(bitboard).zfill(64), ROW_WIDTH))

if __name__ == '__main__':
  import doctest
  doctest.testmod()
