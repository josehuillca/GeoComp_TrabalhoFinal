import matplotlib.pyplot as plt
import matplotlib.patches as patches

from quadtree.node import Node
from quadtree.point import Point
from quadtree.utils import recursive_subdivide, contains, find_children,leaf_nodes, get_neighbor_of_greater_or_equal_size,Direction,has_to_split, DEBUG_MODE

class QTree():
    def __init__(self, k, w, h, points):
        # k: max points in Node
        # w: width
        # h: height
        # points: List[Point]
        self.w = w
        self.h = h
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
        L = leaf_nodes(self.root)
        print(len(L))
        while len(L)>0:
            # Remove a leaf u from L
            u = L.pop(0)
            # Neighbors of u
            NL = [
                get_neighbor_of_greater_or_equal_size(u, Direction.N),
                get_neighbor_of_greater_or_equal_size(u, Direction.S),
                get_neighbor_of_greater_or_equal_size(u, Direction.W),
                get_neighbor_of_greater_or_equal_size(u, Direction.E)
            ]
            split_, NL_depths = has_to_split(u, NL)
            if split_:
                # Add four children(nw,sw, ne,se) to u in 'self' & update their object contents
                w_ = float(u.width/2)
                h_ = float(u.height/2)
                p = []
                nw = Node(u.x0, u.y0, w_, h_, p, depth=u.depth+1, parent=u)
                sw = Node(u.x0, u.y0+h_, w_, h_, p, depth=u.depth+1, parent=u)
                ne = Node(u.x0 + w_, u.y0, w_, h_, p, depth=u.depth+1, parent=u)
                se = Node(u.x0+w_, u.y0+h_, w_, h_, p, depth=u.depth+1, parent=u)
                u.children = [nw, sw, ne, se]
                
                # Insert four children(nw,sw, ne,se) into L
                L.append(nw)
                L.append(sw)
                L.append(ne)
                L.append(se) 
                # Check if nw,sw, ne,se have neighbors that should split & add them to L
                for i, d in enumerate(NL_depths):
                    if u.depth<(d-2) and False: # Ainda com testes
                        uu = NL[i]
                        NL_uu = [
                            get_neighbor_of_greater_or_equal_size(uu, Direction.N),
                            get_neighbor_of_greater_or_equal_size(uu, Direction.S),
                            get_neighbor_of_greater_or_equal_size(uu, Direction.W),
                            get_neighbor_of_greater_or_equal_size(uu, Direction.E)
                        ]
                        split_2, asdf = has_to_split(uu, NL_uu)
                        print(uu.depth, asdf)
                        if split_2:
                            w_ = float(uu.width/2)
                            h_ = float(uu.height/2)
                            p = []
                            nw_ = Node(uu.x0, uu.y0, w_, h_, p, depth=uu.depth+1, parent=uu)
                            sw_ = Node(uu.x0, uu.y0+h_, w_, h_, p, depth=uu.depth+1, parent=uu)
                            ne_ = Node(uu.x0 + w_, uu.y0, w_, h_, p, depth=uu.depth+1, parent=uu)
                            se_ = Node(uu.x0+w_, uu.y0+h_, w_, h_, p, depth=uu.depth+1, parent=uu)
                            uu.children = [nw_, sw_, ne_, se_]
                            
                            print(u.depth, d, uu)
                            # Insert four children(nw,sw, ne,se) into L
                            L.append(nw_)
                            L.append(sw_)
                            L.append(ne_)
                            L.append(se_)

                if DEBUG_MODE:
                    uu = get_neighbor_of_greater_or_equal_size(se, Direction.E)
                    print(uu)
                pass
            

        pass
    
    def draw(self, title= "Quadtree"):
        _ = plt.figure(figsize=(12, 8))
        # Change init coordenada(0,0) in Top-Left
        ax = plt.subplot()
        ax.set_xlim(0, self.w)
        ax.set_ylim(self.h, 0)

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
