class Node():
    def __init__(self, x0, y0, w, h, points, depth=0, parent=None):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.children = []
        self.depth = depth
        self.parent = parent

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_points(self):
        return self.points

    @property
    def leaf(self):
        """
        @return: True if not any(self.sons)
        """
        return len(self.children)==0
    
    def __str__(self):
        x0 = '\t x0: ' + str(self.x0) + '\n'
        y0 = '\t y0: ' + str(self.y0) + '\n'
        w = '\t width: ' + str(self.width) + '\n'
        h = '\t height: ' + str(self.height) + '\n'
        points = [str(p) for p in self.points]
        points_ = '\t points: ' + ','.join(points) + '\n'
        return x0 + y0 + w + h + points_ 