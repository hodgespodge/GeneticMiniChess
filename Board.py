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
        return Board()

    def get_board_heuristic(self):
        return 0

    def valid_destination(self,move):

        coord = move[0]

        if coord[0] > self.board_dimensions[0] or coord[0] < 0:     # out of width bounds
            return False
        elif coord[1] > self.board_dimensions[1] or coord[1] < 1:   # out of height bounds
            return False
        elif (self.data[coord] > 5 and self.first_player) or (self.data[coord] <= 5 and not self.first_player): # make sure tile is empty or occupied by other player
            return False

        return True

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

        if self.first_player and coord[1] == 0: #has the white pawn moved?
            pass

        
        elif not self.first_player and coord[1] == self.board_dimensions[1]: #has the black pawn moved?
            pass
            
            
                   

    def get_piece_moves(self,move): # moves are always tuple(tuple(x,y),piece)

        coord = move[0]
        piece = move[1]

        moves = []

        if self.first_player: 
            if piece == 0:      #king

                moves += self.king_moves(move)

            elif piece == 1:    #queen


                pass   
            elif piece == 2:    #rook
                pass
            elif piece == 3:    #bishop
                pass
            elif piece == 4:    #knight
                pass
            elif piece == 5:    #pawn
                pass
            else:
                print("error: player id doesn't match piece.")

        else:

            if piece == 6:      #king
                pass
            elif piece == 7:    #queen
                pass   
            elif piece == 8:    #rook
                pass
            elif piece == 9:    #bishop
                pass
            elif piece == 10:    #knight
                pass
            elif piece == 11:    #pawn
                pass
            else:
                print("error: player id doesn't match piece.")




        return 0


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
