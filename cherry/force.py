import math
import types
import random
from quadtree import *


d3_layout_forceLinkDistance = 20
d3_layout_forceLinkStrength = 1
d3_layout_forceChargeDistance2 = float("inf");

class Link(object):
    def __init__(self, id, source, target,index=None):
        self.source = source
        self.target = target
        self.id = id
        self.index =index
        
    def __str__(self):
        return "{id:"+self.id+", source:"+str(self.source)+", target:"+str(self.target)+"}"


def d3_layout_forceAccumulate(quad, alpha, charges):
    cx = 0
    cy = 0
    quad.charge = 0;
    if not quad.leaf:
        nodes = quad.nodes
        n = len(nodes)
        for c in nodes:
            if c == None: continue
            d3_layout_forceAccumulate(c, alpha, charges)
            quad.charge += c.charge;
            cx += c.charge * c.cx;
            cy += c.charge * c.cy;

    if quad.point != None:
        #jitter internal nodes that are coincident
        if not quad.leaf:
            quad.point.x += random.random() - .5;
            quad.point.y += random.random() - .5;
        quad.pointCharge= alpha * charges[quad.point.index];
        quad.charge += quad.pointCharge
        cx += quad.pointCharge * quad.point.x;
        cy += quad.pointCharge * quad.point.y;

    quad.cx = cx / quad.charge;
    quad.cy = cy / quad.charge;
    

class Force():
    def __init__(self):
        #how this would wortk without events TICK
        #self.event = d3.dispatch("start", "tick", "end") 
        self._size            = [1, 1]
        #self.drag           
        self._alpha           = 0
        self._friction        = .9
        self._linkDistance    = d3_layout_forceLinkDistance
        self._linkStrength    = d3_layout_forceLinkStrength
        self._charge          = -30
        self._chargeDistance2 = d3_layout_forceChargeDistance2
        self._gravity         = .1
        self._theta2          = .64
        self._nodes           = []
        self._links           = []
        self._distances       = [];
        self._strengths       = [];
        self._charges         = [];

    def nodes(self,x=None):
        if (x==None):
            return self._nodes
        self._nodes = x
        return self
  
    def links(self,x=None):
        if (x==None):
            return self._links
        self._links = x
        return self
  
    def size(self,x=None):
        if (x==None):
            return self._size
        self._size = x
        return self

    def linkDistance(self,x=None):
        if (x==None):
            return self._linkDistance
        self._linkDistance = x
        return self

    def linkStrength(self,x=None):
        if (x==None):
            return self._linkStrength
        self._linkStrength = x #linkStrength = typeof x === "function" ? x : +x;
        return self
  
    def friction(self,x=None):
        if (x==None):
            return self._friction
        self._friction = x
        return self
  
    def charge(self,x=None):
        if (x==None):
            return self._charge
        self._charge = x
        return self

    def chargeDistance(self,x=None):
        if (x==None):
            return math.sqrt(_chargeDistance2)
        self._chargeDistance2 = x*x
        return self
    
    def gravity(self,x=None):
        if (x==None):
            return self._gravity
        self._gravity = x
        return self
  
    def theta(self,x=None):
        if (x==None):
            return math.sqrt(self._theta)
        self._theta = x * x
        return self
  
    def alpha(self,x=None):
        if (x==None):
            return self._alpha
        if self._alpha != 0:
            self._alpha = x if x>0 else 0
        else:
            self._alpha = x
            self.run() # the simulation should start here
