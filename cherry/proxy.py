#!/usr/bin/env python
import os
import settings
import time
import hashlib

# PINV modules
import pinv
import settings
import auth
from pinv import InteractionNetwork

# 3rd party modules
import sunburnt
import cherrypy
from cherrypy import _cperror
import httplib2
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['html'])

SOLR="http://127.0.0.1:8983"

cherrypy.server.max_request_body_size=1048576000
localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

def check_request(rq):
    parts = rq.path_info.split("/")
    if len(parts) <=3:
        return False
    if parts[3] == "select":
        print "-----PASSED------ SELECT",parts
        return True
    if len(parts) > 3 and parts[3] == "admin" and parts[4] == "luke":
        print "-----PASSED------ ADMIN, LUKE",parts
        return True
    if len(parts) > 3 and parts[2] == "admin" and parts[3] == "cores":
        print "-----PASSED------ ADMIN, CORES",parts
        if "action" in rq.params and rq.params["action"] == "UNLOAD":
            if "key" not in rq.params or "core" not in rq.params:
                print "FAILED: no key provided"
                return False
            elif auth.check_delete_key(rq.params["core"], rq.params["key"]):
                print "ALLOWED!"
                return True
            else:
                print "FAILED: auth_check_failed"
                return False
        return True
    print "-----FAILED------ CHECK_PATHS failed for",parts
    return False

def remove_jsonwrf(json_text):
    json_text = json_text.strip()
    p1 = json_text.find("(")
    p2 = json_text.rfind(")")
    if p2==len(json_text)-1:
        return (json_text[p1+1:-1],json_text[:p1])
    else:
        return (json_text, None)

def strip_private_cores(json_response, blacklist):
    import json
    cherrypy.log(str(type(json_response)))
    json_text, wrf = remove_jsonwrf(json_response)
    json_obj = json.loads(json_text)
    cores ={}
    for core in json_obj["status"]:
        if core not in blacklist:
            cores[core] =json_obj["status"][core]
    json_obj["status"] = cores
    json_text_filtered = json.dumps(json_obj)
    if wrf != None:
        return wrf+"("+json_text_filtered+")"
    return json_text_filtered
     
