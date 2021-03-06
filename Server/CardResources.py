## CardResources.py  (our custom Resources, not to be confused with Twisteds)
## Naming Conventions: PEP 08 and PEP 20

import hashlib
import time
import json
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

from Crypto import Random
import base64
import urlparse
import urllib
import time

## our files
from Games import GameError, GAMES_LIST


CookieIDsDict = {}
GameIDDict = {}
COOKE_TIME_EXPERATION = 2 * 60 * 60
class CookieError(Exception):
    '''Cookie fetching and validation issues'''

# Main Resource, deals with certain things that have to be setup
class CardsResource(Resource):
    def render(self, request):
        try:
            id = getPlatypusCookie(request)
        except CookieError:
            print "There was a cookie issue"
            try:
                redirect_number = int(request.args["redirect"][0])
            except:
                redirect_number = 1

            print "Redirect number ",
            print int(redirect_number)


            if redirect_number < 6:
                print "Setting cookie"
                setPlatypusCookie(request)
                url = str(request.uri)
                url = self.appendToURL(url, {"redirect":str(redirect_number)})
                print "Redirect url is ",
                print str(url)
                redirectTo(url, request)
                request.finish()
                return NOT_DONE_YET # though we are

            else:
                request.write("<h2> You're request couldn't be completed.")
                request.finish()
                return NOT_DONE_YET# though we are

        else:
            try:
                return Resource.render(self, request) 
            except:
                log.err()
                return "<html> <body><h2>Sorry we could not process your request.</h2></body> </html>"
        '''       
        print "Underlying render code"
        not_in_db = not CookieIDsDict.has_key(id)
        if id == None or not_in_db:

            CookieIDsDict[id] = []
            expiration_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time() + 3600 * 2))
            request.addCookie("platypus_id", id, expiration_time) 

            # httpOnly = True, # not accisable by javascript
        '''
    def appendToURL(self, url, params):
        print url
        print params
        url_parts = list(urlparse.urlparse(url))
        print url_parts
        query = dict(urlparse.parse_qsl(url_parts[4]))
        print url_parts[4]
        print query
        query.update(params)
        print query

        url_parts[4] = urllib.urlencode(query)
        print url_parts
        return str(urlparse.urlunparse(url_parts))


# cookie utils
def getPlatypusCookie(request): # twisted already has a 'getCookie' method
    cookie = request.getCookie("platypus_id")
    if cookie is None:
        raise CookieError("No cookie")

    try:
        print CookieIDsDict
        id = CookieIDsDict[cookie]
        print id
        cookie_set_time = id["time"]
        if (cookie_set_time + COOKE_TIME_EXPERATION) < int(time.time()):
            raise CookieError("Old cookie")
    except (KeyError, ValueError):
        raise CookieError("Invalid cookie")

    # valid cookie; update time
    id["time"] = time.time()
    
    return cookie

def setPlatypusCookie(request):
    # https://www.owasp.org/index.php/Insufficient_Session-ID_Length
    # cookie should be at least 128 bits
    # ours are 256 bits or 32 bytes
    cookie_str = Random.get_random_bytes(32)
    assert len(cookie_str) == 32
    cookie_str = base64.b64encode(cookie_str)
    CookieIDsDict[cookie_str] = {}
    CookieIDsDict[cookie_str]["time"] = time.time() # time cookie was set
    CookieIDsDict[cookie_str]["games"] = {} # stores all the players games they are in mapping game_id -> player number
    expiration_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time() + 3600 * 2))
    # redirect page an set cookie
    print "Cookie issue."
    request.addCookie("platypus_id", cookie_str)


class CookiePage(CardsResource):

    def render_GET(self, request):
        request.write("<html>")
        request.write("<body>")
        request.write("<h1>")
        request.write("Cookie Information Page")
        request.write("</h1>")
        request.write("<p>")
        request.write("Your cookie id: ")
        try:
            cookie = getPlatypusCookie(request)
            request.write("<code>")
            request.write(cookie)
            request.write("</code>")
        except CookieError:
            request.write("None")
        request.write("</p>")
        request.write("<p>")
        request.write("Cookie was set at ")
        import datetime
        try:
            cookie = getPlatypusCookie(request)
            time = CookieIDsDict[cookie]["time"]
            formatted_time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
            request.write("<code>")
            request.write(formatted_time)
            request.write("</code>")
        except CookieError:
            request.write("unkown")
        request.write("</p>")
        request.write("<p>")
        request.write("You're involved in ")
        try:
            cookie = getPlatypusCookie(request)
            games = CookieIDsDict[cookie]["games"]
            request.write(str(len(games.keys())))
            request.write(" games.")
            request.write("<br/><div>")
            for id in games:
                v = GameIDDict[id]["game"]
                request.write("<code>%s</code>" % str(v))
                request.write("<br/>")
                request.write("<p>I am player number %s</p>" % str(games[id]))

            request.write("</div>")

        except (CookieError, KeyError, ValueError):
            request.write("0 games.")
        request.write("</p>")

        request.write("</body>")
        request.write("</html>")
        request.finish()

        return NOT_DONE_YET

