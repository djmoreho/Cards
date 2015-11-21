#### NON ENCRYPTION SSL VERSION 
#### DO NOT SUBMIT SENSITIVE INFORMATION
#### UNLESS YOU ARE DOING IT THROUGH THE LOOPBACK DEVICE

### TO RUN
## DOWNLOAD PYTHON AND VIRTUALENV (you will only have to do this once!)
# > setup the virtualenv (sudo pip install virtualenv)
# > virtualenv cards
# > source cards/bin/activate

## OK NOW YOU HAVE A VIRTUAL ENV
## TO INSTALL THE LIBARIES USED JUST RUN
## USING THE reqs.txt on the Git Repo
## (you will only have to do this when we add libaries)
# > pip install -r reqs.txt


import twisted
from twisted.python import log
import sys

log.startLogging(sys.stdout)
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.internet import reactor


class Site(Site):
    pass

from CardResources import Home, Create
root = Home()
site = Site(root)
## now load other resources
Create(root)

# listen
if __name__ == "__main__":
    reactor.listenTCP(8080, site)
    reactor.run()
