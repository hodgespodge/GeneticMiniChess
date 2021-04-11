from collections import UserDict
from copy import deepcopy


def piece_list(): # pieces are numbered 0-11
    return ["white_king","white_queen","white_rook","white_bishop","white_knight","white_pawn","black_king","black_queen","black_rook","black_bishop","black_knight","black_pawn"]
def white_piece_list():
    return ["white_king","white_queen","white_rook","white_bishop","white_knight","white_pawn"]
def black_piece_list():
    return ["black_king","black_queen","black_rook","black_bishop","black_knight","black_pawn"]

def get_new_board_after_move(board,move,first_player):

    new_board = deepcopy(board) 
    new_board[move[1]] = move[2] # replace dict value at key = coord with new piece
    del new_board[move[0]]       # Piece moved so delete old key/value 

    return new_board

# heuristic_coefficients will be in this order: 
# 0-6   ["white_king","white_queen","white_rook","white_bishop","white_knight","white_pawn"]
# 7-11  ["black_king","black_queen","black_rook","black_bishop","black_knight","black_pawn"]

def get_board_heuristic(board,heuristic_coefficients):

    score = 0

    for piece in board.values():

        if piece < 7:
            score += heuristic_coefficients[piece] # Add points for white
        else:
            score -= heuristic_coefficients[piece % 7] # Subtract points for black

    return score

