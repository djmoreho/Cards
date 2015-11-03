## CardResources.py  (our custom Resources, not to be confused with Twisteds)
## This way we can keep the crypto out of this file
## and hopefully make life easier.
## Naming Conventions: PEP 08 and PEP 20

### LOGGING
from twisted.python import log

### TEMPLATES
from twisted.web.template import Element, renderer, XMLFile, tags, TagLoader, Comment
from twisted.web.template import flatten

### RESOURCES
import twisted.web
from twisted.web.server import Site
from twisted.web.server import NOT_DONE_YET # magic value for persistant connection
from twisted.web.static import File
from twisted.web.resource import Resource, NoResource
from twisted.web.util import redirectTo

### REACTOR
from twisted.internet import reactor


### API

class CardsResource(Resource):

    def render(self, request):
        print "CR"
        s = request.getSession()
        print s
        return Resource.render(self, request)


class API(CardsResource):
    '''Virtual Directory for api'''
    isLeaf = False
    def render_GET(self, request):
        return "<html><h1>API</h1></html>"


class Users(CardsResource):
    '''Renders a users page'''
    isLeaf = False
    def render_GET(self, request):
        return "<html><h1>User</h1></html>"

class Game(CardsResource):
    '''Renders the game app'''
    isLeaf = False
    def render_GET(self, request):
        return "<html><h1>Game</h1></html>"

class PersistantExample(CardsResource):
    '''Gives an example of a persistant request'''
    isLeaf = True
    def render_GET(self, request):
        log.msg("Ooooh a render request")
        # schedule the reoccuring thing (this could be something else like a deferred result)
        reactor.callLater(1.1, self.keeps_going, request, 0) # 1.1 seconds just to show it can take floats
        request.responseHeaders.addRawHeader("Content-Type", "text/html; charset=utf-8") # set the MIME header
        request.responseHeaders.addRawHeader("Connection", "keep-alive")
        #request.responseHeaders.addRawHeader("Content-Length", "700")
        # firefox requirest the char set see https://bugzilla.mozilla.org/show_bug.cgi?id=647203
        request.write("<html>\n<title>PE</title>\n<body>")
        return NOT_DONE_YET


    def keeps_going(self, request, i):
        log.msg("I'm going again....")
        i = i + 1
        request.write("\n<br> This is the %sth time I've written. </br>" % i) ## probably not best to use <br> tag
        
        if i < 5:
            reactor.callLater(1.1, self.keeps_going, request, i) # 1.1 seconds just to show it can take floats
        if i >= 5 and not request.finished:
            request.write("\n</body>")
            request.write("\n</html>")
            # safari will only render when finished
            request.finish()

class AndrewExample(CardsResource):
    '''Gives an example of a persistant request'''
    isLeaf = True
    def render_GET(self, request):
        '''
        request.responseHeaders.addRawHeader("Content-Type", "text; charset=utf-8") # set the MIME header
        d = {}
        d["success"] = True
        d["hand"] = True
        d["data"] = [1, 2, 5, 7, 674, 6]

        import json
        s = json.dumps(d)
        print s
        return s
        '''
        html = '''
        <form action="ae" method="post">
        First name:<br>
        <input type="text" name="firstname" value="Mickey">
        <br>
        Last name:<br>
        <input type="text" name="lastname" value="Mouse">
        <br><br>
        <input type="submit" value="Submit">
        </form> 
        '''
        return html


    def render_POST(self, request):
        request.responseHeaders.addRawHeader("Content-Type", "text; charset=utf-8") # set the MIME header        
        args = request.args
        f = args["firstname"][0]
        l = args["lastname"][0]
        import json
        if f.lower() == "donald" and l.lower() == "duck":
            d = {}
            d["valid"] = True
            return json.dumps(d)

        else:
            d = {}
            d["valid"] = False
            return json.dumps(d)



## HOME PAGE

class Home(CardsResource):
    isLeaf = False
    def render_GET(self, request):
        return "<html><center><h1>Hi!</h1><img src=\"logo.png\" width=\"400\"></center></html>"



def Create(root):
    ## probably should find a better name for this function
    logo = File("/Users/davidmorehouse/Desktop/platypus-logo-anni-2.png")
    api = API();

    # various representions of the home page
    root.putChild("", root)
    root.putChild("index.html", root)
    root.putChild("index", root)

    root.putChild("pe", PersistantExample())
    root.putChild("ae", AndrewExample())
    root.putChild("test", File("test.html"))
    # platypus image
    root.putChild("logo.png", logo)

    # app specific pages
    root.putChild("user", Users())
    root.putChild("game", Game())


    # api
    root.putChild("api", api)
