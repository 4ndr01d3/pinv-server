import sys
import re

if len(sys.argv)!=5:
	print "it requires 3 arguments: [string file] [mapping file] [protein list file] and [output file]"
else :
	string     = sys.argv[1];
	mapping    = sys.argv[2];
	query      = sys.argv[3];
	outputfile = sys.argv[4];
	
	stringF     = open(string,"r");
	queryF      = open(query,"r");
	outputfileF = open(outputfile,"w");
	mappingF    = open(mapping,"r");
	proteins = []
	for line in queryF:
		proteins += re.split("[\t ,-]+",line.strip())
	map ={}
	for line in mappingF:
		parts = line.split("\t")
		stringIDS= parts[1].split(";")
		for stringID in stringIDS:
			if stringID != "":
				map[stringID]= parts[0]
				
	print proteins
	number=0
	outputfileF.write("#"+stringF.readline().replace(" ","\t"))
	for line in stringF:
		parts = line.split(" ")
		try:
			p1,p2 = map[parts[0]],map[parts[1]]
			print p1,p2
			if p1 in proteins and p2 in proteins:
				outputfileF.write(p1+"\t"+p2+"\t"+("\t".join(parts[2:])))
				number += 1
		except KeyError:
			print "ERROR:",parts
	
	print str(number)+ " interactions writen in the file "+outputfile

