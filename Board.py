from collections import UserDict


def piece_list(): # pieces are numbered 0-11
    return ["white_king","white_queen","white_rook","white_bishop","white_knight","white_pawn","black_king","black_queen","black_rook","black_bishop","black_knight","black_pawn"]
def white_piece_list():
    return ["white_king","white_queen","white_rook","white_bishop","white_knight","white_pawn"]
def black_piece_list():
    return ["black_king","black_queen","black_rook","black_bishop","black_knight","black_pawn"]


class Board(UserDict):
    def __init__(self,first_player,board_dimensions) -> None:
        self.hash = self.get_hash_of_board()
        self.first_player = first_player
        self.board_dimensions = board_dimensions #Tuple(width,heigh)
  
    def get_hash_of_board(self):
        return hash(self)

    def get_new_board_after_move(self,move):
        return Board(not self.first_player,self.board_dimensions)

    def get_board_heuristic(self):
        return 0

    def _in_board(self,coord):

        if coord[0] > self.board_dimensions[0] or coord[0] < 0:     # out of width bounds
            return False
        elif coord[1] > self.board_dimensions[1] or coord[1] < 1:   # out of height bounds
            return False
        else:
            return True

    def _space_occupied_by_opponent(self,coord):
        return (self.data[coord] > 5 and self.first_player) or (self.data[coord] <= 5 and not self.first_player)

    def _space_empty(self,coord):
        return not self.get(coord,-1) >= 0  #dict.get('key',default)

    def _valid_destination(self,move):

        coord = move[0]
        return self._in_board(coord) and (self._space_empty(coord) or self._space_occupied_by_opponent(coord))
        
    def _cardinal_directions(self):
        return ((0,1),(1,0),(0,-1),(-1,0))  # Up,Right,Down,Left

    def _diagonal_directions(self):
        return ((1,1),(1,-1),(-1,-1),(-1,1)) # Up-Right, Down-Right, Down-Left, Up-Left

    def _knight_directions(self):
        return ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))

    def _king_moves(self, move):
        coord = move[0]
        piece = move[1]

        moves = []

        for direction in self._cardinal_directions()+self._diagonal_directions(): 
            move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

            if self._valid_destination(move):
                moves.append(move)

        return moves

    def _queen_moves(self, move):
        coord = move[0]
        piece = move[1]


        moves = []

        for direction in self._cardinal_directions()+self._diagonal_directions(): 

            while(True):

                move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

                if self._valid_destination(move):
                    moves.append(move)

                else: 
                    break

        return moves

    def _rook_moves(self, move):
        coord = move[0]
        piece = move[1]

        moves = []

        for direction in self._cardinal_directions(): 

            while(True):

                move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

                if self._valid_destination(move):
                    moves.append(move)

                else: 
                    break

        return moves

    def _bishop_moves(self,move):
        coord = move[0]
        piece = move[1]

        moves = []

        for direction in self._diagonal_directions(): 

            while(True):

                move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

                if self._valid_destination(move):
                    moves.append(move)

                else: 
                    break

        return moves

    def _knight_moves(self, move):
            coord = move[0]
            piece = move[1]

            moves = []

            for direction in self._knight_directions(): 
                move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

                if self._valid_destination(move):
                    moves.append(move)

            return moves

    def _pawn_moves(self,move):
        coord = move[0]
        piece = move[1]

        moves = []

        if self.first_player: # white

            move = tuple(coord+(0,1),piece) # move up one space
            if self._space_empty(move[0]) and self._in_board(move[0]):
                moves.append(move)

                if coord[1] == 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple(coord+(0,2))
                    if self._space_empty(move[0]) and self._in_board(move[0]):
                        moves.append(move)
                        
            
            move = tuple(coord+(-1,1),piece) # capture up left
            if self._space_occupied_by_opponent(move[0]) and self._in_board(move[0]):
                moves.append(move)

            move = tuple(coord+ (1,1),piece) # capture up right
            if self._space_occupied_by_opponent(move[0]) and self._in_board(move[0]):
                moves.append(move)

        else:   # black

            move = tuple(coord+(0,-1),piece) # move down one space
            if self._space_empty(move[0]) and self._in_board(move[0]):
                moves.append(move)

                if coord[1] == self.board_dimensions - 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple(coord+(0,-2))
                    if self._space_empty(move[0]) and self._in_board(move[0]):
                        moves.append(move)
                        
            move = tuple(coord+(-1,-1),piece) # capture down left
            if self._space_occupied_by_opponent(move[0]) and self._in_board(move[0]):
                moves.append(move)

            move = tuple(coord+ (1,-1),piece) # capture down right
            if self._space_occupied_by_opponent(move[0]) and self._in_board(move[0]):
                moves.append(move)


    def _get_piece_moves(self,move): # moves are always tuple(tuple(x,y),piece)

        piece = move[1]


        if self.first_player: 
            if piece == 0:      #king

                return self._king_moves(move)

            elif piece == 1:    #queen
                return self._queen_moves(move)

            elif piece == 2:    #rook

                return self._rook_moves(move)

            elif piece == 3:    #bishop
                return self._bishop_moves(move)

            elif piece == 4:    #knight
                return self._knight_moves(move)

            elif piece == 5:    #pawn
                return self._pawn_moves(move)
                
            else:
                print("error: player id doesn't match piece.")

        else:

            if piece == 6:      #king
                return self._king_moves(move)

            elif piece == 7:    #queen
                return self._queen_moves(move)
            elif piece == 8:    #rook
                return self._rook_moves(move)

            elif piece == 9:    #bishop
                return self._bishop_moves(move)

            elif piece == 10:    #knight
                return self._knight_moves(move)

            elif piece == 11:    #pawn
                return self._pawn_moves(move)

            else:
                print("error: player id doesn't match piece.")


    def get_all_moves(self):

        player_pieces = []
        moves = []

        if self.first_player: # white player

            for piece in self.data.items: 
                if piece[1] <= 5: #if piece is white
                    player_pieces.append(piece)

        else:   # black player
             for piece in self.data.items: 
                if piece[1] > 5: #if piece is black
                    player_pieces.append(piece)

        for piece in player_pieces:
            moves.append(self._get_piece_moves(piece))

class MapOfBoards():
    def __init__(self) -> None:
        self.boards = {}
    
    def add_board(self,board):
        board_hash = board.get_hash_of_board()

        self.boards[board_hash] = board
        return board_hash