#            self._alpha = 0.9
#            self.run()
            #event.start({type: "start", alpha: alpha = x});
            #d3.timer(force.tick);
        return self
    def run(self):
        for i in range(1000):
            #print i
            if self.tick():
                return; 
    def start(self):
        n = len(self._nodes)
        m = len(self._links)
        w = self._size[0]
        h = self._size[1]
        neighbors = None
        #o;
        def position(dimension, size,neighbors,n,m,i):
            if neighbors==None:
                neighbors = [[] for k in range(n)]
                
                for j in range(m):
                    neighbors[self._links[j].source.index].append(self._links[j].target)
                    neighbors[self._links[j].target.index].append(self._links[j].source)
              
            candidates = neighbors[i]

            for j in range(len(candidates)):
                if hasattr(candidates[j], dimension) and getattr(candidates[j],dimension)!=None:
                    return getattr(candidates[j],dimension)
                
            return random.random() * size

        for i in range(n):
            self._nodes[i].index = i
            self._nodes[i].weight = 0
            
        for i in range(m):
            if type(self._links[i].source) == int:
                self._links[i].source = self._nodes[self._links[i].source]
            if type(self._links[i].target) == int:
                self._links[i].target = self._nodes[self._links[i].target]
            self._links[i].source.weight += 1
            self._links[i].target.weight += 1

        for i in range(n):
            if not hasattr(self._nodes[i],'x')   or self._nodes[i].x==None:  self._nodes[i].x  = position("x",  w,neighbors,n,m,i)
            if not hasattr(self._nodes[i],'y')   or self._nodes[i].y==None:  self._nodes[i].y  = position("y",  w,neighbors,n,m,i)
            if not hasattr(self._nodes[i],'px')  or self._nodes[i].px==None: self._nodes[i].px = self._nodes[i].x
            if not hasattr(self._nodes[i],'py')  or self._nodes[i].py==None: self._nodes[i].py = self._nodes[i].y

        if type(self._linkDistance)==types.FunctionType:
            self._distances = [ self._linkDistance(self._links[i], i) for i in range(m)]
        else:
            self._distances = [ self._linkDistance for i in range(m)]
        
        if type(self._linkStrength)==types.FunctionType:
            self._strengths = [ self._linkStrength(self._links[i], i) for i in range(m)]
        else:
            self._strengths = [ self._linkStrength for i in range(m)]

        if type(self._charge)==types.FunctionType:
            self._charges = [ self._charge(self._links[i], i) for i in range(n)]
        else:
            self._charges = [ self._charge for i in range(n)]


        return self.resume()

    def resume(self):
        return self.alpha(.1)

    def stop(self):
        return self.alpha(0)

    def repulse(self,node):
        def function(quad, x1, _, x2,_2):
            if (quad.point != node):
                dx = quad.cx - node.x
                dy = quad.cy - node.y
                dw = x2 - x1
                dn = dx * dx + dy * dy
            
                # Barnes-Hut criterion. 
                if (dw * dw / self._theta2) < dn:
                    if dn < self._chargeDistance2:
                        k = quad.charge / dn;
                        node.px -= dx * k;
                        node.py -= dy * k;
                    return True;
                
                if quad.point!=None and dn!=0 and dn < self._chargeDistance2:
                    k = quad.pointCharge / dn;
                    node.px -= dx * k;
                    node.py -= dy * k;
                  
            return quad.charge==0
        return function

    def tick(self):
        #simulated annealing, basically
        self._alpha *= .99
        if self._alpha < .005:
            #event.end({type: "end", alpha: alpha = 0});
            return True
        
    
        n = len(self._nodes)
        m = len(self._links)
        q=0 
        i=0 # current index
        o=0 # current object
        s=0 # current source
        t=0 # current target
        l=0 # current distance
        k=0 # current force
        x=0 # x-distance
        y=0 # y-distance
    
        # gauss-seidel relaxation for links
        for i in range(m):
            o = self._links[i]
            s = o.source
            t = o.target
            x = t.x - s.x
            y = t.y - s.y
            l = (x * x + y * y)
            if l != 0:
                l = math.sqrt(l)
                l =self._alpha * self._strengths[i] * (l-self._distances[i])/l
                x *= l
                y *= l
                k = float(s.weight) / (t.weight + s.weight)
                t.x -= x * k
                t.y -= y * k
                k = 1 - k
                s.x += x * k
                s.y += y * k
          
        
    
        #apply gravity forces
        k = self._alpha * self._gravity
        if k!= 0:
            x = self._size[0] / 2
            y = self._size[1] / 2
            for i in range(n):
                o = self._nodes[i]
                o.x += (x - o.x) * k
                o.y += (y - o.y) * k
                
          
        
    
        #compute quadtree center of mass and apply charge forces
        if (self._charge != 0):
            q= QuadTree(self._nodes)
            d3_layout_forceAccumulate(q, self._alpha, self._charges);
            for i in range(n):
                o = self._nodes[i]
                q.visit(self.repulse(o));
            
          
        
    
        #position verlet integration
        for i in range(n):
            o = self._nodes[i];
            
            tmp,o.px = o.px,o.x
            o.x -= (tmp - o.x) * self._friction;
            tmp,o.py = o.py,o.y
            o.y -= (tmp - o.y) * self._friction;
          
        return False
    
        #event.tick({type: "tick", alpha: alpha});

