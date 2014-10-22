Uploading your dataset
======

When you want to upload your dataset into PINV, the server requires 2 files: one that includes the protein interactions and one with protein annotations:

Interactions File
------

The interactions file is a tab delimited file where the first line should start with ```#``` followed with the header information. 
The header is used to specify the names of each of the columns in your interactions file. 
The first two columns are the accession numbers of the interacting proteins.
Any following column in the file will be considered as score values of some kind of evidence for that interaction, and the last of those scores should be a unified value.

**Example**
```
#P1	P2	STRING	SeqSim	SharedDomain	Other Data	Interologs	Unified Score
P66777	Q7D856	0.00000	0.00000	0.33000	0.00000	0.00000	0.33000
Q50906	P0A624	0.64200	0.00000	0.00000	0.00000	0.00000	0.64200
Q7D890	Q7D5S2	0.00000	0.00000	0.33000	0.00000	0.00000	0.33000
P64398	O53921	0.00000	0.00000	0.33000	0.00000	0.00000	0.33000
P66777	Q7D5S2	0.00000	0.00000	0.13000	0.00000	0.00000	0.13000
Q7D856	P64398	0.00000	0.00000	0.00000	0.12900	0.00000	0.12900
Q50906	O53921	0.00000	0.16400	0.13000	0.00000	0.00000	0.23988
P0A624	Q50906	0.86138	0.00000	0.00000	0.00000	0.00000	0.86138
Q7D890	P0A624	0.00000	0.00000	0.00000	0.13200	0.00000	0.13200
P66777	Q7D890	0.00000	0.00000	0.33000	0.00000	0.00000	0.33000
``` 

Protein Features File
------

Through the Protein Feature File you can enrich the information of your network. Information included here will be used by PINV to provide ways to manipulate your visualization. (e.g. color the nodes by one of the provided features).

The only required feature is the organism that the protein belongs to. **All** the proteins included in the interaction file should be included in the Features File.

The format of the file it is also tab delimited, where the first line should start with ```#``` followed with the header information.

**Example**
```
#Protein-Acc	Organism	Gene-Name	Description	Funct-Class	Chrom-Location	Betweenness	Closeness	Degree	Eigenvector
P66777	MTB	ephD	Probable oxidoreductase ephD (EC 1.-.-.-)	virulence, detoxification, adaptation	2345	108145.59	0.35848	188	0.08187
Q7D856	MTB	MT1723	Poly-beta-hydroxybutyrate polymerase/very long chain acyl-CoA dehydrogenase, putative (EC 6.2.1.-)	lipid metabolism	1777	114945.96	0.33660	109	0.00521
Q50906	MTB	apa	Alanine and proline-rich secreted protein apa (45/47 kDa antigen) (Fibronectin attachment protein) (Immunogenic protein MPT32) (Antigen MPT-32) (45 kDa glycoprotein) (FAP-B)	cell wall and cell processes	1969	8134.00	0.29093	23	0.00002
P0A624	MTB	modB	Molybdenum transport system permease protein modB	cell wall and cell processes	1967	6886.39	0.29176	30	0.00060
Q7D890	MTB	MT1662	Response regulator	regulatory proteins	U	15434.00	0.32322	81	0.00023
Q7D5S2	MTB	sigF	Stress response/stationary phase sigma factor SigF (ALTERNATE RNA POLYMERASE SIGMA FACTOR SIGF)	information pathways	3527	38899.07	0.32518	87	0.00021
P64398	MTB	hrcA	Heat-inducible transcription repressor hrcA	virulence, detoxification, adaptation	2531	49695.08	0.32840	89	0.00034
O53921	MTB	MT1712	PROBABLE TRANSCRIPTIONAL REGULATORY PROTEIN (Transcriptional regulator, ArsR family)	regulatory proteins	1766	46418.37	0.33021	82	0.00133
```

