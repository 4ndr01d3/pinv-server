#!/usr/bin/env python
import sunburnt
import settings
from string import *
import os
import os.path
import urllib2
import shutil
from force import *
from quadtree import *

def create_new_solr(network_name):
    new_core_name = os.path.join(settings.SOLR_BASE, network_name)
    if not os.path.exists(new_core_name):
        message = "Creating solr core in:", new_core_name
        template_path = os.path.join(settings.SOLR_BASE,"blank")
        shutil.copytree(template_path,new_core_name)
        #"http://solrserver:8080/solr/admin/cores?action=CREATE&name=222&instanceDir=cores/222"
        SOLR_CREATE_URL='%s/solr/admin/cores?action=CREATE&name=%s&instanceDir=cores/%s'%(settings.SOLR_SERVER,network_name,network_name)
        print "--- CREATING:",SOLR_CREATE_URL
        urllib2.urlopen(SOLR_CREATE_URL)
        result = True
    else:
        message = "Core already exists:", new_core_name
        result = False
    return message, result

def fix_name(name):
    return name.lower().replace(" ","_")

# http://stackoverflow.com/questions/295135
def clean(input):
    import string
    if not input:
        return ''
    valid_chars = "%s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in input if c in valid_chars)

def load_annotations(fin):
    annos = {}
    line = fin.readline()
    while line.startswith("#"):
        head = line.strip().strip("#").split("\t")
        line = fin.readline()
    while line:
        if not line.startswith("#") and line.strip() != '':
            row = [x.strip() for x in line.split("\t")]
            assert len(row) == len(head)
            annos[row[0]] = map(strip,row[1:])
        line = fin.readline()
    fieldnames = map(fix_name,map(strip,head[1:]))
    return fieldnames, annos

def load_network(fin):
    network = {}
    line = fin.readline()
    while line.startswith("#"):
        head = line.strip().strip("#").split("\t")
        line = fin.readline()
    while line:
        if not line.startswith("#") and line.strip() != '':
            row = line.strip().split("\t")
            assert len(row) == len(head)
            p1, p2 = row[0], row[1]
            network[(p1,p2)] = map(strip,row[2:])
        line = fin.readline()
    fieldnames = ["score_" + x for x in map(fix_name,map(strip,head[2:]))]
    return fieldnames, network

def clusterCore(network_name):
    core_name = os.path.join(settings.SOLR_BASE, network_name)
    if os.path.exists(core_name):
        return "["+network_name+"] to be cluster"
    else:
        return "["+network_name+"] doesn't exists"

class DynamicInteraction(object):
    def __init__(self, id, p1, p2, fieldnames, fieldvalues, unified_score):
        self.id = id #p1 + "-" + p2 
        self.p1 = p1
        self.p2 = p2
        self.score = unified_score
        for name, value in zip(fieldnames, fieldvalues):
            setattr(self,name,value)
    
    def __repr__(self):
        return "\t".join(dir(self))

def addClusterLink(links,n1,n2):
    found= False
    
    if n1==n2: #Ignoring cluster interactions with itself
        return;
    for link in links:
        if (link.source==n1 and link.target==n2) or (link.source==n2 and link.target==n1):
            link.strength +=1
            found = True
            break;
    if not found:
        link =Link(n1+"_"+n2,n1,n2)
        link.strength=1
        links.append(link)

class InteractionNetwork(object):
    def __init__(self, name, description, nw_fin, ann_fin):
	self.errors = set()
        self.name = name
        self.description = description
        self.nhead, self.network = load_network(nw_fin)
        self.ahead, self.annotations = load_annotations(ann_fin)
        self.g = None
        self.q = None
    
    def upload(self, solr_interface):
        stepsize = 1000
        print "Inserting records...",
        count = 0
        queue = []
        for (p1,p2), network_annotations in self.network.items():
            count += 1
            unified_score = network_annotations[-1]        
            if not p1 in self.annotations:
                self.errors.add("Missing annotations for protein:%s"%p1)
                continue
            if not p2 in self.annotations:
                self.errors.add("Missing annotations for protein:%s"%p2)
                continue
            values = network_annotations[:-1] + self.annotations[p1] + self.annotations[p2]
            names = self.nhead[:-1] + ["p1_"+x for x in self.ahead]  + ["p2_"+x for x in self.ahead]
            d = DynamicInteraction(p1 + "-" + p2,p1, p2, names, values, unified_score)
            #solr_interface.add(d)
            queue.append(d)
            if count%stepsize==0:
                print "\b.",
                solr_interface.add(queue)
                solr_interface.commit()
                queue = []
        print "final commit...",
        solr_interface.add(queue)
        solr_interface.commit() 
        print "done"
    
    
    def createGraph(self):
        print "Creating graphic...",
        self.vertices=[]
        self.links = []
        self.g = Force()
        self.g.size([2000, 2000])
        self.g.charge(-120)
        self.g.linkDistance(30)


        for (p1,p2), network_annotations in self.network.items():
            try:
                pos1 = self.vertices.index(p1)
            except:
                pos1 = len(self.vertices)
                self.vertices.append(p1)
            try:
                pos2 = self.vertices.index(p2)
            except:
                pos2 = len(self.vertices)
                self.vertices.append(p2)
            self.links.append(Link(p1+"_"+p2,pos1,pos2))
        self.g.nodes( [Item(self.vertices[i]) for i in range(len(self.vertices))] )
        self.g.links(self.links)
        self.g.start()


    def createQuadtree(self):
        if self.g==None:
            self.createGraph()
            
        print "Creating quadtree...",
#                .charge(-self.opt.radius*(3+self.proteins.length))
 #               .linkDistance(self.opt.radius*(3+self.proteins.length*0.05))
        
        self.q=QuadTree(self.g.nodes())
        
    def createClusters(self,solr_interface,from_level,to_level):
        if self.q==None:
            self.createQuadtree()

        
        tagQuadrants(self.q)
        fillAllPointsPerQuadrant(self.q)
        

        print "Starting clustering...",
        for level in range(from_level,to_level):
            clusterLinks=[]
    
            for link in self.links:
                n1 = link.source.quadrant[0:level]
                n2 = link.target.quadrant[0:level]
                addClusterLink(clusterLinks,n1,n2)
            
            queue = []
            for l in clusterLinks:
                
                p1,p2 = l.source,l.target
  #              print "pre:",level,p1,p2
                values = ["CLUSTER",";".join([i.id for i in getNodesByQuadrant(self.q,p1)]),"CLUSTER",";".join([i.id for i in getNodesByQuadrant(self.q,p2)]),level]
                names = ["p1_organism","p1_description","p2_organism", "p2_description", "level"]

                d = DynamicInteraction(str(level)+"_"+p1+"-"+p2,p1, p2, names, values,l.strength)
#                print d.id,d.level,d.p1,d.p1_description,d.p2,d.p2_description,d.score
                #solr_interface.add(d)
                queue.append(d)
            print "commit level ",level,"...",
            solr_interface.add(queue)
            solr_interface.commit() 
        
def getTextLine(q,id):
    text = id+"\t"
    npq = q.getNodesByQuadrant(id)
    sep=""
    for n in npq:
        text += sep+n.id
        sep=","
    return text

