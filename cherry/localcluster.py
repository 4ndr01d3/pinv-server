import sys
import time

def addClusterLink(links,n1,n2):
	if n1!=0: print n1,n2
	found= False
	
	if n1==n2: #Ignoring cluster interactions with itself
		return;
	for link in links:
		if (link["source"]==n1 and link["target"]==n2) or (link["source"]==n2 and link["target"]==n1):
			link["strength"] +=1
			found = True
			break;
	if not found:
		links.append({"source":n1,"target":n2,"strength":1})
		print "adding"


start=time.time()
print "START:\t%i"%start;
if len(sys.argv)!=3:
	print "it requires 2 arguments: [input file] and [output file]"
else :
	inputfile= sys.argv[1];
	outputfile= sys.argv[2];
	from igraph import *
	g = Graph()
	f = open(inputfile,"r")
	f.readline()
	#level=2

	vertices=[]
	links = []
	for line in f:
		parts = line.split("\t")
		if not (parts[0] in vertices):
			vertices.append(parts[0])
			g.add_vertex(parts[0])
		if not (parts[1] in vertices):
			vertices.append(parts[1])
			g.add_vertex(parts[1])
		g.add_edge(parts[0],parts[1])
		links.append([parts[0],parts[1]])
		
	f.close()
	layout = g.layout_graphopt()
	clusters = g.clusters()
	clustersg = clusters.cluster_graph()
	
	clusterLinks=[]
	for link in links:
		addClusterLink(clusterLinks,clusters.membership[vertices.index(link[0])],clusters.membership[vertices.index(link[1])])

	clustersg.layout_graphopt()
	print "number of edges in cluster graph :%d"%clustersg.ecount()
	print "number of vertices in cluster graph :%d"%clustersg.vcount()
	
	g.write_svg("testCluster.svg",width=1400,height=1000)
	clustersg.write_svg("testClustered.svg",width=1400,height=1000)

end=time.time()
print "END:\t%i"%end;
print "it took %d seconds to cluster %d interactions"%(end-start,len(links))
