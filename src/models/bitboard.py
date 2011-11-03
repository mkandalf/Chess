"""A collection of functions for manipulating 64-bit bitboards."""
import numpy as np


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

def bit_scan_forward(bitboard):
  return INDEX_64[((np.uint64(bitboard & -bitboard) * DEBRUIJN) >> 58)]

def clear_least_bit(bitboard):
  """Set the rightmost 1 to a 0.
  In the case the bitboard is empty, do nothing."""
  return bitboard & ~(np.uint64(1) << np.uint64(bitboard.bit_scan_forward()))

NOT_A_FILE = np.uint64(0xfefefefefefefefe)
NOT_H_FILE = np.uint64(0x7f7f7f7f7f7f7f7f)
#abstract these
def east(bitboard, shift=1):
  """Shift all the bits to the right. Bits in the H-column will be truncated."""
  return Bitboard((bitboard >> np.uint64(shift)) & bitboard.NOT_H_FILE)

def west(bitboard, shift=1):
  """Shift all the bits to the left. Bits in the A-column will be truncated."""
  return Bitboard((bitboard << np.uint64(shift)) & bitboard.NOT_A_FILE)

def north(bitboard, shift=1):
  """Shift all the bits up. Bits in the 8-row will be truncated."""
  return Bitboard((bitboard << np.uint64(bitboard.ROW_WIDTH * shift)))

def south(bitboard, shift=1):
  """Shift all the bits down. Bits in the 1-row will be truncated."""
  return Bitboard((bitboard >> np.uint64(bitboard.ROW_WIDTH * shift)))

def flip(bitboard):
  """Flip the least significant bit."""
  return bitboard ^ 1

def flip_diag_A1H8(bitboard):
  """Flip the board along the A1-H8 diagonal."""
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
  """Flip the board along the horizontal axis."""
  k1 = np.uint64(0x00FF00FF00FF00FF)
  k2 = np.uint64(0x0000FFFF0000FFFF)
  bitboard = ((bitboard >> np.uint64(8)) & k1) | ((bitboard & k1) << np.uint64(8))
  bitboard = ((bitboard >> np.uint64(16)) & k2) | ((bitboard & k2) << np.uint64(16))
  bitboard = (bitboard >> np.uint64(32)) | (bitboard << np.uint64(32))
  return bitboard

def _divide(n, k):
  '''Divide n into sets of size of k or smaller.'''
  for i in range(0, len(n), k):
      yield n[i:i + k]

ROW_WIDTH = 8
def __repr__(bitboard):
  return "\n".join(_divide(np.binary_repr(bitboard).zfill(64), ROW_WIDTH))
