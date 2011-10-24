from numpy import uint64, binary_repr
from util import north_one, south_one, east_one, west_one, print_bb, flip_diag_A1H8

all_knight_attacks = [uint64(0)]*64
all_king_attacks = [uint64(0)]*64
not_a_file = uint64(0xfefefefefefefefe)
not_h_file = uint64(0x7f7f7f7f7f7f7f7f)
pawn_advance_2_mask = [uint64(0xff000000), uint64(0xff00000000)] 
rank_mask = [uint64(0xff), uint64(0xff00), uint64(0xff0000), uint64(0xff000000), uint64(0xff00000000), uint64(0xff0000000000), uint64(0xff000000000000), uint64(0xff00000000000000)]
magic_number_shifts_rook = [52,53,53,53,53,53,53,52,53,54,54,54,54,54,54,53,
                            53,54,54,54,54,54,54,53,53,54,54,54,54,54,54,53,
                            53,54,54,54,54,54,54,53,53,54,54,54,54,54,54,53,
                            53,54,54,54,54,54,54,53,52,53,53,53,53,53,53,52]
rook_occ = [0]*64
rook_moves = [[0 for x in range(2**(64-magic_number_shifts_rook[y]))] for y in range(64)]

def init():
    init_king_attacks()
    init_knight_attacks()
#   gen_all_rook_occ()
#   rook_attacks()
    load_pregen_rook_moves()

def load_pregen_rook_moves():
  global rook_moves
  rook_moves = [[uint64(int(item.strip())) for item in line.rstrip('\r\n').split('\t')] for line in open('rook_moves')]

def gen_rook_occ(sq):
  ret_moves = []
  sq_rank = sq >> 3
  sq_file = sq & 7
  ret = uint64(0)
  for i in range(0,2**max(0,6-sq_file)):
    ret_left = ret | (uint64(i) << uint64(8*sq_rank+sq_file+1))
    for j in range(0,2**max(0,sq_file-1)):  
      ret_right = ret_left | (uint64(j) << uint64(8*sq_rank+1))
      for k in range(0,2**max(0,sq_rank-1)):
        ret_top = ret_right | \
          flip_diag_A1H8(uint64(k) << uint64(8*sq_file+1)) 
        for l in range(0,2**max(0,6-sq_rank)):
          ret_bottom = ret_top | \
            flip_diag_A1H8(uint64(l) << uint64(8*sq_file+sq_rank+1)) 
          ret_moves.append(uint64(ret_bottom))
  return ret_moves

def gen_all_rook_occ():
  for i in xrange(64):
    rook_occ[i] = (gen_rook_occ(i)) 

def rook_attacks():
  for sq,val in enumerate(rook_occ):
    print sq
    sq_rank = sq >> 3
    sq_file = sq & 7
    for occ in val:
      ret = uint64(0)
      for i in range(sq_file-1,-1,-1):                      
        ret |= (uint64(1) << uint64(8*sq_rank+i))
        if (((uint64(1) << uint64(8*sq_rank+i)) & occ) != 0): 
          break
      for i in range(sq_file+1,8):
        ret |= (uint64(1) << uint64(8*sq_rank+i)) 
        if (((uint64(1) << uint64(8*sq_rank+i)) & occ) != 0):
          break
      for i in range(sq_rank+1,8):
        ret |= (uint64(1) << uint64(8*i+sq_file)) 
        if (((uint64(1) << uint64(8*i+sq_file)) & occ) != 0):
          break
      for i in range(sq_rank-1,-1,-1):
        ret |= (uint64(1) << uint64(8*i+sq_file)) 
        if (((uint64(1) << uint64(8*i+sq_file)) & occ) != 0):
          break
      index = ((occ & occupancy_mask_rook[sq]) * magic_number_rook[sq]) \
        >> magic_number_shifts_rook[sq]
      rook_moves[sq][index] = ret
  with open('rook_moves', 'w') as file:
    file.writelines('\t'.join(map(str,i)) + '\n' for i in rook_moves)

def knight_attacks(knight):
    east = east_one(knight)
    west = west_one(knight)
    attacks = (east|west) << 16
    attacks |= (east|west) >> 16
    east = east_one(east)
    west = west_one(west)
    attacks |= (east|west) << 8
    attacks |= (east|west) >> 8
    return attacks

def king_attacks(king):
    attacks = east_one(king) | west_one(king)
    king |= attacks
    attacks |= (north_one(king) | south_one(king))
    return attacks

def init_knight_attacks():
    sq_BB = uint64(1)
    for sq in xrange(64):
        all_knight_attacks[sq] = knight_attacks(sq_BB)
        sq_BB <<= uint64(1)

