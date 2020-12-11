import cv2
from enum import IntEnum, Enum
from quadtree.node import Node

DEBUG_MODE = False

class Child(IntEnum):
    NW = 0
    SW = 1
    NE = 2
    SE = 3
    
class Direction(Enum):
    NW = 0
    SW = 1
    NE = 2
    SE = 3
    N = 4
    S = 5
    W = 6
    E = 7

def has_to_split(node, neighbors):
    res = [deeper(el) if el is not None else -1 for el in neighbors]
    a = max(res)
    if DEBUG_MODE: 
        print(res, 'max_depth: ', a, 'u_depth: ',node.depth)
    return node.depth<=(a-2), res # 1 ou 2?
    # i = 0
    # for el in neighbors:
    #     if el is not None:
    #         print(el.depth, node.depth)
    #         if el.depth < node.depth-1:
    #             return True, i
    #     i += 1
    # return False, i

def deeper(node):
    if node is None: return -1
    if node.leaf: return node.depth

    c = find_children(node)
    return max([el.depth for el in c])

def recursive_subdivide(node, k):
    if len(node.points)<=k:
        return
    w_ = float(node.width/2)
    h_ = float(node.height/2)

    p = contains(node.x0, node.y0, w_, h_, node.points)
    nw = Node(node.x0, node.y0, w_, h_, p, depth=node.depth+1, parent=node)
    recursive_subdivide(nw, k)

    p = contains(node.x0, node.y0+h_, w_, h_, node.points)
    sw = Node(node.x0, node.y0+h_, w_, h_, p, depth=node.depth+1, parent=node)
    recursive_subdivide(sw, k)

    p = contains(node.x0+w_, node.y0, w_, h_, node.points)
    ne = Node(node.x0 + w_, node.y0, w_, h_, p, depth=node.depth+1, parent=node)
    recursive_subdivide(ne, k)

    p = contains(node.x0+w_, node.y0+h_, w_, h_, node.points)
    se = Node(node.x0+w_, node.y0+h_, w_, h_, p, depth=node.depth+1, parent=node)
    recursive_subdivide(se, k)

    node.children = [nw, sw, ne, se]

def contains(x, y, w, h, points):
    pts = []
    for point in points:
        if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
            pts.append(point)
    return pts

def find_children(node):
    if not node.children:
        return [node]
    else:
        children = []
        for child in node.children:
            children += (find_children(child))
    return children

def leaf_nodes(node):
    c = find_children(node)
    depths = [el.depth for el in c]
    max_depth = max(depths)

    res = []
    for el in c:
        if el.depth<max_depth:
            res.append(el)
    return res

def get_neighbor_of_greater_or_equal_size(node_, direction):
    if direction == Direction.N:       
        if node_.parent is None:
            return None
        if node_.parent.children[Child.SW] == node_: # Is 'self' SW child?
            return node_.parent.children[Child.NW]
        if node_.parent.children[Child.SE] == node_: # Is 'self' SE child?
            return node_.parent.children[Child.NE]
            
        node = get_neighbor_of_greater_or_equal_size(node_.parent, direction)
        if node is None or node.leaf:
            return node

        # 'self' is guaranteed to be a north child
        return (node.children[Child.SW]
                if node_.parent.children[Child.NW] == node_ # Is 'self' NW child?
                else node.children[Child.SE])
    elif direction == Direction.S:
        if node_.parent is None:
            return None
        if node_.parent.children[Child.NW] == node_: # Is 'self' NW child?
            return node_.parent.children[Child.SW]
        if node_.parent.children[Child.NE] == node_: # Is 'self' NE child?
            return node_.parent.children[Child.SE]
            
        node = get_neighbor_of_greater_or_equal_size(node_.parent, direction)
        if node is None or node.leaf:
            return node
        
        # 'self' is guaranteed to be a north child
        return (node.children[Child.NW]
                if node_.parent.children[Child.SW] == node_ # Is 'self' SW child?
                else node.children[Child.NE])
    elif direction == Direction.W:
        if node_.parent is None:
            return None
        if node_.parent.children[Child.SE] == node_: # Is 'self' SE child?
            return node_.parent.children[Child.SW]
        if node_.parent.children[Child.NE] == node_: # Is 'self' SE child?
            return node_.parent.children[Child.NW]

        node = get_neighbor_of_greater_or_equal_size(node_.parent, direction)
        if node is None or node.leaf:
            return node
        
        # 'self' is guaranteed to be a north child
        return (node.children[Child.SE]
                if node_.parent.children[Child.SW] == node_ # Is 'self' SW child?
                else node.children[Child.NE])
    elif direction == Direction.E:
        if node_.parent is None:
            return None
        if node_.parent.children[Child.SW] == node_: # Is 'self' SE child?
            return node_.parent.children[Child.SE]
        if node_.parent.children[Child.NW] == node_: # Is 'self' SE child?
            return node_.parent.children[Child.NE]

        node = get_neighbor_of_greater_or_equal_size(node_.parent, direction)
        if node is None or node.leaf:
            return node
        
        # 'self' is guaranteed to be a north child
        return (node.children[Child.SW]
                if node_.parent.children[Child.SE] == node_ # Is 'self' SW child?
                else node.children[Child.NW])
    else:
        print('Direction not Found ...', direction)
        return None

## ==========================================================================
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized