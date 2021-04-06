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

    def in_board(self,coord):

        if coord[0] > self.board_dimensions[0] or coord[0] < 0:     # out of width bounds
            return False
        elif coord[1] > self.board_dimensions[1] or coord[1] < 1:   # out of height bounds
            return False
        else:
            return True

    def space_occupied_by_opponent(self,coord):
        return (self.data[coord] > 5 and self.first_player) or (self.data[coord] <= 5 and not self.first_player)

    def space_empty(self,coord):
        return not self.get(coord,-1) >= 0  #dict.get('key',default)

    def valid_destination(self,move):

        coord = move[0]
        return self.in_board(coord) and (self.space_empty(coord) or self.space_occupied_by_opponent(coord))
        
    def cardinal_directions(self):
        return ((0,1),(1,0),(0,-1),(-1,0))  # Up,Right,Down,Left

    def diagonal_directions(self):
        return ((1,1),(1,-1),(-1,-1),(-1,1)) # Up-Right, Down-Right, Down-Left, Up-Left

    def knight_directions(self):
        return ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))

    def king_moves(self, move):
        coord = move[0]
        piece = move[1]

        moves = []

        for direction in self.cardinal_directions()+self.diagonal_directions(): 
            move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

            if self.valid_destination(move):
                moves.append(move)

        return moves

    def queen_moves(self, move):
        coord = move[0]
        piece = move[1]


        moves = []

        for direction in self.cardinal_directions()+self.diagonal_directions(): 

            while(True):

                move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

                if self.valid_destination(move):
                    moves.append(move)

                else: 
                    break

        return moves

    def rook_moves(self, move):
        coord = move[0]
        piece = move[1]

        moves = []

        for direction in self.cardinal_directions(): 

            while(True):

                move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

                if self.valid_destination(move):
                    moves.append(move)

                else: 
                    break

        return moves

    def bishop_moves(self,move):
        coord = move[0]
        piece = move[1]

        moves = []

        for direction in self.diagonal_directions(): 

            while(True):

                move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

                if self.valid_destination(move):
                    moves.append(move)

                else: 
                    break

        return moves

    def knight_moves(self, move):
            coord = move[0]
            piece = move[1]

            moves = []

            for direction in self.knight_directions(): 
                move = tuple(map(sum,zip(coord,direction)),piece)  # Get destination

                if self.valid_destination(move):
                    moves.append(move)

            return moves

    def pawn_moves(self,move):
        coord = move[0]
        piece = move[1]

        moves = []

        if self.first_player: # white

            move = tuple(coord+(0,1),piece) # move up one space
            if self.space_empty(move[0]) and self.in_board(move[0]):
                moves.append(move)

                if coord[1] == 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple(coord+(0,2))
                    if self.space_empty(move[0]) and self.in_board(move[0]):
                        moves.append(move)
                        
            
            move = tuple(coord+(-1,1),piece) # capture up left
            if self.space_occupied_by_opponent(move[0]) and self.in_board(move[0]):
                moves.append(move)

            move = tuple(coord+ (1,1),piece) # capture up right
            if self.space_occupied_by_opponent(move[0]) and self.in_board(move[0]):
                moves.append(move)

        else:   # black

            move = tuple(coord+(0,-1),piece) # move down one space
            if self.space_empty(move[0]) and self.in_board(move[0]):
                moves.append(move)

                if coord[1] == self.board_dimensions - 1: # Pawn's first move can be 2 spaces if both unoccupied
                    move = tuple(coord+(0,-2))
                    if self.space_empty(move[0]) and self.in_board(move[0]):
                        moves.append(move)
                        
            move = tuple(coord+(-1,-1),piece) # capture down left
            if self.space_occupied_by_opponent(move[0]) and self.in_board(move[0]):
                moves.append(move)

            move = tuple(coord+ (1,-1),piece) # capture down right
            if self.space_occupied_by_opponent(move[0]) and self.in_board(move[0]):
                moves.append(move)


    def get_piece_moves(self,move): # moves are always tuple(tuple(x,y),piece)

        piece = move[1]


        if self.first_player: 
            if piece == 0:      #king

                return self.king_moves(move)

            elif piece == 1:    #queen
                return self.queen_moves(move)

            elif piece == 2:    #rook

                return self.rook_moves(move)

            elif piece == 3:    #bishop
                return self.bishop_moves(move)

            elif piece == 4:    #knight
                return self.knight_moves(move)

            elif piece == 5:    #pawn
                return self.pawn_moves(move)
                
            else:
                print("error: player id doesn't match piece.")

        else:

            if piece == 6:      #king
                return self.king_moves(move)

            elif piece == 7:    #queen
                return self.queen_moves(move)
            elif piece == 8:    #rook
                return self.rook_moves(move)

            elif piece == 9:    #bishop
                return self.bishop_moves(move)

            elif piece == 10:    #knight
                return self.knight_moves(move)

            elif piece == 11:    #pawn
                return self.pawn_moves(move)

            else:
                print("error: player id doesn't match piece.")


    def get_all_moves(self):

        white_pieces,black_pieces = [],[]

        for piece in self.data.items: 
            if piece[1] < 5: #if piece is white
                white_pieces.append(piece)
            else:   #else piece black
                black_pieces.append(piece)

        if self.first_player:
            for piece in white_pieces:
                pass
        else:
            for piece in black_pieces:
                pass
            
        




class MapOfBoards(UserDict):
    def __init__(self,) -> None:
        pass