def init_king_attacks():
    sq_BB = uint64(1)
    for sq in xrange(64):
        all_king_attacks[sq] = king_attacks(sq_BB)
        sq_BB <<= uint64(1)

magic_number_rook = [uint64(0xa180022080400230L), uint64(0x40100040022000L), uint64(0x80088020001002L), uint64(0x80080280841000L), uint64(0x4200042010460008L), uint64(0x4800a0003040080L), uint64(0x400110082041008L), uint64(0x8000a041000880L), uint64(0x10138001a080c010L), uint64(0x804008200480L), uint64(0x10011012000c0L), uint64(0x22004128102200L), uint64(0x200081201200cL), uint64(0x202a001048460004L), uint64(0x81000100420004L), uint64(0x4000800380004500L), uint64(0x208002904001L), uint64(0x90004040026008L), uint64(0x208808010002001L), uint64(0x2002020020704940L), uint64(0x8048010008110005L), uint64(0x6820808004002200L), uint64(0xa80040008023011L), uint64(0xb1460000811044L), uint64(0x4204400080008ea0L), uint64(0xb002400180200184L), uint64(0x2020200080100380L), uint64(0x10080080100080L), uint64(0x2204080080800400L), uint64(0xa40080360080L), uint64(0x2040604002810b1L), uint64(0x8c218600004104L), uint64(0x8180004000402000L), uint64(0x488c402000401001L), uint64(0x4018a00080801004L), uint64(0x1230002105001008L), uint64(0x8904800800800400L), uint64(0x42000c42003810L), uint64(0x8408110400b012L), uint64(0x18086182000401L), uint64(0x2240088020c28000L), uint64(0x1001201040c004L), uint64(0xa02008010420020L), uint64(0x10003009010060L), uint64(0x4008008008014L), uint64(0x80020004008080L), uint64(0x282020001008080L), uint64(0x50000181204a0004L), uint64(0x102042111804200L), uint64(0x40002010004001c0L), uint64(0x19220045508200L), uint64(0x20030010060a900L), uint64(0x8018028040080L), uint64(0x88240002008080L), uint64(0x10301802830400L), uint64(0x332a4081140200L), uint64(0x8080010a601241L), uint64(0x1008010400021L), uint64(0x4082001007241L), uint64(0x211009001200509L), uint64(0x8015001002441801L), uint64(0x801000804000603L), uint64(0xc0900220024a401L), uint64(0x1000200608243L)]

magic_number_bishop = [uint64(0x2910054208004104L), uint64(0x2100630a7020180L), uint64(0x5822022042000000L), uint64(0x2ca804a100200020L), uint64(0x204042200000900L), uint64(0x2002121024000002L), uint64(0x80404104202000e8L), uint64(0x812a020205010840L), uint64(0x8005181184080048L), uint64(0x1001c20208010101L), uint64(0x1001080204002100L), uint64(0x1810080489021800L), uint64(0x62040420010a00L), uint64(0x5028043004300020L), uint64(0xc0080a4402605002L), uint64(0x8a00a0104220200L), uint64(0x940000410821212L), uint64(0x1808024a280210L), uint64(0x40c0422080a0598L), uint64(0x4228020082004050L), uint64(0x200800400e00100L), uint64(0x20b001230021040L), uint64(0x90a0201900c00L), uint64(0x4940120a0a0108L), uint64(0x20208050a42180L), uint64(0x1004804b280200L), uint64(0x2048020024040010L), uint64(0x102c04004010200L), uint64(0x20408204c002010L), uint64(0x2411100020080c1L), uint64(0x102a008084042100L), uint64(0x941030000a09846L), uint64(0x244100800400200L), uint64(0x4000901010080696L), uint64(0x280404180020L), uint64(0x800042008240100L), uint64(0x220008400088020L), uint64(0x4020182000904c9L), uint64(0x23010400020600L), uint64(0x41040020110302L), uint64(0x412101004020818L), uint64(0x8022080a09404208L), uint64(0x1401210240484800L), uint64(0x22244208010080L), uint64(0x1105040104000210L), uint64(0x2040088800c40081L), uint64(0x8184810252000400L), uint64(0x4004610041002200L), uint64(0x40201a444400810L), uint64(0x4611010802020008L), uint64(0x80000b0401040402L), uint64(0x20004821880a00L), uint64(0x8200002022440100L), uint64(0x9431801010068L), uint64(0x1040c20806108040L), uint64(0x804901403022a40L), uint64(0x2400202602104000L), uint64(0x208520209440204L), uint64(0x40c000022013020L), uint64(0x2000104000420600L), uint64(0x400000260142410L), uint64(0x800633408100500L), uint64(0x2404080a1410L), uint64(0x138200122002900L)]

