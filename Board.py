from collections import UserDict
from copy import deepcopy
from operator import add, sub
from math import pow


def print_board(board):
    board_dimensions = board.board_dimensions
    for y in range(board_dimensions[1],-1,-1):
        for x in range(board_dimensions[0]+1):
            piece = (board.get((x,y),None))

            if (x+y)%2 == 0:
                square_color = 44
            else:
                square_color = 45

            if piece != None:

                if piece > 5:
                    player_color = 0
                else:
                    player_color = 100
                tile = '\x1b[3;{0};{1}m'.format(player_color, square_color)
                tile += piece_unicode_list()[piece]+" "+'\x1b[0m'
                # print('\x1b[6;30;42m'+piece_unicode_list()[piece]+" "+'\x1b[0m',end="")
                print(tile,end="")
            else:

                tile = '\x1b[3;{0};{1}m'.format(0, square_color)
                tile += "  "+'\x1b[0m'

                print(tile,end="")
                # print('\x1b[6;30;42m'+" "+'\x1b[0m',end=" ")
        print()

def get_english_notation(move):
    starting_coords = move[0]
    ending_coords = move[1]
    piece = move[2]
    
    out = alphabet()[starting_coords[0]]+str(starting_coords[1]+1) 
    out += piece_unicode_list()[piece] + " "
    out += alphabet()[ending_coords[0]]+str(ending_coords[1]+1)

    return out

def piece_unicode_list(): # pieces are numbered 0-11
    return ["\u2654","\u2655","\u2656","\u2657","\u2658","\u2659","\u265A","\u265B","\u265C","\u265D","\u265E","\u265F"]


def alphabet():
    return ["a","b","c","d","e","f","g","h","i","j"]

def piece_list(): # pieces are numbered 0-11
    return ["white_king","white_queen","white_rook","white_bishop","white_knight","white_pawn","black_king","black_queen","black_rook","black_bishop","black_knight","black_pawn"]
def white_piece_list():
    return ["white_king","white_queen","white_rook","white_bishop","white_knight","white_pawn"]
def black_piece_list():
    return ["black_king","black_queen","black_rook","black_bishop","black_knight","black_pawn"]

def tuple_add(a,b):
    return tuple(map(add,a,b))

def tuple_sub(a,b):
    return tuple(map(sub,a,b))

def get_new_board_after_move(board,move,first_player):

    new_board = deepcopy(board) 
    new_board[move[1]] = move[2] # replace dict value at key = coord with new piece
    del new_board[move[0]]       # Piece moved so delete old key/value 

    return new_board

def game_over(board):

    if not ( 0 in board.values()): # is white king missing?
        return True, -1 # black wins
    elif not ( 6 in board.values()): # is black king missing?
        return True, 1 # white wins
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
    def __init__(self,board_dimensions) -> None:
        # self.hash = self.get_board_hash()
        self.board_dimensions = board_dimensions #Tuple(width,heigh)
  
    def _hash_(self):
        # i = 0
        # hash = 0

        items = sorted(self.items(), key = lambda x : x[0][0] + 12*x[0][1])

        return hash(frozenset(items))

        # for item in items:
        #     x = item[0][0]
        #     y = item[0][1]
        #     p = item[1]

        #     hash += pow((x+1) * 13 , y) + p

        #     i += 1
        # hash = hash // i

        # return int(hash)

    def get_board_hash(self,first_player):

        items = sorted(self.items(), key = lambda x : x[0][0] + 12*x[0][1])

        return hash(frozenset(items))

        # if first_player:

        #     return self._hash_() 
        # else:
        #     return self._hash_() * -1

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

        for direction in tuple_add(self._cardinal_directions(),self._diagonal_directions()): 
            move = (coord,tuple(map(sum,zip(coord,direction))),piece)  # Get destination

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

                move = (coord,tuple(map(sum,zip(move[1],direction))),piece)  # Get destination

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

                move = (coord,tuple(map(sum,zip(move[1],direction))),piece)  # Get destination

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

                move = (coord,tuple(map(sum,zip(move[1],direction))),piece)  # Get destination

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
            move = (coord,tuple(map(sum,zip(coord,direction))),piece)  # Get destination

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
            if self._in_board(move[1]) and self._space_empty(move[1]):
                
                moves.append(move)

                if coord[1] == 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple((coord,tuple_add(coord,(0,2)),piece))
                    if self._in_board(move[1]) and self._space_empty(move[1]):
                        moves.append(move)
                        
            
            move = tuple((coord,tuple_add(coord,(-1,1)),piece)) # capture up left
            if self._in_board(move[1]) and self._space_occupied_by_opponent(move[1],first_player) :
                moves.append(move)

            move = tuple((coord,tuple_add(coord,(1,1)),piece)) # capture up right
            if self._in_board(move[1]) and self._space_occupied_by_opponent(move[1],first_player) :
                moves.append(move)

        else:   # black

            if coord[1] - 1 == 0: # If pawn would reach end of board by moving up, always promote to queen
    
                piece = 7 # Black queen

            move = tuple((coord,tuple_add(coord,(0,-1)),piece)) # move down one space
            if self._in_board(move[1]) and self._space_empty(move[1]) :
                moves.append(move)

                if coord[1] == self.board_dimensions[1] - 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple((coord,tuple_add(coord,(0,-2)),piece))
                    if self._in_board(move[1]) and self._space_empty(move[1]) :
                        moves.append(move)
                        
            move = tuple((coord,tuple_add(coord,(-1,-1)),piece)) # capture down left
            if self._in_board(move[1]) and self._space_occupied_by_opponent(move[1],first_player):
                moves.append(move)

            move = tuple((coord,tuple_add(coord,(1,-1)),piece)) # capture down right
            if self._in_board(move[1]) and self._space_occupied_by_opponent(move[1],first_player):
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
