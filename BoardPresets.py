from Board import Board, tuple_sub

# ["white_king","white_queen","white_rook","white_bishop","white_knight","white_pawn","black_king","black_queen","black_rook","black_bishop","black_knight","black_pawn"]


def silverman4x4():

    board_dimensions = (4,4) # 4x4 game
    
    board = Board(board_dimensions= tuple_sub(board_dimensions,(1,1))) # dimensions is 0 indexed

    # Row 0
    board[(0,0)] = 2 # white_rook
    board[(1,0)] = 1 # white_queen
    board[(2,0)] = 0 # white_king
    board[(3,0)] = 2 # white_rook

    # Row 1
    board[(0,1)] = 5 # white_pawn
    board[(1,1)] = 5 # white_pawn
    board[(2,1)] = 5 # white_pawn
    board[(3,1)] = 5 # white_pawn

    # Row 2
    board[(0,2)] = 11 # black_pawn
    board[(1,2)] = 11 # black_pawn
    board[(2,2)] = 11 # black_pawn
    board[(3,2)] = 11 # black_pawn

    # Row 3
    board[(0,3)] = 8 # black_rook
    board[(1,3)] = 7 # black_queen
    board[(2,3)] = 6 # black_king
    board[(3,3)] = 8 # black_rook
 
    return board

def silverman4x5():

    board_dimensions = (4,5) # 4x5 game

    board = Board(board_dimensions=tuple_sub(board_dimensions,(1,1))) # dimensions is 0 indexed

    # Row 0
    board[(0,0)] = 2 # white_rook
    board[(1,0)] = 1 # white_queen
    board[(2,0)] = 0 # white_king
    board[(3,0)] = 2 # white_rook

    # Row 1
    board[(0,1)] = 5 # white_pawn
    board[(1,1)] = 5 # white_pawn
    board[(2,1)] = 5 # white_pawn
    board[(3,1)] = 5 # white_pawn

    # Row 3
    board[(0,3)] = 11 # black_pawn
    board[(1,3)] = 11 # black_pawn
    board[(2,3)] = 11 # black_pawn
    board[(3,3)] = 11 # black_pawn

    # Row 4
    board[(0,4)] = 8 # black_rook
    board[(1,4)] = 7 # black_queen
    board[(2,4)] = 6 # black_king
    board[(3,4)] = 8 # black_rook
 
    return board

def gardner():

    board_dimensions = (5,5) # 5x5 game

    board = Board(board_dimensions=tuple_sub(board_dimensions,(1,1))) # dimensions is 0 indexed

    # Row 0
    board[(0,0)] = 2 # white_rook
    board[(1,0)] = 4 # white_knight
    board[(2,0)] = 3 # white_bishop
    board[(3,0)] = 1 # white_queen
    board[(4,0)] = 0 # white_king

    # Row 1
    board[(0,1)] = 5 # white_pawn
    board[(1,1)] = 5 # white_pawn
    board[(2,1)] = 5 # white_pawn
    board[(3,1)] = 5 # white_pawn
    board[(4,1)] = 5 # white_pawn

    # Row 3
    board[(0,3)] = 11 # black_pawn
    board[(1,3)] = 11 # black_pawn
    board[(2,3)] = 11 # black_pawn
    board[(3,3)] = 11 # black_pawn
    board[(4,3)] = 11 # black_pawn

    # Row 4
    board[(0,4)] = 8 # black_rook
    board[(1,4)] = 10 # black_knight
    board[(2,4)] = 9 # black_bishop
    board[(3,4)] = 7 # black_queen
    board[(4,4)] = 6 # black_king
 
    return board

def baby_chess():

    board_dimensions = (5,5) # 5x5 game

    board = Board(board_dimensions=tuple_sub(board_dimensions,(1,1))) # dimensions is 0 indexed

    # Row 0
    board[(0,0)] = 2 # white_rook
    board[(1,0)] = 4 # white_knight
    board[(2,0)] = 3 # white_bishop
    board[(3,0)] = 1 # white_queen
    board[(4,0)] = 0 # white_king

    # Row 1
    board[(0,1)] = 5 # white_pawn
    board[(1,1)] = 5 # white_pawn
    board[(2,1)] = 5 # white_pawn
    board[(3,1)] = 5 # white_pawn
    board[(4,1)] = 5 # white_pawn

    # Row 3
    board[(0,3)] = 11 # black_pawn
    board[(1,3)] = 11 # black_pawn
    board[(2,3)] = 11 # black_pawn
    board[(3,3)] = 11 # black_pawn
    board[(4,3)] = 11 # black_pawn

    # Row 4
    board[(0,4)] = 6 # black_king
    board[(1,4)] = 7 # black_queen
    board[(2,4)] = 9 # black_bishop
    board[(3,4)] = 10 # black_knight
    board[(4,4)] = 8 # black_rook
 
    return board