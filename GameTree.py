class StateNode():

    def __init__(self) -> None:
        
        self.state_hash = None #int
        self.children = None #list of statenodes
        self.min_max_value = None #float
        self.current_depth = None #int
        
class GameTree():

    def __init__(self) -> None:
        self.root_node = None #root node
        self.target_depth = None #int
        