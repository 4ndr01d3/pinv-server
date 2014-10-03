Uploading your dataset
======

When you want to upload your dataset into PINV, the server requires 2 files: one tha includes the interactions and one to include anotations on the proteins:

Interactions File
------

The interactions file is a tab delimited file where the first line should start with ```#``` and correspond to the header. It is used to specify the names of each of the columns. 
The first two columns are the accession numbers of the interacting proteins.
Any following column in the file will be consider as score values of some kind of evidence for that interaction, and the last of those scores should be a unified value.

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

Through the Protein Feature File you can enrich the information of your network. Information included here will be used by PINV to provide ways to manipulate the look of your visualization. (e.g. color the nodes by one of the provided features)
The only required feature is the organism that the protein belongs to. **All** the proteins included in the interaction file should be included in the Features File.
The format of the file it is also TAB delimited, where the first line correspond to the headers (it should also starts with the character ```#```).

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


Creating the interactions file from STRING db
======

There are multiple ways to obtain the data from STRING, for this example we will use the flat files available to download in [this link](http://string-db.org/newstring_cgi/show_download_page.pl).
For this example we are selecting the protein network data for the organism *Homo Sapiens*. 
The first lines of this file looks like:
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
The file that STRING provides uses Ensemble Protein IDS, PINV doesn't discriminate which type of accession number do you use for the network, as long as it is consistent with the ids in the features file.
For this example we will create an interaction file that uses UniprotKB accession numbers. It is possible to get this information programatically through the REST services of UniProt, quering protein by protein.
 
In this particular example we have retrieved beforehand all the mappings between the 2 identifiers for proteins in Homo Sapiens using this URL request: http://www.uniprot.org/uniprot/?query=organism:9606&format=tab&columns=id,database(STRING) and save it into a file that looks like this:

```
Entry	Cross-reference (STRING)
P31946	9606.ENSP00000300161;
P62258	9606.ENSP00000264335;
Q04917	9606.ENSP00000248975;
P61981	9606.ENSP00000306330;
P31947	9606.ENSP00000340989;
P27348	9606.ENSP00000238081;
P63104	
P30443	
P01892	
```

Filtering the network with a list of proteins
-----

The pyhton script provided [here](string2pinv.py) takes 4 parameter when executed ina the command line:
 * *String File*: File path to the string data. It uses Ensemble protein identifiers and it is space separated.
 * *Uniprot Mapping*: Path to the file from the Uniprot REST services with tab format
 * *Target Proteins*: Path to the file tha include a list of proteins with uniprot IDs
 * *Output File*: Path to the new file formated to PINV


     