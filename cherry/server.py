#!/usr/bin/python -u
import os
import cherrypy
import pinv
import settings
from pinv import InteractionNetwork
import sunburnt
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=[''])
import time
import hashlib

cherrypy.server.max_request_body_size=1048576000

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

class FileDemo(object):
    @cherrypy.expose
    def index(self):
        print "--- cherrypy --- index requested"
        tmpl = lookup.get_template("index.mako")
        message = ""    
        return tmpl.render(message=message)
    
    @cherrypy.expose
    def settings_form(self):
        tmpl = lookup.get_template("settings_form.mako")
        return tmpl.render()

    @cherrypy.expose
    def save_settings(self, json_settings):
        json_cleaned = json_settings.strip()
        m = hashlib.md5()
        m.update(json_cleaned)
        hash = m.hexdigest() + ".json"
        fout = open(os.path.join("saves",hash),"wt")
        fout.write(json_cleaned)
        fout.close()
        return hash

    @cherrypy.expose
    def upload(self, network_name, network_file, annotations_file):
        out = """<html>
        <body>
            Network name: %s<br/><br/>
            
            Annotations columns: %s<br/>
            Annotations count: %i<br />
            Annotations filename: %s<br />
            
            Network head: %s<br />
            Network length: %i<br />
            Network filename: %s<br />
            
            %s
                    <br/>
                    Errors:<br/>
                    %s
        </body>
        </html>"""
        network_name = pinv.clean(network_name)
        if settings.TEST and not (network_file.file and annotations_file.file):
            network_file.file = open("../data/test.txt")
            annotations_file.file = open("../data/test_annot.txt")
        solr_url = settings.SOLR_URL
        solr_url = '%s/solr/%s'%(settings.SOLR_SERVER,network_name)
        time.sleep(2)
        inv = InteractionNetwork(network_name, "description text", network_file.file, annotations_file.file)
        time.sleep(2)
        message, result = pinv.create_new_solr(network_name)
        time.sleep(2)
        print "--- UPLOAD. Connecting to:", solr_url        
        si = sunburnt.SolrInterface(solr_url)
        time.sleep(2)
        inv.upload(si)
        errormessage = "<br/>".join(inv.errors)
        return out % (network_name,"|".join(inv.ahead), len(inv.annotations), repr(annotations_file.filename), 
                      "|".join(inv.nhead), len(inv.network), repr(network_file.filename),message,errormessage)

tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(FileDemo(),'/',config={'global':{'server.socket_port':8080, 'cherrypy.tool.CORS.on' : True,
                                                         'server.socket_host':'0.0.0.0'}})    
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(FileDemo())
