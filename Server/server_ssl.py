#### ENCRYPTION SSL VERSION 
#### DO NOT SUBMIT TO GITHUB

import twisted
from twisted.python import log
import sys

log.startLogging(sys.stdout)
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.internet import reactor, ssl
import OpenSSL


class Site(Site):
    pass

from Resources.CardResources import Home, Create
root = Home()
site = Site(root)
## now load other resources
Create(root)

# listen
if __name__ == "__main__":
    # load private key
    import import OpenSSL.crypto  # py open ssl
    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM,
                                  samplePEMKey,
                                  passphrase=)



    context_factory = ssl.DefaultOpenSSLContextFactory(
        "",
        "", 
        sslmethod=OpenSSL.SSL.TLSv1_2_METHOD # TLS v 1.2 Prevent BEAST and CRIME attacks
    )
    ## ADD what algorithms to use
    reactor.listenSSL(8000, site,
                      context_factory)
    reactor.run()