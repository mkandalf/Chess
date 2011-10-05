from numpy import uint64

all_king_attacks = [uint64(0)]*64
not_a_file = uint64(0xfefefefefefefefe)
not_h_file = uint64(0x7f7f7f7f7f7f7f7f)

def init():
    init_king_attacks()

def king_attacks(king):
    attacks = east_one(king) | west_one(king)
    king |= attacks
    attacks |= (north_one(king) | south_one(king))
    return attacks

def init_king_attacks():
    sq_BB = uint64(1)
    for sq in xrange(64):
        all_king_attacks[sq] = king_attacks(sq_BB)
        sq_BB <<= uint64(1)

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
