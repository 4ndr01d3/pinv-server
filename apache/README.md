Apache Configuration
=====

The [default](default) File in this directory is an example of the configuration for the apache server that hosts the PINV client in order to map both cherrypy and solr servers and prevent to open other ports than :80

This config also helps to avoid any CORS errors when saving the status' files. 
The important part of this example is the redirection rules for solr and cherrypy:
```
        RewriteEngine on
        RewriteRule ^solr$ /solr [R]
        RewriteRule ^solr(.*) http://localhost:8983/solr$1 [P]
        RewriteRule ^uploader$ /uploader [R]
        RewriteRule ^uploader(.*) http://localhost:8080/$1 [P]
```
This allows to redirect any URL from:
 *  http://[yourserver]/solr/[query] to  http://[yourserver]:8983/solr/[query]
 *  http://[yourserver]/uploader/[query] to  http://[yourserver]:8983/uploader/[query]
 
Also remember to link the folder ```saves``` on apache to the ```cherrypy/saves``` where the statuses are been saved. 
This can be done via symbolic links. See line 6 on the example file: ```Options FollowSymLinks```. 
This allow apache to follow symbolic links, then you can create one under the apache web files :
```
ln -s [pinv-server]/cherrypy/saves [apache_web_dir]/saves
```