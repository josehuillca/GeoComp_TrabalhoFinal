import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import Delaunay
from quadtree.point import Point
from quadtree.utils import find_children, get_neighbor_of_greater_or_equal_size, Direction, deeper, DEBUG_MODE, is_inside_polygon, node_is_inside_polygon, contains

class Mesh():
    def __init__(self, qtree):
        self.qtree = qtree
        self.triangles = []
        self.pts_inside_contour = []
        self.nodes_inside_polygon = []

    def mesh_generation(self):
        c = find_children(self.qtree.root)
        
        for u in c:
            d = u.depth
            dN = deeper(get_neighbor_of_greater_or_equal_size(u, Direction.N))
            dS = deeper(get_neighbor_of_greater_or_equal_size(u, Direction.S))
            dW = deeper(get_neighbor_of_greater_or_equal_size(u, Direction.W))
            dE = deeper(get_neighbor_of_greater_or_equal_size(u, Direction.E))

            x, y = u.x0, u.y0
            w_, h_ = u.width, u.height
            #print(d, dN, dS, dW, dE)
            # Padrao #1 -------------------------
            if d>=dN and d>=dS and d>=dW and d>=dE:
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x, y + h_])
                # triangle 2  
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x, y + h_])
            
            # Padrao #2 -------------------------
            if dW>d and d>=dN and d>=dS and d>=dE:
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x, y + h_/2.])
                # triangle 2  
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x, y + h_/2.])
                # triangle 3  
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x, y + h_])
                self.triangles.append([x, y + h_/2.])
            if dE>d and d>=dN and d>=dS and d>=dW:
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_/2.])
                # triangle 2  
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x, y + h_])
                # triangle 3  
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x, y + h_])
            if dN>d and d>=dW and d>=dS and d>=dE:
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x, y + h_])
                # triangle 2  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x, y + h_])
                # triangle 3  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_])
            if dS>d and d>=dN and d>=dW and d>=dE:
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_/2., y + h_])
                # triangle 2  
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_])
                # triangle 3  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x, y + h_])

            # Padrao #3 -------------------------
            if dN>d and dW>d and d>=dS and d>=dE: #----1
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x, y + h_/2.])
                # triangle 2  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_/2., y + h_/2.])
                self.triangles.append([x, y + h_/2.])
                # triangle 3  
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_/2.])
                self.triangles.append([x, y + h_])
                # triangle 4  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 5  
                self.triangles.append([x + w_/2., y + h_/2.])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x, y + h_])
                # triangle 6  
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_/2.])
            if dN>d and dE>d and d>=dS and d>=dW: #----2
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 2  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 3  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_/2.])
                # triangle 4  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y+ h_/2.])
                self.triangles.append([x, y + h_])
                # triangle 5  
                self.triangles.append([x, y + h_])
                self.triangles.append([x + w_/2., y+ h_/2.])
                self.triangles.append([x + w_, y + h_])
                # triangle 6  
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y+ h_/2.])
                self.triangles.append([x + w_, y + h_/2.])
            if dS>d and dE>d and d>=dW and d>=dN: #----3
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y + h_/2.])
                self.triangles.append([x, y + h_])
                # triangle 2 
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 3 
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 4 
                self.triangles.append([x + w_/2., y + h_/2.])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x, y + h_])
                # triangle 5
                self.triangles.append([x + w_/2., y + h_/2.])
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_])
                # triangle 5
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_])
            if dS>d and dW>d and d>=dN and d>=dE: #----4
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y + h_/2.])
                self.triangles.append([x, y + h_/2.])
                # triangle 2 
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 3 
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 4 
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 5
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 6
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x, y + h_])
                self.triangles.append([x, y + h_/2.])

            # Padrao #4 -------------------------
            if dW>d and dE>d and d>=dS and d>=dN:
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 2  
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 3  
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 4  
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x, y + h_])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 5  
                self.triangles.append([x, y + h_])
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 6  
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y + h_/2.])
            if dN>d and dS>d and d>=dW and d>=dE:
                # triangle 1  
                self.triangles.append([x, y + h_])
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 2  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 3  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 4  
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 5  
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x + w_/2., y + h_/2.])
                # triangle 6  
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x, y + h_])
                self.triangles.append([x + w_/2., y + h_/2.])

            # Padrao #5 -------------------------
            if dW>d and dN>d and dS>d and d>=dE:
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x, y + h_/2.])
                # triangle 2  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x, y + h_/2.])
                # triangle 3  
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x + w_/2., y])
                # triangle 4  
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x + w_, y])
                # triangle 5 
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x, y + h_])
            if dW>d and dN>d and dE>d and d>=dS:
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x, y + h_/2.])
                # triangle 2  
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y + h_/2.])
                # triangle 3  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_/2.])
                # triangle 4  
                self.triangles.append([x, y + h_])
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x + w_, y + h_/2.])
                # triangle 5  
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x, y + h_])
                self.triangles.append([x + w_, y + h_/2.])
            if dN>d and dE>d and dS>d and d>=dW:
                # triangle 1  
                self.triangles.append([x, y + h_])
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y + h_])
                # triangle 2  
                self.triangles.append([x, y])
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_/2., y + h_])
                # triangle 3  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_/2.])
                # triangle 4  
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y + h_/2.])
                # triangle 5  
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x + w_, y + h_/2.])
            if dW>d and dE>d and dS>d and d>=dN:
                # triangle 1  
                self.triangles.append([x, y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x, y + h_/2.])
                # triangle 2  
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x, y + h_/2.])
                # triangle 3  
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_])
                # triangle 4  
                self.triangles.append([x, y + h_])
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_])
                # triangle 5  
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_])

            # Padrao #6 -------------------------
            if dW>d and dN>d and dS>d and dE>d:
                # triangle 1  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x, y + h_/2.])
                self.triangles.append([x, y])
                # triangle 2  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x, y + h_/2.])
                # triangle 3  
                self.triangles.append([x + w_/2., y])
                self.triangles.append([x + w_, y])
                self.triangles.append([x + w_, y + h_/2.])
                # triangle 4  
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_, y + h_])
                self.triangles.append([x + w_/2., y + h_])
                # triangle 5  
                self.triangles.append([x + w_, y + h_/2.])
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x, y + h_/2.])
                # triangle 6  
                self.triangles.append([x + w_/2., y + h_])
                self.triangles.append([x, y + h_])
                self.triangles.append([x, y + h_/2.])
            
            else:
                if DEBUG_MODE:
                    print('warning! Not case found triangulation..')

    
    def mesh_generation_v2(self):
        c = find_children(self.qtree.root)

        xx_ = [point.x for point in self.qtree.points]
        yy_ = [point.y for point in self.qtree.points]
        polygon_ = list(zip(xx_, yy_))
        pt_countour = []

        for u in c:
            d = u.depth
            NN = get_neighbor_of_greater_or_equal_size(u, Direction.N)
            NS = get_neighbor_of_greater_or_equal_size(u, Direction.S)
            NW = get_neighbor_of_greater_or_equal_size(u, Direction.W)
            NE = get_neighbor_of_greater_or_equal_size(u, Direction.E)

            dN = deeper(NN)
            dS = deeper(NS)
            dW = deeper(NW)
            dE = deeper(NE)

            x, y = u.x0, u.y0
            w_, h_ = u.width, u.height

            if is_inside_polygon(polygon_, [x,y]) and is_inside_polygon(polygon_, [x+w_,y]) and is_inside_polygon(polygon_, [x,y+h_]) and is_inside_polygon(polygon_, [x+w_,y+h_]) and len(u.points)==0:
                self.nodes_inside_polygon.append(u)

                # Puntos de contorno
                if not node_is_inside_polygon(NN, polygon_):
                    pt_countour.append([x,y])
                    pt_countour.append([x+w_,y])
                if not node_is_inside_polygon(NS, polygon_):
                    pt_countour.append([x,y+h_])
                    pt_countour.append([x+w_,y+h_])
                if not node_is_inside_polygon(NW, polygon_):
                    pt_countour.append([x,y])
                    pt_countour.append([x,y+h_])
                if not node_is_inside_polygon(NE, polygon_):
                    pt_countour.append([x+w_,y])
                    pt_countour.append([x+w_,y+h_])

                #print(d, dN, dS, dW, dE)
                # Padrao #1 -------------------------
                if d>=dN and d>=dS and d>=dW and d>=dE:
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x, y + h_])
                    # triangle 2  
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x, y + h_])
                
                # Padrao #2 -------------------------
                if dW>d and d>=dN and d>=dS and d>=dE:
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 2  
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 3  
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x, y + h_/2.])
                if dE>d and d>=dN and d>=dS and d>=dW:
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_/2.])
                    # triangle 2  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x, y + h_])
                    # triangle 3  
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x, y + h_])
                if dN>d and d>=dW and d>=dS and d>=dE:
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x, y + h_])
                    # triangle 2  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x, y + h_])
                    # triangle 3  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_])
                if dS>d and d>=dN and d>=dW and d>=dE:
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_/2., y + h_])
                    # triangle 2  
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_])
                    # triangle 3  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x, y + h_])

                # Padrao #3 -------------------------
                if dN>d and dW>d and d>=dS and d>=dE: #----1
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 2  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 3  
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    self.triangles.append([x, y + h_])
                    # triangle 4  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 5  
                    self.triangles.append([x + w_/2., y + h_/2.])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x, y + h_])
                    # triangle 6  
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_/2.])
                if dN>d and dE>d and d>=dS and d>=dW: #----2
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 2  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 3  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_/2.])
                    # triangle 4  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y+ h_/2.])
                    self.triangles.append([x, y + h_])
                    # triangle 5  
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x + w_/2., y+ h_/2.])
                    self.triangles.append([x + w_, y + h_])
                    # triangle 6  
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y+ h_/2.])
                    self.triangles.append([x + w_, y + h_/2.])
                if dS>d and dE>d and d>=dW and d>=dN: #----3
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    self.triangles.append([x, y + h_])
                    # triangle 2 
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 3 
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 4 
                    self.triangles.append([x + w_/2., y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x, y + h_])
                    # triangle 5
                    self.triangles.append([x + w_/2., y + h_/2.])
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_])
                    # triangle 5
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_])
                if dS>d and dW>d and d>=dN and d>=dE: #----4
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 2 
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 3 
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 4 
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 5
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 6
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x, y + h_/2.])

                # Padrao #4 -------------------------
                if dW>d and dE>d and d>=dS and d>=dN:
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 2  
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 3  
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 4  
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 5  
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 6  
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                if dN>d and dS>d and d>=dW and d>=dE:
                    # triangle 1  
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 2  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 3  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 4  
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 5  
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x + w_/2., y + h_/2.])
                    # triangle 6  
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x + w_/2., y + h_/2.])

                # Padrao #5 -------------------------
                if dW>d and dN>d and dS>d and d>=dE:
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 2  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 3  
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x + w_/2., y])
                    # triangle 4  
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x + w_, y])
                    # triangle 5 
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x, y + h_])
                if dW>d and dN>d and dE>d and d>=dS:
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 2  
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y + h_/2.])
                    # triangle 3  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_/2.])
                    # triangle 4  
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x + w_, y + h_/2.])
                    # triangle 5  
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x + w_, y + h_/2.])
                if dN>d and dE>d and dS>d and d>=dW:
                    # triangle 1  
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y + h_])
                    # triangle 2  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_/2., y + h_])
                    # triangle 3  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_/2.])
                    # triangle 4  
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y + h_/2.])
                    # triangle 5  
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x + w_, y + h_/2.])
                if dW>d and dE>d and dS>d and d>=dN:
                    # triangle 1  
                    self.triangles.append([x, y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 2  
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 3  
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_])
                    # triangle 4  
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_])
                    # triangle 5  
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_])

                # Padrao #6 -------------------------
                if dW>d and dN>d and dS>d and dE>d:
                    # triangle 1  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x, y + h_/2.])
                    self.triangles.append([x, y])
                    # triangle 2  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 3  
                    self.triangles.append([x + w_/2., y])
                    self.triangles.append([x + w_, y])
                    self.triangles.append([x + w_, y + h_/2.])
                    # triangle 4  
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_, y + h_])
                    self.triangles.append([x + w_/2., y + h_])
                    # triangle 5  
                    self.triangles.append([x + w_, y + h_/2.])
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x, y + h_/2.])
                    # triangle 6  
                    self.triangles.append([x + w_/2., y + h_])
                    self.triangles.append([x, y + h_])
                    self.triangles.append([x, y + h_/2.])
                
                else:
                    if DEBUG_MODE:
                        print('warning! Not case found triangulation..')
        # Remover puntos repetido
        seen = set()
        #print(pt_countour)
        for a,b in pt_countour:
            if (a,b) not in seen:
                self.pts_inside_contour.append([a,b])
            seen.add((a,b))

    def draw_delaunay(self):
        points = []

        xx_ = [point.x for point in self.qtree.points]
        yy_ = [point.y for point in self.qtree.points]
        polygon_ = list(zip(xx_, yy_))

        for pt in self.qtree.points:
            points.append([pt.x, pt.y])
        for pt in self.pts_inside_contour:
            points.append(pt)
        
        points = np.array(points)
        tri = Delaunay(points)
        
        # Remover triangulos que estan fuera del polygono original
        tri_v2 = []
        for i1, i2, i3 in  tri.simplices:
            c_x = (points[i1][0] + points[i2][0] + points[i3][0])/3.0
            c_y = (points[i1][1] + points[i2][1] + points[i3][1])/3.0
            if is_inside_polygon(polygon_, [c_x, c_y]):
                # Remover triangulos que estan dentro de self.nodes_inside_polygon
                add = True
                for el in self.nodes_inside_polygon:
                    x, y = el.x0, el.y0
                    w_, h_ = el.width, el.height
                    if contains(x, y, w_, h_, [Point(c_x, c_y)]):
                        add = False
                        break
                if add:
                    tri_v2.append([i1, i2, i3])
        

        print(tri_v2)
        plt.triplot(points[:,0], points[:,1], tri_v2)
        plt.plot(points[:,0], points[:,1], 'go')

    def draw(self, w, h, plot_points=True):
        _ = plt.figure(figsize=(12, 8))

        plt.figure()
        ax = plt.subplot()
        ax.set_xlim(0, w)
        ax.set_ylim(h, 0)

        i = 0
        while i<len(self.triangles):
            tri = []
            for _ in range(3):
                tri.append(self.triangles[i])
                i += 1
            t1 = plt.Polygon(tri, fill=False, edgecolor='black', lw=0.5)
            plt.gcf().gca().add_patch(t1)

        if plot_points:
            # plots the points as red dots
            xx = [point.x for point in self.qtree.points]
            yy = [point.y for point in self.qtree.points]
            plt.plot(xx, yy, 'ro') 

            xx_ = [x for x,y in self.pts_inside_contour]
            yy_ = [y for x,y in self.pts_inside_contour]
            plt.plot(xx_, yy_, 'bo') 

            plt.gcf().gca().add_patch(patches.Polygon(list(zip(xx,yy)), fill=False, color='b'))

            self.draw_delaunay()

        plt.show()