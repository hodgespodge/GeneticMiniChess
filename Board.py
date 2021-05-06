from collections import UserDict
from copy import deepcopy
# from operator import add, sub
from math import pow

from MiscFunctions import tuple_add

def get_new_board_after_move(board,move,first_player):

    new_board = deepcopy(board) 
    new_board[move[1]] = move[2] # replace dict value at key = coord with new piece
    del new_board[move[0]]       # Piece moved so delete old key/value 

    # king locations are tracked for easy "check" testing
    if move[2] == 0:
        new_board.white_king_loc_piece = (move[1], 0)
    elif move[2] == 6:
        new_board.black_king_loc_piece = (move[1], 6)

    return new_board

# Checks if game is over for the player 
def game_over(board,first_player):

    childNodes = board.get_all_moves(first_player)

    if len(childNodes) < 1: # If no moves are possible, game must be over

        if board._player_king_threatened(first_player): # If king in check and no moves to leave check

            if first_player:
                return True, -1
            else:
                return True, 1

        else:
            return True, 0 # Otherwise game is draw

    else:
        return False, 0

# heuristic_coefficients will be in this order: 
# 0-5   ["king","queen","rook","bishop","knight","pawn"]

def get_board_heuristic(board,heuristic_coefficients):

    score = 0

    for piece in board.values():

        if piece <= 5:
            score += heuristic_coefficients[piece] # Add points for white
        else:
            score -= heuristic_coefficients[piece % 6] # Subtract points for black

    return score

