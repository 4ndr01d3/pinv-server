import sys
import re

#Extracting the Uniprot IDs from the annotations file
def getQueryIDs(featuresF):
	query = {}
	featuresF.readline()
	for line in featuresF:
		parts = line.split("\t")
		query[parts[0]] =[]
	query=query.keys()
	featuresF.seek(0)
	return query

#Creating a map between Uniprot and ENSP Ids for the queried proteins
def getMapUniprot2ENSP(aliasesF,query):
	map  = {}
	mapI = {}
	aliasesF.readline()
	for line in aliasesF:
		parts = line.split("\t")
		if parts[2] in query:
			map[parts[2]] = parts[1]
			mapI[parts[1]] = parts[2]
	return map,mapI

#writing the interaction files by extracting the info from the String database file that contains anything from the query proteins
def writeNetworkFile (N_outputF,stringF,mapI):
	number=0
	n=0
	N_outputF.write("#"+stringF.readline().replace(" ","\t"))
	for line in stringF:
		parts = line.split(" ")
		try:
			p1,p2 = mapI[parts[0][5:]],mapI[parts[1][5:]]
			N_outputF.write(p1+"\t"+p2+"\t"+("\t".join(parts[2:])))
			number += 1
		except:
			n += 1
	N_outputF.close()
	return number

def getUniprotMap(uniprotF,query):
	UniprotMap ={}
	for line in uniprotF:
		parts = line.split("\t")
		if parts[0] in query:
			UniprotMap[parts[0]]= [x.strip() for x in parts[2:]]
	return UniprotMap

def writeFeaturesFile(F_outputF,featuresF,UniprotMap):
	number=0
	mappingErrors={}
	titles =featuresF.readline().split("\t")
	F_outputF.write("#ID\torganism\t" + "\t".join([x.strip() for x in titles[1:]]) +"\tgene\tGO_id\tGO_term\n" )
	for line in featuresF:
		parts = line.split("\t")
		try:
			F_outputF.write(parts[0]+"\tHomo Sapiens\t" + "\t".join([x.strip() for x in parts[1:]]) + "\t" + "\t".join(UniprotMap[parts[0]]) + "\n")
			number += 1
		except:
			F_outputF.write(parts[0]+"\tHomo Sapiens\t" + "\t".join([x.strip() for x in parts[1:]]) + "\t\t\t\n")
			mappingErrors[parts[0]] = 1
	F_outputF.close()
	return number,mappingErrors

if len(sys.argv)!=7:
	print "it requires 6 arguments: [feature_file] [aliases_file] [string_file] [uniprot_file] [features output file] [network output file] |",len(sys.argv)
else :
	features     = sys.argv[1];
	aliases      = sys.argv[2];
	string       = sys.argv[3];
	uniprot      = sys.argv[4];
	F_output     = sys.argv[5];
	N_output     = sys.argv[6];
	
	aliasesF      = open(aliases,"r");
	featuresF     = open(features,"r");
	stringF       = open(string,"r");
	uniprotF      = open(uniprot,"r");
	F_outputF     = open(F_output,"w");
	N_outputF     = open(N_output,"w");

	query = getQueryIDs(featuresF)
	print "The feature file contains",len(query)," UniProt IDs"
	
	map,mapI=getMapUniprot2ENSP(aliasesF,query)
	print len(map.keys())," proteins have been map to Ensembl protein ids"

	number = writeNetworkFile(N_outputF,stringF,mapI)
	print str(number)+ " interactions writen in the file "+N_output
	
	UniprotMap = getUniprotMap(uniprotF,query)
	print len(UniprotMap.keys()), " proteins found in the uniprot file"

	number,mappingErrors = writeFeaturesFile(F_outputF,featuresF,UniprotMap)
	print str(number)+ " protein+features writen in the file "+F_output, "\n There weren't uniprot features for:\n", "-".join(mappingErrors.keys())
