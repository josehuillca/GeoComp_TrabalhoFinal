class Node:
    #__slots__ = ("nw", "ne", "sw", "se", "val", "bounds")

    def __init__(self, bounds, points, depth=0, parent=None):
        """
        Creates a node.
        bounds: type(Rect)
        points: List[Point]
        depth: int
        parent: Node
        """
        self.nw, self.ne, self.sw, self.se = None, None, None, None
        self.points = points
        self.depth = depth
        self.bounds = bounds
        self.parent = parent

    def __str__(self):
        return "<{}, {}>".format(self.points, self.bounds)

    @property
    def sons(self):
        """
        @return: tuple of sons (nw,ne,sw,se)
        """
        return self.nw, self.ne, self.sw, self.se

    @property
    def leaf(self):
        """
        @return: True if not any(self.sons)
        """
        return not any(self.sons)