class Board(UserDict):
    def __init__(self,board_dimensions) -> None:
        self.hash = self.get_hash_of_board()
        self.board_dimensions = board_dimensions #Tuple(width,heigh)
  
    def get_hash_of_board(self):
        return hash(self.data)

    def _in_board(self,coord):

        if coord[0] > self.board_dimensions[0] or coord[0] < 0:     # out of width bounds
            return False
        elif coord[1] > self.board_dimensions[1] or coord[1] < 1:   # out of height bounds
            return False
        else:
            return True

    def _space_occupied_by_opponent(self,coord,first_player):
        return (self.data[coord] > 5 and first_player) or (self.data[coord] <= 5 and not first_player)

    def _space_empty(self,coord):
        return not self.get(coord,-1) >= 0  #dict.get('key',default)

    def _valid_destination(self,move,first_player):

        coord = move[1] 
        return self._in_board(coord) and (self._space_empty(coord) or self._space_occupied_by_opponent(coord,first_player))
        
    def _cardinal_directions(self):
        return ((0,1),(1,0),(0,-1),(-1,0))  # Up,Right,Down,Left

    def _diagonal_directions(self):
        return ((1,1),(1,-1),(-1,-1),(-1,1)) # Up-Right, Down-Right, Down-Left, Up-Left

    def _knight_directions(self):
        return ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))

    def _king_moves(self, loc_piece,first_player):
        coord = loc_piece[0]
        piece = loc_piece[1]

        moves = []

        for direction in self._cardinal_directions()+self._diagonal_directions(): 
            move = tuple(coord,map(sum,zip(coord,direction)),piece)  # Get destination

            if self._valid_destination(move,first_player):
                moves.append(move)

        return moves

    def _queen_moves(self, loc_piece,first_player):
        coord = loc_piece[0]
        piece = loc_piece[1]


        moves = []

        for direction in self._cardinal_directions()+self._diagonal_directions(): 

            while(True):

                move = tuple(coord,map(sum,zip(coord,direction)),piece)  # Get destination

                if self._valid_destination(move,first_player):
                    moves.append(move)

                else: 
                    break

        return moves

    def _rook_moves(self, loc_piece,first_player):
        coord = loc_piece[0]
        piece = loc_piece[1]

        moves = []

        for direction in self._cardinal_directions(): 

            while(True):

                move = tuple(coord,map(sum,zip(coord,direction)),piece)  # Get destination

                if self._valid_destination(move,first_player):
                    moves.append(move)

                else: 
                    break

        return moves

    def _bishop_moves(self,loc_piece,first_player):
        coord = loc_piece[0]
        piece = loc_piece[1]

        moves = []

        for direction in self._diagonal_directions(): 

            while(True):

                move = tuple(coord,map(sum,zip(coord,direction)),piece)  # Get destination

                if self._valid_destination(move,first_player):
                    moves.append(move)

                else: 
                    break

        return moves

    def _knight_moves(self, loc_piece,first_player):
        coord = loc_piece[0]
        piece = loc_piece[1]

        moves = []

        for direction in self._knight_directions(): 
            move = tuple(coord,map(sum,zip(coord,direction)),piece)  # Get destination

            if self._valid_destination(move,first_player):
                moves.append(move)

        return moves

    def _pawn_moves(self,loc_piece,first_player): 
        coord = loc_piece[0]
        piece = loc_piece[1]

        moves = []

        if first_player: # white

            if coord[1] + 1 == self.board_dimensions[1]: # If pawn would reach end of board by moving up, always promote to queen
    
                piece = 1 # White Queen

            move = tuple(coord,coord+(0,1),piece) # move up one space
            if self._space_empty(move[1]) and self._in_board(move[1]):
                
                moves.append(move)

                if coord[1] == 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple(coord,coord+(0,2),piece)
                    if self._space_empty(move[1]) and self._in_board(move[1]):
                        moves.append(move)
                        
            
            move = tuple(coord,coord+(-1,1),piece) # capture up left
            if self._space_occupied_by_opponent(move[1],first_player) and self._in_board(move[1]):
                moves.append(move)

            move = tuple(coord,coord+ (1,1),piece) # capture up right
            if self._space_occupied_by_opponent(move[1],first_player) and self._in_board(move[1]):
                moves.append(move)

        else:   # black

            if coord[1] - 1 == 0: # If pawn would reach end of board by moving up, always promote to queen
    
                piece = 7 # Black queen

            move = tuple(coord,coord+(0,-1),piece) # move down one space
            if self._space_empty(move[1]) and self._in_board(move[1]):
                moves.append(move)

                if coord[1] == self.board_dimensions[1] - 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple(coord,coord+(0,-2),piece)
                    if self._space_empty(move[1]) and self._in_board(move[1]):
                        moves.append(move)
                        
            move = tuple(coord,coord+(-1,-1),piece) # capture down left
            if self._space_occupied_by_opponent(move[1],first_player) and self._in_board(move[1]):
                moves.append(move)

            move = tuple(coord,coord+ (1,-1),piece) # capture down right
            if self._space_occupied_by_opponent(move[1],first_player) and self._in_board(move[1]):
                moves.append(move)


    def _get_piece_moves(self,loc_piece,first_player): # moves are always tuple(tuple(x1,y1),tuple(x2,y2),piece)

        piece = loc_piece[1]

        if first_player: # white 
            if piece == 0:      #king

                return self._king_moves(loc_piece,first_player)

            elif piece == 1:    #queen
                return self._queen_moves(loc_piece,first_player)

            elif piece == 2:    #rook

                return self._rook_moves(loc_piece,first_player)

            elif piece == 3:    #bishop
                return self._bishop_moves(loc_piece,first_player)

            elif piece == 4:    #knight
                return self._knight_moves(loc_piece,first_player)

            elif piece == 5:    #pawn
                return self._pawn_moves(loc_piece,first_player=first_player)
                
            else:
                print("error: player id doesn't match piece.")

        else:   # black

            if piece == 6:      #king
                return self._king_moves(loc_piece,first_player)

            elif piece == 7:    #queen
                return self._queen_moves(loc_piece,first_player)
            elif piece == 8:    #rook
                return self._rook_moves(loc_piece,first_player)

            elif piece == 9:    #bishop
                return self._bishop_moves(loc_piece,first_player)

            elif piece == 10:    #knight
                return self._knight_moves(loc_piece,first_player)

            elif piece == 11:    #pawn
                return self._pawn_moves(loc_piece,first_player=first_player)

            else:
                print("error: player id doesn't match piece.")


    def get_all_moves(self,first_player): # moves are always tuple(tuple(x1,y1),tuple(x2,y2),piece)

        player_pieces = []
        moves = []

        if first_player: # white player

            for piece in self.data.items: 
                if piece[1] <= 5: #if piece is white
                    player_pieces.append(piece)

        else:   # black player
             for piece in self.data.items: 
                if piece[1] > 5: #if piece is black
                    player_pieces.append(piece)

        for piece in player_pieces:
            moves.append(self._get_piece_moves(piece,first_player))

        return moves