class API(Resource):
    '''Virtual Directory for api'''
    isLeaf = True

    def render(self, request):

        try:
            return Resource.render(self, request)
        except:
            log.err()
            return """{"message": "We were unable to handle your api request.", "success": false}"""

    def render_GET(self, request):
        return self.render_POST(request) # cheat for easy debugging

    def render_POST(self, request):
        request.responseHeaders.addRawHeader("Content-Type", "application/javascript; charset=utf-8")
        # on the last version "Well at least we can delete this abomination"
        action  = request.args["action"][0]
        game    = request.args["game"][0]# later we can move this to virtual directories
        game_id = request.args["gid"][0]# later we can move this to virtual directories
        cookie = getPlatypusCookie(request)
        print CookieIDsDict[cookie]["games"]
        player_number = CookieIDsDict[cookie]["games"][game_id]


        other_args = dict(request.args)
        # remove the special vars
        other_args.pop("action")
        other_args.pop("game")
        other_args.pop("gid")


        processed_args = {}
        for k in other_args.keys():
            processed_args[k] = other_args[k][0]
        print processed_args
        try:
            player = int(CookieIDsDict[cookie]["games"][game_id])
            game_object = getGame(game_id)
            result = game_object.verb(action, player, **processed_args)
        except GameError as ex:
            log.err(ex)
            d = """{"message": "%s", "success": false}""" % ex.message
        except:
            log.err()
            d = """{"message": "We were unable to handle your api request.", "success": false}"""
        else:
            d = {}
            d["success"] = True
            d["message"] = "Succesfully handled api request."
            d["result"] = result
            log.msg("result asdfasdfasfasf")
            log.msg(str(d))
            log.msg(str(result))
            d = json.dumps(d)

        return d

class DebugAPI(API):

    def render_POST(self, request):
        d = API.render_POST(self, request)

        action  = request.args["action"][0]
        game    = request.args["game"][0]# later we can move this to virtual directories
        game_id = request.args["gid"][0]# later we can move this to virtual directories
        cookie = getPlatypusCookie(request)
        player_number = CookieIDsDict[cookie]["games"][game_id]


        request.responseHeaders.addRawHeader("Content-Type", "text/html; charset=utf-8")
        return """<html> <body> <code>
               <p>Action: %s</p> <p>Game: %s</p> <p>Game ID: %s</p> <p>Player Number: %s</p> 
               </code>
               <p>Result: 
               <code>
               %s
               </code> 
               <p>
               </body> </html>""" % (str(action), str(game),
                                     str(game_id), str(player_number), 
                                     str(d))

class Users(CardsResource):
    '''Renders a users page'''
    isLeaf = False
    def render_GET(self, request):
        return "<html><h1>User</h1></html>"


def getGame(id):
    ''' Returns a game object associated with a game id '''
    game  = GameIDDict[id]
    return game["game"]

def createGame(id, game_object):
    ''''Sets up a game object '''
    GameIDDict[id] = {}
    GameIDDict[id]["game"] = game_object # mapping to game interactivity for api

class GameResource(CardsResource):
    '''Renders the game app'''
    isLeaf = False
    def render_GET(self, request):
        a = request.args
        game_id = a["gid"][0]
        cookie = getPlatypusCookie(request)
        type = str(a["gtype"][0]).lower()
        try:
            game_object = getGame(game_id)
            print game_object
        except KeyError:
            # no game to be found, we need to create it
            game_object = GAMES_LIST[type]()
            createGame(game_id, game_object)
        # check to see if the user is already part of this game
        if game_id in CookieIDsDict[cookie]["games"]:
            pass# do nothing
        else:
            details = game_object.add_player()
            CookieIDsDict[cookie]["games"][game_id] = details[0] # map player id

        if type == "poker":
            return File("html/poker.html").render_GET(request)
        elif type == "war":
            return File("html/war.html").render_GET(request)
        else:
            return "<html><body><h2>Unable to render game %s</h2</body></html>" % type

class PersistantExample(CardsResource):
    '''Gives an example of a persistant request'''
    # does not exist on Safari until stopping browser / ending connection

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
    root.putChild("game", GameResource())

    root.putChild("cookie_info", CookiePage())

    # api
    root.putChild("api", api)
    root.putChild("debugapi", DebugAPI())

    import glob
    for i in glob.glob("html/*"):
        print i
        root.putChild(i.replace("html/", ""), File(i))