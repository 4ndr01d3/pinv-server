import math
class Item(object):
    def __init__(self, id, x=None, y=None):
        self.x      = x
        self.y      = y
        self.id     = id
        
    def __str__(self):
        return "{id:"+self.id+", x:"+str(self.x)+", y:"+str(self.y)+"}"

# Recursively inserts the specified point p at the node n or one of its
# descendants. The bounds are defined by [x1, x2] and [y1, y2].
def insert(n, d, x, y, x1, y1, x2, y2) :
    if (math.isnan(x) or math.isnan(y)): return; # ignore invalid points
    if (n.leaf):
        nx = n.x
        ny = n.y
        if (nx != None):
            # If the point at this leaf node is at the same position as the new
            # point we are adding, we leave the point associated with the
            # internal node while adding the new point to a child node. This
            # avoids infinite recursion.
            if ((math.fabs(nx - x) + math.fabs(ny - y)) < .01):
                insertChild(n, d, x, y, x1, y1, x2, y2)
            else:
                nPoint = n.point
                n.x = n.y = n.point = None
                insertChild(n, nPoint, nx, ny, x1, y1, x2, y2)
                insertChild(n, d, x, y, x1, y1, x2, y2)
        else: 
            n.x = x
            n.y = y
            n.point = d
      
    else:
        insertChild(n, d, x, y, x1, y1, x2, y2)
 

# Recursively inserts the specified point [x, y] into a descendant of node
# n. The bounds are defined by [x1, x2] and [y1, y2].
def insertChild(n, d, x, y, x1, y1, x2, y2):
    # Compute the split point, and the quadrant in which to insert p.
    sx = (x1 + x2) * .5
    sy = (y1 + y2) * .5
    right = x >= sx
    bottom = y >= sy
    
    if right:
        if bottom: i=3 
        else: i=1
    else:
        if bottom:i=2
        else: i=0

    # Recursively insert into the child node.
    n.leaf = False
    if n.nodes[i]==None :
        n.nodes[i] =QuadTree()

    # Update the bounds as we recurse.
    if right: x1 = sx
    else: x2 = sx
    
    if bottom: y1 = sy
    else: y2 = sy;
    insert(n.nodes[i], d, x, y, x1, y1, x2, y2);


      
class QuadTree():
    def __init__(self, data=None):#, x1=None, y1=None, x2=None, y2=None):
        if data!=None:
#             if x1 != None:
#                 x1_ = x1
#                 y1_ = y1
#                 x2_ = x2
#                 y2_ = y2
#             else:
            x2_ = y2_ = -float("inf")
            x1_ = y1_ = float("inf")
            xs = []
            ys = []
            n = len(data)
            for i in range(n): 
                  d = data[i]
                  if d.x < x1_: x1_ = d.x
                  if d.y < y1_: y1_ = d.y
                  if d.x > x2_: x2_ = d.x
                  if d.y > y2_: y2_ = d.y
                  xs.append(d.x)
                  ys.append(d.y)
                  
            # Squarify the bounds.
            dx = x2_ - x1_
            dy = y2_ - y1_
            if dx > dy: 
                y2_ = y1_ + dx;
            else: 
                x2_ = x1_ + dy;
            
            self.x1_ = x1_
            self.y1_ = y1_
            self.x2_ = x2_
            self.y2_ = y2_
                
            self.initNode()
            
            # Insert all points.
            for i in range(n):
                insert(self, data[i], xs[i], ys[i], x1_, y1_, x2_, y2_)
            
            # Discard captured fields.
            xs = ys = data = d = None;
               
        else:
            self.initNode()

    def initNode(self):
        self.leaf     = True
        self.nodes    = [None,None,None,None]
        self.point    = None
        self.x        = None
        self.y        = None
    
    def visit(self,f):
        d3_geom_quadtreeVisit(f,self,self.x1_, self.y1_, self.x2_, self.y2_)

def d3_geom_quadtreeVisit(f, node, x1, y1, x2, y2):
  if (not f(node, x1, y1, x2, y2)):
    sx = (x1 + x2) * .5
    sy = (y1 + y2) * .5
    children = node.nodes
    if children[0] != None: d3_geom_quadtreeVisit(f, children[0], x1, y1, sx, sy);
    if children[1] != None: d3_geom_quadtreeVisit(f, children[1], sx, y1, x2, sy);
    if children[2] != None: d3_geom_quadtreeVisit(f, children[2], x1, sy, sx, y2);
    if children[3] != None: d3_geom_quadtreeVisit(f, children[3], sx, sy, x2, y2);        
    
def tagQuadrants(node, quadrant=""):
    node.quadrant = quadrant
    if node.point != None:
        node.point.quadrant=quadrant
        
    children = node.nodes
    if children[0] != None: tagQuadrants(children[0], quadrant+"0");
    if children[1] != None: tagQuadrants(children[1], quadrant+"1");
    if children[2] != None: tagQuadrants(children[2], quadrant+"2");
    if children[3] != None: tagQuadrants(children[3], quadrant+"3");        

def fillAllPointsPerQuadrant(node):
    children = node.nodes
    node.points = []
    if node.point != None:
        node.points += [node.point]
    if children[0] != None: node.points += fillAllPointsPerQuadrant(children[0]);
    if children[1] != None: node.points += fillAllPointsPerQuadrant(children[1]);
    if children[2] != None: node.points += fillAllPointsPerQuadrant(children[2]);
    if children[3] != None: node.points += fillAllPointsPerQuadrant(children[3]);
    return node.points

def getNodesByQuadrant(node,quadrant):
    if node.quadrant==quadrant:
        return node.points
    else:
        q = node.nodes[int(quadrant[len(node.quadrant)])]
        if q!=None:
            return getNodesByQuadrant(q,quadrant);
