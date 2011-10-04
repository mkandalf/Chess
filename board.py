from numpy import uint64, uint16

PIECE_INIT = [0xFFFF, 0xFFFF000000000000, 0xFF00, 0x42, 0x24, 0x81, 0x8,
                0x10, 0xFF000000000000, 0x4200000000000000,
                0x2400000000000000, 0x8100000000000000, 0x800000000000000,
                0x1000000000000000]
OCCUPIED_INIT = 0xffff000000000000ffff
EMPTY_INIT = 0xffffffffffffff0000

class Board(object):
    def __init__(self):
        self.piece_BB = PIECE_INIT
        self.occupied_BB = OCCUPIED_INIT
        self.empty_BB = EMPTY_INIT
        # status - 50-move, en-passant, color to move, castling rights
        self.status = uint16(0)
        side_to_move = 1
        castle = [[3,3]]*67

    # Moves will be integers, with the rightmost bits storing to, from, 
    # piece, captured, and any other flags
    # Eventually move these functions out of this file
    def get_from(self, a):
        a & 63

    def get_to(self, a):
        a >> 6 & 63

    def get_piece(self, a):
        a >> 12 & 7

    def get_captured(self, a):
        a >> 15 & 

    def flip(self, a):
        x^1

    # makeMove does not validate moves (e.g castling without rights)
    def make_move(self, move, ply):
        piece = get_piece(move)
        p_to = get_to(move)
        p_from = get_from(move)
        captured = get_captured(move)
        from_BB = uint64(1) << p_from 
        to_BB = uint64(1) << p_to 
        from_to_BB = from_BB ^ to_BB
        self.piece_BB[piece] ^= from_to_BB
        self.piece_BB[side_to_move] ^= from_to_BB 
        if piece == KING:
            if castle[ply][side_to_move] > 0:
                if (abs(p_to - p_from) == 2:
                    if p_to == rooks[6][side_to_move]:
                        p_from = rooks[7][side_to_move]
                        p_to = rooks[5][side_to_move]
                    else:
                        p_from = rooks[0][side_to_move]:
                        p_to = rooks[3][side_to_move]
                    rook_bitmap = uint64(1) << p_from | uint64(1) << p_to
                    self.piece_BB[ROOK] ^= rook_bitmap
                    self.piece_BB[side_to_move] ^= rook_bitmap
            pass
        elif piece == PAWN:
            # Put pawn logic here (em passant)
            pass
        elif piece == ROOK:
            if castle[ply][side_to_move] > 0:
                if p_from == rooks[7][side_to_move]:
                    castle[ply][side_to_move] &= 1
                elif p_from == rooks[0][side_to_move]:
                    castle[ply][side_to_move] &= 2
        if captured:
            self.piece_BB[captured] ^= to_BB                  
            self.piece_BB[flip(side_to_move)] ^= to_BB
            self.occupied_BB ^= from_BB 
            self.empty_BB ^= from_BB
        else:
            occupied_BB ^= from_to_BB 
            self.empty_BB ^= from_to_BB