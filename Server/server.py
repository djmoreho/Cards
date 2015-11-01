#### NON ENCRYPTION SSL VERSION 
#### DO NOT SUBMIT SENSITIVE INFORMATION
#### UNLESS YOU ARE DOING IT THROUGH THE LOOPBACK DEVICE

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
reactor.listenTCP(8080, site)
reactor.run()