From Excel to Tab Separated Values TSV {#excel}
------
If you have your data in excel and want to import it to PINV, what you need to do is use the option ```Save as...``` from the File menu in excel, 
and then you should choose ```Windows Formatted Text (.txt)```. This format ensures that you have the right separators in between values (```\t```) 
and in between lines (```\n```).

Creating the interactions file from the STRING database {#string_file}
======
It is usual that a researcher has the proteins with some annotations, but wants to visualize them in a network. We can obtain the interactions from STRING.

There are multiple ways to obtain the data from STRING, for instance we will use the flat files available through this [http://string-db.org/newstring_cgi/show_download_page.pl](link). 
For this example we are selecting the protein network data for the organism *Homo Sapiens*. 
The first lines of this file looks like this [example][example]:

```
protein1 protein2 combined_score
9606.ENSP00000000233 9606.ENSP00000020673 176
9606.ENSP00000000233 9606.ENSP00000054666 327
9606.ENSP00000000233 9606.ENSP00000158762 718
9606.ENSP00000000233 9606.ENSP00000203407 272
9606.ENSP00000000233 9606.ENSP00000203630 241
9606.ENSP00000000233 9606.ENSP00000215071 170
9606.ENSP00000000233 9606.ENSP00000215115 196
9606.ENSP00000000233 9606.ENSP00000215375 279
9606.ENSP00000000233 9606.ENSP00000215565 151
```


From Ensembl protein ids to UniProtKB IDs
------
The file that STRING provides contains Ensemble Protein IDs, PINV doesn't discriminate between the types of accession numbers you use for the network, as long as it corresponds (i.e. consistent type) with the IDs in the features file. 
For this example we will create an interaction file that uses UniProtKB accession numbers. 

STRING provides a file that lists the aliases for all the proteins in their database, to download this file go to the [http://string-db.org/newstring_cgi/show_download_page.pl](download page) and look for the file named protein.aliases.v[version].txt.gz for instance [http://string-db.org/newstring_download/protein.aliases.v9.1.txt.gz](here) is the link for version 9.1. 
Unfortunately, this file is quite big(>400Mb zipped and >2.7Gb unzipped) and there are not up-to-date versions per organism. Nonetheles, you can create a filtered file of this file through the command line. 
For example to create a file(```protein.aliases.9606.v9.1.txt```) with the lines that includes *9606* (Human taxonomy ID) you can execute:
```
zgrep 9606 protein.aliases.v9.1.txt > protein.aliases.9606.v9.1.txt
```
In reality the filtered file includes more than only the Human interactions, because it contains any line that has the string 9606 in any column. 
We can explore better ways to filter it but for the purposes of this example the command above is enough because the file now is smaller (~170Mb unzipped) and we will execute another filter to restrict the network to the proteins of interest.   

The format of the file is tab separated were the first column is the taxonomy ID, the second column is the Ensembl protein ID, and any subsequent column contains an alias in different databases.
For example the line that contains information for the Ensemble protein ID ENSP00000332790 in human (9606) looks like this:
```
9606	ENSP00000332790	Q8IUE6	BLAST_KEGG_DBLINKS_UniProt BLAST_UniProt_AC Ensembl_HGNC_UniProt_ID_(mapped_data_supplied_by_UniProt) Ensembl_HGNC_UniProt_ID_(mapped_data_supplied_by_UniProt)_AC Ensembl_UniProt_AC
```
Here is a simple python function that receives the content of the file and create dictionaries (i.e. Hashmap tables) to map between Uniprot and Ensembl protein IDs:
```python
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
```python
The parameter query in this function is the list of proteins that you are interested on. In this way the resultant map includes only relevant information. You can create this list by filtering your feature's file. See the next python function as an example of how to do it:
```
def getQueryIDs(featuresF):
	query = {}
	featuresF.readline()
	for line in featuresF:
		parts = line.split("\t")
		query[parts[0]] =[]
	query=query.keys()
	return query
```

Creating the Network file
------
Now with all this information we can generate the network file. 
The following function requires a file in ```stringF``` which should be as explained [#header1](above). 
Then going through the lines of the files extract the Ensembl IDs of each interaction, and try to map them to uniprot IDs with the previously created dictionary.
If the mapping is OK, then it rewrites this line in the output file (```N_outputF```) using UniProt IDs. 

```python
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
```

Enrichment of your annotations with UniProt features
-----
It is possible to get information programatically through the REST services of UniProt and you can use this information to enrich the annotations you already have.
For instance with this link http://www.uniprot.org/uniprot/?query=organism:9606&columns=id,database(ensembl),genes,go-id,go&format=tab you get a tab separated file of all the human proteins including: UniProt Id, Ensemble IDs, Gene names, GO IDs and GO terms.

Using a similar function as the one to get the mapping between IDs, we can load the Uniprot data from the request:
```python
def getUniprotMap(uniprotF,query):
	UniprotMap ={}
	for line in uniprotF:
		parts = line.split("\t")
		if parts[0] in query:
			UniprotMap[parts[0]]= [x.strip() for x in parts[2:]]
	return UniprotMap
```

And then we can write a function that writes the annotations in your file plus the ones from the UniProt REST file.

```python
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
```

Putting this pieces together
-----

The pyhton script provided [here](string2pinv.py) takes 6 parameter when executed through the command line:
 * *Annotations File*: File path to the annotations of the proteins you are interested. 
 * *Protein Aliases*: File path to the STRING file that contains the aliases to other IDs.
 * *String File*: File path to the string data.
 * *Uniprot Features*: Path to the file from the Uniprot REST services in a tab deliminated format.
 * *Features Output File*: Path to the new features file formatted to PINV
 * *Interactions Output File*: Path to the new interactions file formatted to PINV

It goes thorough the STRING file, maps the IDs to UniProtKB, and filters the network to include only the interactions between the proteins included in the query file.

Run with:
```
python string2pinv.py <Annotations_File> <protein_aliases> <String_File> <Uniprot_Features> <Features_Output_File> <Interactions_Output_File>     
```

 