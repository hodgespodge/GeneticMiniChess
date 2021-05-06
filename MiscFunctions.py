from operator import add, sub

'''
Author Samuel Hodges

'''


def print_board(board):
    board_dimensions = board.board_dimensions
    for y in range(board_dimensions[1],-1,-1):
        
        print(y + 1,end=" ")

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

    print("  ",end="")
    for x in range(board_dimensions[0]+1):
        print(alphabet()[x],end=" ")
    print()
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
def reverse_alphabet():
    return {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8,"j":9}

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