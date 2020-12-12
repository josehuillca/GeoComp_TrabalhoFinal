import numpy as np
import matplotlib.pyplot as plt

from quadtree.utils import find_children, get_neighbor_of_greater_or_equal_size, Direction, deeper, DEBUG_MODE

class Mesh():
    def __init__(self, qtree):
        self.qtree = qtree
        self.triangles = []

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
        plt.show()