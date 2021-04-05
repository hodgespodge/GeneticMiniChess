from collections import UserDict


def piece_list():
    return ["king","queen","rook","bishop","knight","pawn"]


class Board(UserDict):
    def __init__(self) -> None:
        self.hash = self.get_hash()
        self.board_heuristic = self.get_board_heuristic()

    def get_hash(self):
        return None

    def get_new_board_after_move(self,move):
        return Board()

    def get_board_heuristic(self):
        return 0
    


class MapOfBoards(UserDict):
    def __init__(self) -> None:
        pass

