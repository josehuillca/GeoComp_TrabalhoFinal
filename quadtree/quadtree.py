import matplotlib.pyplot as plt
import matplotlib.patches as patches

from quadtree.node import Node
from quadtree.point import Point
from quadtree.utils import recursive_subdivide, contains, find_children

class QTree():
    def __init__(self, k, w, h, points):
        # k: max points in Node
        # w: width
        # h: height
        # points: List[Point]
        self.threshold = k
        self.points = points
        self.root = Node(0, 0, w, h, self.points)

    def add_point(self, x, y):
        self.points.append(Point(x, y))
    
    def get_points(self):
        return self.points
    
    def subdivide(self):
        recursive_subdivide(self.root, self.threshold)

    def balanced(self):
        pass
    
    def draw(self, w, h, title= "Quadtree"):
        _ = plt.figure(figsize=(12, 8))
        # Change init coordenada(0,0) in Top-Left
        ax = plt.subplot()
        ax.set_xlim(0, w)
        ax.set_ylim(h, 0)

        plt.title(title)
        c = find_children(self.root)
        print("Number of segments: %d" %len(c))
        areas = set()
        for el in c:
            areas.add(el.width*el.height) # area=lado*lado
        print("Minimum segment area: %.3f units" %min(areas))

        # Plot Rectangles
        for n in c:
            plt.gcf().gca().add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        
        # plots the points as red dots
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]
        plt.plot(x, y, 'ro') 
        plt.show()
        return
