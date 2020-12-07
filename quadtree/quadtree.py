from quadtree.rect import Rect

class QuadTree:
    """A class implementing a quadtree."""

    def __init__(self, boundary, max_points=4, depth=0, parent=None):
        """Initialize this node of the quadtree.

        boundary is a Rect object defining the region from which points are
        placed into this node; max_points is the maximum number of points the
        node can hold before it must divide (branch into four more nodes);
        depth keeps track of how deep into the quadtree this node lies.

        """
        self.nw, self.ne, self.sw, self.se = None, None, None, None
        self.boundary = boundary
        self.max_points = max_points
        self.points = []
        self.depth = depth
        self.parent = parent
        # A flag to indicate whether this node has divided (branched) or not.
        self.divided = False

    def __str__(self):
        """Return a string representation of this node, suitably formatted."""
        sp = ' ' * self.depth * 2
        s = str(self.boundary) + '\n'
        s += sp + ', '.join(str(point) for point in self.points)
        if not self.divided:
            return s
        return s + '\n' + '\n'.join([
                sp + 'nw: ' + str(self.nw), sp + 'ne: ' + str(self.ne),
                sp + 'se: ' + str(self.se), sp + 'sw: ' + str(self.sw)])

    def divide(self):
        """Divide (branch) this node by spawning four children nodes."""

        cx, cy = self.boundary.cx, self.boundary.cy
        w, h = self.boundary.w / 2, self.boundary.h / 2
        # The boundaries of the four children nodes are "northwest",
        # "northeast", "southeast" and "southwest" quadrants within the
        # boundary of the current node.
        self.nw = QuadTree(Rect(cx - w/2, cy - h/2, w, h),
                                    self.max_points, self.depth + 1, parent=self)
        self.ne = QuadTree(Rect(cx + w/2, cy - h/2, w, h),
                                    self.max_points, self.depth + 1, parent=self)
        self.se = QuadTree(Rect(cx + w/2, cy + h/2, w, h),
                                    self.max_points, self.depth + 1, parent=self)
        self.sw = QuadTree(Rect(cx - w/2, cy + h/2, w, h),
                                    self.max_points, self.depth + 1, parent=self)
        self.divided = True

    def insert(self, point):
        """Try to insert Point point into this QuadTree."""

        if not self.boundary.contains(point):
            # The point does not lie inside boundary: bail.
            return False
        if len(self.points) < self.max_points:
            # There's room for our point without dividing the QuadTree.
            self.points.append(point)
            print(self.points, len(self.points), self.max_points)
            return True

        # No room: divide if necessary, then try the sub-quads.
        if not self.divided:
            self.divide()

        return (self.ne.insert(point) or
                self.nw.insert(point) or
                self.se.insert(point) or
                self.sw.insert(point))
    
    def insert_all(self, points):
        pass

    def query(self, boundary, found_points):
        """Find the points in the quadtree that lie within boundary."""

        if not self.boundary.intersects(boundary):
            # If the domain of this node does not intersect the search
            # region, we don't need to look in it for points.
            return False

        # Search this node's points to see if they lie within boundary ...
        for point in self.points:
            if boundary.contains(point):
                found_points.append(point)
        # ... and if this node has children, search them too.
        if self.divided:
            self.nw.query(boundary, found_points)
            self.ne.query(boundary, found_points)
            self.se.query(boundary, found_points)
            self.sw.query(boundary, found_points)
        return found_points

    def __len__(self):
        """Return the number of points in the quadtree."""

        npoints = len(self.points)
        if self.divided:
            npoints += len(self.nw)+len(self.ne)+len(self.se)+len(self.sw)
        return npoints

    def getAllLeaf(self, found_leafs):
        if self.leaf:
            found_leafs.append(self)
        if self.divided:
            self.nw.getAllLeaf(found_leafs)
            self.ne.getAllLeaf(found_leafs)
            self.se.getAllLeaf(found_leafs)
            self.sw.getAllLeaf(found_leafs)
        return found_leafs
            
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

    def draw(self, ax, c='k'):
        """Draw a representation of the quadtree on Matplotlib Axes ax."""

        self.boundary.draw(ax, c=c)
        if self.divided:
            self.nw.draw(ax, c=c)
            self.ne.draw(ax, c=c)
            self.se.draw(ax, c=c)
            self.sw.draw(ax, c=c)

    # ========================== Balanced QuadTree ===============
    def getLeafs_to_balanced(self):
        # Insert all the leaf nodes of QT(I) whose size is greater than two and less
        # than the size of root node into a linear list, L.
        list_leafs = []
        self.getAllLeaf(list_leafs)
        leafs_depths = [qt.depth for qt in list_leafs]
        max_depth = max(leafs_depths)
        res = []
        for qt in list_leafs:
            if qt.depth>2 and qt.depth<max_depth:
                res.append(qt)
        list_leafs = None
        return res
        
    def balanced(self):
        # Input: A quadtree QT(I)
        # Output: A balanced version of QT(I) .
        L = self.getLeafs_to_balanced()
        while L:
            # Remove a node, u, from L.
            u = L.pop()
            pass
        return L