class Board(dict):
    def __init__(self,board_dimensions,white_king_loc_piece = None,black_king_loc_piece = None) -> None:
        self.board_dimensions = board_dimensions #Tuple(width,heigh)
        self.white_king_loc_piece = white_king_loc_piece
        self.black_king_loc_piece = black_king_loc_piece
  
    def _hash_(self):

        items = sorted(self.items(), key = lambda x : x[0][0] + 12*x[0][1])

        return hash(frozenset(items))

    def get_board_hash(self,first_player):

        items = sorted(self.items(), key = lambda x : x[0][0] + 12*x[0][1])

        return hash(frozenset(items))

    def _in_board(self,coord):

        if coord[0] > self.board_dimensions[0] or coord[0] < 0:     # out of width bounds
            return False
        elif coord[1] > self.board_dimensions[1] or coord[1] < 1:   # out of height bounds
            return False
        else:
            return True

    def _space_occupied_by_opponent(self,coord,first_player):
        if first_player:
            return self.get(coord, 0) > 5

        else:
            return self.get(coord, 100) <= 5

    def _space_empty(self,coord):
        return not self.get(coord,-1) >= 0  #dict.get('key',default)




    def _move_into_check(self,move,first_player):

        temp_board = get_new_board_after_move(self,move,first_player)
        
        return temp_board._player_king_threatened(first_player)

    def  _player_king_threatened(self,first_player):

        if first_player:
            coord = self.white_king_loc_piece[0]
            offset = 6 # first player checks against black pieces

            for direction in ((1,1),(-1,1)): # white king threatened by black pawn?
                if self.get(tuple_add(coord,direction), -1) == 11: #if occupied by enemy pawn
                    return True
        else:
            coord = self.black_king_loc_piece[0]
            offset = 0 #not first player checks against white pieces

            for direction in ((1,-1),(-1,-1)): # black king threatened by white pawn?
                if self.get(tuple_add(coord,direction), -1) == 5: #if occupied by enemy pawn
                    return True
            
        for direction in self._knight_directions(): # king threatened by enemy knight?
            if self.get(tuple_add(coord,direction), -1) == 4 + offset: #if occupied by enemy knight
                return True

        for direction in self._cardinal_directions(): # king threatened by enemy queen or rook
            loc = tuple_add(coord,direction)

            while(self._in_board(loc)):
                piece = self.get(loc  , None)

                if piece is not None:
                    if piece in {1 + offset, 2 + offset}: #threatened by queen or rook
                        return True
                    else:
                        break #switch direction

                loc = tuple_add(loc,direction)

        for direction in self._diagonal_directions():  # king threatened by enemy queen or bishop
            loc = tuple_add(coord,direction)
            
            while(self._in_board(loc)):
                piece = self.get(loc  , None)

                if piece is not None:
                    if piece in {1 + offset, 3 + offset}: #threatened by queen or bishop
                        return True
                    else:
                        break #switch direction

                loc = tuple_add(loc,direction)
        
        return False

    def _valid_destination(self,move,first_player):

        coord = move[1] 
        return self._in_board(coord) and (self._space_empty(coord) or self._space_occupied_by_opponent(coord,first_player)) and not self._move_into_check(move,first_player)
        
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

        for direction in tuple_add(self._cardinal_directions(),self._diagonal_directions()): 
            # move = (coord,tuple(map(sum,zip(coord,direction))),piece)  # Get destination
            move = (coord, tuple_add(coord,direction),piece)

            if self._valid_destination(move,first_player):
                moves.append(move)

        return moves

    def _queen_moves(self, loc_piece,first_player):
        coord = loc_piece[0]
        piece = loc_piece[1]


        moves = []

        for direction in tuple_add(self._cardinal_directions(),self._diagonal_directions()): 

            move = (coord,coord,piece)

            while(True):

                # move = (coord,tuple(map(sum,zip(move[1],direction))),piece)  # Get destination
                move = (coord, tuple_add(move[1],direction),piece)

                if self._valid_destination(move,first_player):
                    moves.append(move)

                    if self._space_occupied_by_opponent(move[1],first_player):
                        break

                else: 
                    break

        return moves

    def _rook_moves(self, loc_piece,first_player):
        coord = loc_piece[0]
        piece = loc_piece[1]

        moves = []

        for direction in self._cardinal_directions(): 

            move = ( coord,coord,piece)

            while(True):

                # move = (coord,tuple(map(sum,zip(move[1],direction))),piece)  # Get destination
                move = (coord, tuple_add(move[1],direction),piece)

                if self._valid_destination(move,first_player):
                    moves.append(move)

                    if self._space_occupied_by_opponent(move[1],first_player):
                        break

                else: 
                    break

        return moves

    def _bishop_moves(self,loc_piece,first_player):
        coord = loc_piece[0]
        piece = loc_piece[1]

        moves = []

        for direction in self._diagonal_directions(): 
            move =( coord,coord,piece)

            while(True):

                move = (coord, tuple_add(move[1],direction),piece)

                if self._valid_destination(move,first_player):
                    moves.append(move)

                    if self._space_occupied_by_opponent(move[1],first_player):
                        break

                else: 
                    break

        return moves

    def _knight_moves(self, loc_piece,first_player):
        coord = loc_piece[0]
        piece = loc_piece[1]

        moves = []

        for direction in self._knight_directions(): 
            move = (coord, tuple_add(coord,direction),piece)
            

            if self._valid_destination(move,first_player):
                moves.append(move)

        return moves

    # TODO pawn moves are still probably fucked up
    def _pawn_moves(self,loc_piece,first_player): 
        coord = loc_piece[0]
        piece = loc_piece[1]

        moves = []

        if first_player: # white

            if coord[1] + 1 == self.board_dimensions[1]: # If pawn would reach end of board by moving up, always promote to queen
    
                piece = 1 # White Queen

            move = tuple((coord, tuple_add(coord,(0,1)) ,piece)) # move up one space
            if self._in_board(move[1]) and self._space_empty(move[1]) and not self._move_into_check(move,first_player):
                
                moves.append(move)

                if coord[1] == 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple((coord,tuple_add(coord,(0,2)),piece))
                    if self._in_board(move[1]) and self._space_empty(move[1]) and not self._move_into_check(move,first_player):
                        moves.append(move)
                        
            
            move = tuple((coord,tuple_add(coord,(-1,1)),piece)) # capture up left
            if self._in_board(move[1]) and self._space_occupied_by_opponent(move[1],first_player) and not self._move_into_check(move,first_player) :
                moves.append(move)

            move = tuple((coord,tuple_add(coord,(1,1)),piece)) # capture up right
            if self._in_board(move[1]) and self._space_occupied_by_opponent(move[1],first_player) and not self._move_into_check(move,first_player) :
                moves.append(move)

        else:   # black

            if coord[1] - 1 == 0: # If pawn would reach end of board by moving up, always promote to queen
    
                piece = 7 # Black queen

            move = tuple((coord,tuple_add(coord,(0,-1)),piece)) # move down one space
            if self._in_board(move[1]) and self._space_empty(move[1]) and not self._move_into_check(move,first_player) :
                moves.append(move)

                if coord[1] == self.board_dimensions[1] - 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple((coord,tuple_add(coord,(0,-2)),piece))
                    if self._in_board(move[1]) and self._space_empty(move[1]) and not self._move_into_check(move,first_player) :
                        moves.append(move)
                        
            move = tuple((coord,tuple_add(coord,(-1,-1)),piece)) # capture down left
            if self._in_board(move[1]) and self._space_occupied_by_opponent(move[1],first_player) and not self._move_into_check(move,first_player):
                moves.append(move)

            move = tuple((coord,tuple_add(coord,(1,-1)),piece)) # capture down right
            if self._in_board(move[1]) and self._space_occupied_by_opponent(move[1],first_player) and not self._move_into_check(move,first_player):
                moves.append(move)

        return moves

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

        locations_pieces = []
        moves = []

        if first_player: # white player

            for loc_piece in self.items(): 
                if loc_piece[1] <= 5: #if piece is white
                
                    locations_pieces.append(loc_piece)

        else:   # black player
             for loc_piece in self.items(): 
                if loc_piece[1] > 5: #if piece is black
                    locations_pieces.append(loc_piece)


        for loc_piece in locations_pieces:
            # moves.append(self._get_piece_moves(loc_piece,first_player))
            moves += self._get_piece_moves(loc_piece,first_player)

        return moves
