PINV Server 
====

Installation
====


The following 3rd part modules need to be installed. Advised to install under a virtualenv:
To install virtualenv check [this link](http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation)

```
virtualenv --python=python2.7 env
source env/bin/activate

pip install cherrypy
pip install sunburnt
pip install httplib2
pip install mako
pip install lxml
```


Known Problems
----

lxml doesn'r seem to play along with virtualenv [See More](http://stackoverflow.com/questions/13019942/why-cant-i-get-pip-install-lxml-to-work-within-a-virtualenv).
For Mac I installed from a [Mac Port](http://www.macports.org/):
```
sudo port install py27-lxml

```

Configuration
====
The file ```[pinv-server]/cherrypy/settings.py``` requires to point to the right path were the solr instance is.

Starting
====
start with 
```
source env/bin/activate
./proxy.py
```


