from numpy import uint64

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
  return a ^ 1
