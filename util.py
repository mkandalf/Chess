from numpy import uint64, binary_repr

not_a_file = uint64(0xfefefefefefefefe)
not_h_file = uint64(0x7f7f7f7f7f7f7f7f)

def bit_scan_forward(bitboard):
    index_64 = [63,  0, 58,  1, 59, 47, 53,  2,
                60, 39, 48, 27, 54, 33, 42,  3,
                61, 51, 37, 40, 49, 18, 28, 20,
                55, 30, 34, 11, 43, 14, 22,  4,
                62, 57, 46, 52, 38, 26, 32, 41,
                50, 36, 17, 19, 29, 10, 13, 21,
                56, 45, 25, 31, 35, 16,  9, 12,
                44, 24, 15,  8, 23,  7,  6,  5]
    debruijn = uint64(0x07EDD5E59A4E28C2)
    return index_64[((uint64(bitboard & -bitboard) * debruijn) >> 58)] 

def clear_least_bit(bitboard):
    bit = uint64(1) << uint64(bit_scan_forward(bitboard))
    return bitboard & ~bit

def east_one(a):
    return (a << uint64(1)) & not_a_file

def west_one(a):
    return (a >> uint64(1)) & not_h_file

def north_one(a):
    return (a << uint64(8))

def south_one(a): 
    return (a >> uint64(8)) 

def no_ea_one(a):
    return (a << uint64(9)) & not_a_file

def so_ea_one(a):
    return (a >> uint64(7)) & not_a_file

def no_we_one(a):
    return (a << uint64(7)) & not_h_file

def so_we_one(a):
    return (a >> uint64(9)) & not_h_file

def flip(a):
    return (a ^ 1)

def flip_diag_A1H8(x):
  t = uint64(0)
  k1 = uint64(0x5500550055005500)
  k2 = uint64(0x3333000033330000)
  k4 = uint64(0x0f0f0f0f00000000)
  t = k4 & (x ^ (x << uint64(28)))
  x ^= t ^ (t >> uint64(28))
  t = k2 & (x ^ (x << uint64(14)))
  x ^= t ^ (t >> uint64(14))
  t = k1 & (x ^ (x << uint64(7)))
  x ^= t ^ (t >> uint64(7))
  return uint64(x)

def flip_vertical(x):
  k1 = uint64(0x00FF00FF00FF00FF)
  k2 = uint64(0x0000FFFF0000FFFF)
  x = ((x >>  uint64(8)) & k1) | ((x & k1) << uint64(8))
  x = ((x >> uint64(16)) & k2) | ((x & k2) << uint64(16))
  x = ( x >> uint64(32))       | ( x       << uint64(32))
  return x

def print_bb(a):
  s = str(binary_repr(a))
  s = s.zfill(64)
  for i in range(0,8):
    f = i*8
    l = f+8
    print s[f:l]
  print ''
