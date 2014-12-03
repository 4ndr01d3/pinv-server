
class Item(object):
    def __init__(self, id, x, y,index=None):
        self.x = x
        self.y = y
        self.id = id
        self.index =index
        
    def __str__(self):
        return "{id:"+self.id+", x:"+str(self.x)+", y:"+str(self.y)+"}"
            
class QuadTree(object):
    """An implementation of a quad-tree.
 
    This QuadTree started life as a version of [1] but found a life of its own
    when I realised it wasn't doing what I needed. It is intended for static
    geometry, ie, items such as the landscape that don't move.
 
    This implementation inserts items at the current level if they overlap all
    4 sub-quadrants, otherwise it inserts them recursively into the one or two
    sub-quadrants that they overlap.
 
    Items being stored in the tree must possess the following attributes:
 
        left - the x coordinate of the left edge of the item's bounding box.
        top - the y coordinate of the top edge of the item's bounding box.
        right - the x coordinate of the right edge of the item's bounding box.
        bottom - the y coordinate of the bottom edge of the item's bounding box.
 
        where left &lt; right and top &lt; bottom
        
    ...and they must be hashable.
    
    Acknowledgements:
    [1] http://mu.arete.cc/pcr/syntax/quadtree/1/quadtree.py
    """
    def __init__(self, items, depth=9, bounding_rect=None,quadrant="",parent=None):
        """Creates a quad-tree.
 
        @param items:
            A sequence of items to store in the quad-tree. Note that these
            items must possess left, top, right and bottom attributes.
            
        @param depth:
            The maximum recursion depth.
            
        @param bounding_rect:
            The bounding rectangle of all of the items in the quad-tree. For
            internal use only.
        """
        # The sub-quadrants are empty to start with.
        self.nw = self.ne = self.se = self.sw = None
        self.depth = depth;
        self.quadrant = quadrant
        self.parent = parent
        self.nodes={}
        self.point=None
        self.leaf = False
        self.quadrants = None

        # If we've reached the maximum depth then insert all items into this
        # quadrant.
        depth -= 1
        if depth == 0:
            self.items = items
            self.point = Item("avg",0,0,0); 
            for item in items:
                self.addQuadrantToNode(item,self.quadrant)
                self.point.x += item.x
                self.point.y += item.y
            self.point.x /= len(items)
            self.point.y /= len(items)
            return
 
        # Find this quadrant's centre.
        if bounding_rect:
            l, t, r, b = bounding_rect
        else:
            # If there isn't a bounding rect, then calculate it from the items.
            l = min(item.x for item in items)
            t = min(item.y for item in items)
            r = max(item.x for item in items)
            b = max(item.y for item in items)
        self.l, self.t, self.r, self.b =l, t, r, b
        cx = self.cx = (l + r) * 0.5
        cy = self.cy = (t + b) * 0.5
        
        self.items = items
        if len(items)<2:
            self.addQuadrantToNode(items[0],self.quadrant)
            self.point = items[0]
            self.leaf = True
            return
        
        nw_items = []
        ne_items = []
        se_items = []
        sw_items = []
        
        for item in items:
            # Which of the sub-quadrants does the item overlap?
            if item.x <= cx and item.y <= cy: 
                nw_items.append(item)
            else: 
                if item.x <= cx and item.y >= cy: 
                    ne_items.append(item)
                else: 
                    if item.x >= cx and item.y <= cy: 
                        se_items.append(item)
                    else:
                        if item.x >= cx and item.y >= cy: 
                            sw_items.append(item)
            
        # Create the sub-quadrants, recursively.
        if nw_items:
            self.nw = QuadTree(nw_items, depth, (l, t, cx, cy),self.quadrant+"0",self)
        if ne_items:
            self.ne = QuadTree(ne_items, depth, (cx, t, r, cy),self.quadrant+"1",self)
        if sw_items:
            self.sw = QuadTree(sw_items, depth, (l, cy, cx, b),self.quadrant+"2",self)
        if se_items:
            self.se = QuadTree(se_items, depth, (cx, cy, r, b),self.quadrant+"3",self)
            
        self.quadrants=[self.nw,self.ne,self.sw,self.se]
        
    def __str__(self):
        spaces=" "*(8 - self.depth)
        s="\n"+spaces + str(self.items)
        if self.nw: s += "\n"+spaces+"nw: "+str(self.nw)
        if self.ne: s += "\n"+spaces+"ne: "+str(self.ne)
        if self.sw: s += "\n"+spaces+"sw: "+str(self.sw)
        if self.se: s += "\n"+spaces+"se: "+str(self.se)
        return s;
    
    def visit(self,f):
      visitQuadtree(f, self, self.l,self.t,self.r,self.b);

    def addQuadrantToNode(self,node,quadrant):
        if self.parent==None:
            self.nodes[node.id]=quadrant
        else:
            self.parent.addQuadrantToNode(node,quadrant)
    
    def getQuadrant(self,id,level):
        return self.nodes[id][0:level]
        
    def getNodesByQuadrant(self,quadrant):
        if self.quadrant==quadrant:
            return self.items
        else:
            q = self.quadrants[int(quadrant[len(self.quadrant)])]
            if q!=None:
                return q.getNodesByQuadrant(quadrant);

def visitQuadtree(f, node, x1, y1, x2, y2):
    if (not(f(node, x1, y1, x2, y2))):
        sx = (x1 + x2) * .5
        sy = (y1 + y2) * .5
        if node.nw: visitQuadtree(f, node.nw, x1, y1, sx, sy)
        if node.ne: visitQuadtree(f, node.ne, sx, y1, x2, sy)
        if node.sw: visitQuadtree(f, node.sw, x1, sy, sx, y2)
        if node.se: visitQuadtree(f, node.se, sx, sy, x2, y2)
