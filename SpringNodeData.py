class NodeType:
    Inner, Boundary, Locked = range(3)

class SpringNode:
    def __init__(self, position, gradient, boundaryCond):
        self.position = position
        self.gradient = gradient
        self.boundaryCond = boundaryCond