occupancy_mask_rook = [uint64(0x101010101017eL), uint64(0x202020202027cL), uint64(0x404040404047aL), uint64(0x8080808080876L), uint64(0x1010101010106eL), uint64(0x2020202020205eL), uint64(0x4040404040403eL), uint64(0x8080808080807eL), uint64(0x1010101017e00L), uint64(0x2020202027c00L), uint64(0x4040404047a00L), uint64(0x8080808087600L), uint64(0x10101010106e00L), uint64(0x20202020205e00L), uint64(0x40404040403e00L), uint64(0x80808080807e00L), uint64(0x10101017e0100L), uint64(0x20202027c0200L), uint64(0x40404047a0400L), uint64(0x8080808760800L), uint64(0x101010106e1000L), uint64(0x202020205e2000L), uint64(0x404040403e4000L), uint64(0x808080807e8000L), uint64(0x101017e010100L), uint64(0x202027c020200L), uint64(0x404047a040400L), uint64(0x8080876080800L), uint64(0x1010106e101000L), uint64(0x2020205e202000L), uint64(0x4040403e404000L), uint64(0x8080807e808000L), uint64(0x1017e01010100L), uint64(0x2027c02020200L), uint64(0x4047a04040400L), uint64(0x8087608080800L), uint64(0x10106e10101000L), uint64(0x20205e20202000L), uint64(0x40403e40404000L), uint64(0x80807e80808000L), uint64(0x17e0101010100L), uint64(0x27c0202020200L), uint64(0x47a0404040400L), uint64(0x8760808080800L), uint64(0x106e1010101000L), uint64(0x205e2020202000L), uint64(0x403e4040404000L), uint64(0x807e8080808000L), uint64(0x7e010101010100L), uint64(0x7c020202020200L), uint64(0x7a040404040400L), uint64(0x76080808080800L), uint64(0x6e101010101000L), uint64(0x5e202020202000L), uint64(0x3e404040404000L), uint64(0x7e808080808000L), uint64(0x7e01010101010100L), uint64(0x7c02020202020200L), uint64(0x7a04040404040400L), uint64(0x7608080808080800L), uint64(0x6e10101010101000L), uint64(0x5e20202020202000L), uint64(0x3e40404040404000L), uint64(0x7e80808080808000L)]

occupancy_mask_bishop = [uint64(0x40201008040200L), uint64(0x402010080400L), uint64(0x4020100a00L), uint64(0x40221400L), uint64(0x2442800L), uint64(0x204085000L), uint64(0x20408102000L), uint64(0x2040810204000L), uint64(0x20100804020000L), uint64(0x40201008040000L), uint64(0x4020100a0000L), uint64(0x4022140000L), uint64(0x244280000L), uint64(0x20408500000L), uint64(0x2040810200000L), uint64(0x4081020400000L), uint64(0x10080402000200L), uint64(0x20100804000400L), uint64(0x4020100a000a00L), uint64(0x402214001400L), uint64(0x24428002800L), uint64(0x2040850005000L), uint64(0x4081020002000L), uint64(0x8102040004000L), uint64(0x8040200020400L), uint64(0x10080400040800L), uint64(0x20100a000a1000L), uint64(0x40221400142200L), uint64(0x2442800284400L), uint64(0x4085000500800L), uint64(0x8102000201000L), uint64(0x10204000402000L), uint64(0x4020002040800L), uint64(0x8040004081000L), uint64(0x100a000a102000L), uint64(0x22140014224000L), uint64(0x44280028440200L), uint64(0x8500050080400L), uint64(0x10200020100800L), uint64(0x20400040201000L), uint64(0x2000204081000L), uint64(0x4000408102000L), uint64(0xa000a10204000L), uint64(0x14001422400000L), uint64(0x28002844020000L), uint64(0x50005008040200L), uint64(0x20002010080400L), uint64(0x40004020100800L), uint64(0x20408102000L), uint64(0x40810204000L), uint64(0xa1020400000L), uint64(0x142240000000L), uint64(0x284402000000L), uint64(0x500804020000L), uint64(0x201008040200L), uint64(0x402010080400L), uint64(0x2040810204000L), uint64(0x4081020400000L), uint64(0xa102040000000L), uint64(0x14224000000000L), uint64(0x28440200000000L), uint64(0x50080402000000L), uint64(0x20100804020000L), uint64(0x40201008040200L)]






magic_number_shifts_bishop = [58,59,59,59,59,59,59,58,59,59,59,59,59,59,59,
                              59,59,59,57,57,57,57,59,59,59,59,57,55,55,57,
                              59,59,59,59,57,55,55,57,59,59,59,59,57,57,57,
                              57,59,59,59,59,59,59,59,59,59,59,58,59,59,59,
                              59,59,59,58]
