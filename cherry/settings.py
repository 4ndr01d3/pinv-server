import socket
if socket.gethostname() == 'biosual':
    TEST = False
    SOLR_BASE="/srv/solr/solr/cores" 
    SOLR_SERVER = "http://biosual.cbio.uct.ac.za:8983"
else:
    TEST = True
    SOLR_BASE="/Users/4ndr01d3/git/pinv-server/solr4/solr/cores"
    SOLR_SERVER = "http://localhost:8983"

#CORENAME="PINV_smegmatis"
#CORENAME="Subnetwork_MTB_MLP_MSM"
#CORENAME="PINV_leprae"
CORENAME="test"

ANNOTATIONS_FILE="../data/%s_annot.txt"%CORENAME
NETWORK_FILE="../data/%s.txt"%CORENAME

SOLR_URL='%s/solr/%s'%(SOLR_SERVER,CORENAME)


    