class PinvProxy(object):
    def preprocess(self=None):
        # route depending on url
        #cherrypy.log("*** preprocess (before_handler) ***")
        if cherrypy.request.path_info.startswith("/solr"):
            #cherrypy.log("Routing to SOLR server")
            rq = cherrypy.request
            parts = rq.path_info.split("/")
            if not check_request(cherrypy.request):
                raise cherrypy.HTTPError(403)
            core_name = parts[2]
            operation = parts[3]
            h = httplib2.Http()
            URL = SOLR+cherrypy.request.path_info+"?"+cherrypy.request.query_string
            if auth.is_private(core_name):
                if "key" in rq.params and auth.check_key(core_name, rq.params["key"]):
                    pass
                else:
                    raise cherrypy.HTTPError(403)                    
            else:
                pass
            resp, content = h.request(URL, "GET")
            cherrypy.request.handler=None
            cherrypy.response.body=content
            cherrypy.response.status = resp["status"]
            print dir(cherrypy.response)
            return content
        else:
            pass # do nothing
    def postprocess(self=None):
        # route depending on uri
        #cherrypy.log("*** postprocess (before_handler) ***")
        params = cherrypy.request.params
        print cherrypy.request.path_info
        if "json.wrf" in params and "q" in params and cherrypy.request.path_info.startswith("/solr/admin/cores"):
            print ">>>>>>>>>>>> json.wrf found"
            response_body = cherrypy.response.collapse_body()
            #import IPython
            #IPython.embed()
            try:
                filteredjson = strip_private_cores(response_body,auth.private_cores())
                #filteredjson = response_body
            except:
                cherrypy.log("EXCEPTION in stripping json!")
                return response_body
            cherrypy.response.body = [filteredjson]
            cherrypy.response.handler=None
            rsp = cherrypy.response
            req = cherrypy.request
            #import IPython
            #IPython.embed()
            return filteredjson
        else:
            print ">>>>>>>>>>>>>>>>>>"

    def final_logging(self=None): 
            """This happens *after* the response has been sent to the client"""
            pass

    def __init__(self):
        cherrypy.log(repr(cherrypy.config))
        cherrypy.tools.preprocess = cherrypy.Tool('before_handler', self.preprocess, priority=60)
        cherrypy.tools.postprocess = cherrypy.Tool('before_finalize', self.postprocess, priority=60)
        cherrypy.tools.final_logging = cherrypy.Tool('on_end_request', self.final_logging, priority=60)
    def handle_error():
        cherrypy.response.status = 500
        tmpl = lookup.get_template("error.mako")      
        details=_cperror.format_exc().replace("\n","<br/>")
        return tmpl.render(details=details)        
    _cp_config = {'request.error_response': handle_error}
    @cherrypy.expose
    def default(self, attr='abc'):
        cherrypy.response.status = 404
        tmpl = lookup.get_template("404.mako")
        return tmpl.render()
    @cherrypy.expose
    def index(self):
        tmpl = lookup.get_template("index.mako")
        message = ""
        return tmpl.render(message=message)
    @cherrypy.expose
    def settings_form(self):
        tmpl = lookup.get_template("settings_form.mako")
        return tmpl.render()
    @cherrypy.expose
    def save_settings(self, json_settings):
        #cherrypy.log("*** save_settings ***")        
        json_cleaned = json_settings.strip()
        m = hashlib.md5()
        m.update(json_cleaned)
        hash = m.hexdigest() + ".json"
        fout = open(os.path.join("saves",hash),"wt")
        fout.write(json_cleaned)
        fout.close()
        return hash
    
    @cherrypy.expose
    def clusterize(self,network_name):
        return pinv.clusterCore(network_name)
    
    @cherrypy.expose
    def upload(self, network_name=None, network_file=None, annotations_file=None, type="public", email="pinv.biosual@gmail.com"):
        #cherrypy.log("Privacy: "+ type)
        #cherrypy.log("annotations: "+ repr(network_file))
        #cherrypy.log("network: "+ repr(annotations_file))
        if cherrypy.request.method == "GET":
            tmpl = lookup.get_template("upload_form.mako")
            return tmpl.render() 
        else:
            network_name = pinv.clean(network_name)
            solr_url = '%s/solr/%s'%(settings.SOLR_SERVER,network_name)
            time.sleep(2)
            inv = InteractionNetwork(network_name, "description text", network_file.file, annotations_file.file)
            time.sleep(2)
            message, result = pinv.create_new_solr(network_name)
            time.sleep(2)
            #cherrypy.log("*** UPLOAD. Connecting to: "+ solr_url)
            si = sunburnt.SolrInterface(solr_url)
            time.sleep(2)
            inv.upload(si)
            if type == "private":
                view_key, delete_key = auth.save_key(network_name, email)
                view_url = "http://biosual.cbio.uct.ac.za/pinViewer.html?core=%(core)s&key=%(key)s" % {'core':network_name,'key':view_key}
                delete_url = "http://biosual.cbio.uct.ac.za/solr/admin/cores?action=UNLOAD&deleteIndex=true&core=%(core)s&key=%(key)s" % {'core':network_name,'key':delete_key}
                auth.sendmail(email,view_url, delete_url,network_name)
            errormessage = "<br/>".join(inv.errors)
            tmpl = lookup.get_template("upload_result.mako")
            return tmpl.render(network_name=network_name, 
                               annotation_head="|".join(inv.ahead), 
                               annotation_count=len(inv.annotations),
                               annotation_file=annotations_file.filename,
                               network_head="|".join(inv.nhead), 
                               network_count=len(inv.network),
                               network_file=network_file.filename,
                               message="",
                               errors="<br/>".join(inv.errors))

app=PinvProxy()
cherrypy.quickstart(app, config="pinv.config")
