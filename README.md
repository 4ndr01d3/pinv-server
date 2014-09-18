PINV server
====

This repository holds the server components that [PINV](http://biosual.cbio.uct.ac.za/pinv.html) requires.

The repo is organize in 4 separate folders:

* **apache**: Contains an example configuration for apache to serve as proxy of cherrypy and solr.
* **php**: PHP script that generates a single JS with all the dependencies and file required on a PINV instance.
* **solr**: Empty SOLR server that ontains the skeleton to support the multicores, and a blank core that is used as template.  
* **cherrypy**: An instance of *cherrypy* that coordinates the upload of new datasets to the solr server, serves as an authentication proxy for protected cores and allow to save the status files for the sharing capabilities of PINV.
 
 Each folder contains a README for further details.
