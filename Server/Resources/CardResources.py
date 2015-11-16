## CardResources.py  (our custom Resources, not to be confused with Twisteds)
## This way we can keep the crypto out of this file
## and hopefully make life easier.
## Naming Conventions: PEP 08 and PEP 20

import hashlib
import time
import json
import glob
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


INC = 22
IDs = {}
GAMEs = {}
COOKE_TIME_EXPERATION = 2 * 60 * 60
class CookieError(Exception):
    '''Cookie fetching and validation issues'''

# Main Resource, deals with certain things that have to be setup
class CardsResource(Resource):
    pass
'''
    def render(self, request):
        try:
            id = self.getPlatypusCookie(request)
        except CookieError:
            try:
                redirect_number = int(request.args["redirect"][0])
            except:
                redirect_number = 0
            self.setPlatypusCookie(request)
            print dir(self)
            print dir(request)
            url = request.sibLink("?redirect=%s" % (redirect_number+1))
            print type(url)
            print url
            url = request.childLink("?redirect=%s" % (redirect_number+1))
            print url

            url = request.prePathURL()
            print type(url)
            print url
            url = request.URLPath()
            print dir(url)
            print type(url)
            print url

            raise IOError

            redirectTo(url, request)
            request.finish()
        else:
            return Resource.render(self, request) 
        
        print "Underlying render code"
        not_in_db = not IDs.has_key(cookie)
        if cookie == None or not_in_db:

            IDs[cookie] = []
            expiration_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time() + 3600 * 2))
            request.addCookie("platypus_id", cookie, expiration_time) 

            # httpOnly = True, # not accisable by javascript
        

    def getPlatypusCookie(self, request): # twisted already has a 'getCookie' method
        cookie = request.getCookie("platypus_id")
        if cookie is None:
            raise CookieError("No cookie")

        try:
            id = IDs[cookie]
        except (KeyError, ValueError):
            raise CookieError("Invalid cookie")

        time = it["time"]
        if (time + expiration_time) < int(time.time()):
            raise CookieError("Old cookie")

        # ok valid cookie and all so return it's id object
        return id

    def setPlatypusCookie(self, request):
        # https://www.owasp.org/index.php/Insufficient_Session-ID_Length
        # cookie should be at least 128 bits
        # ours are 256 bits or 32 bytes
        cookie_str = Random.get_random_bytes(32)
        assert len(cookie_str) == 32
        cookie_str = base64.b64encode(cookie_str)
        IDs[cookie_str] = []
        expiration_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time() + 3600 * 2))
        # redirect page an set cookie
        print "Cookie issue."
        request.addCookie("platypus_id", cookie_str)
'''

class GameError(Exception):
    '''Any game error'''

class Game(object):
    verbs = []
    musts = []
    name  = ""
    
    def __init__(self):
        self.called_verbs = []
        self.verbs.append("end_turn")
        self.players = []
        self.current_player = 1

    def verb(self, verb, player = None, *args, **kw):
        self.called_verbs.append(verb.lower())
        print "verb " + str(verb)
        print "player " + str(player)
        print "args " + str(args)
        print "kw " + str(kw)
        print "player list " + str(self.players)
        print "current player " + str(self.current_player)
        if player is not None:
            player = int(player)

        if (player in self.players and self.current_player == player) or player is None:
            s = "verb_%s" % verb.lower()
            h = getattr(self, s)

            if player is None:
                ret = h(*args, **kw)
            else:
                ret = h(player, *args, **kw)
            return ret
        else:
            raise GameError("Not your turn!")
    def check_musts(self, player):
        c = list(called_verbs)
        for i in musts:
            if i not in c:
                raise GameError("You have not done everything you need to.")
        return

    def verb_EX(self, player):
        print ex # do your stuff

    def verb_end_turn(self, player):
        self.check_musts(player)
        # find next player
        for n,i in enumerate(self.players):
            if i > player:
                break

        self.current_player = self.players[n]

#from Games.TexasHoldemGameState import GameState

from Games.TexasHoldem import score
from Games.TexasHoldem import getHands, generateDeck

class Poker(Game):
    verbs = ["bet", "fold", "add_player", "score", "river"]
    name = "poker"

    def __init__(self):
        Game.__init__(self)
        #self.gs = GameState() # can have optional logic outside class
        self.bets = []
        self.deck = generateDeck()
        self.hands = []
        self.river = []
        # we cheat here with a just horrible hack
        # because all the cards are randomly distributed
        # we can actually calculate the river first
        # and have 'false' animation interactions
        # god help me
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())
        self.river.append(self.deck.pop())

        self.river_rounds = 0

    def check_musts(self, player):
        print "Checking..."
        # if either are in there
        if "bet" in self.called_verbs:
            return
        if "fold" in self.called_verbs:
            return
        raise GameError("You have not done everything you need to do.")

    def verb_end_turn(self, player):
        Game.verb_end_turn(self, player)
        # last man standing?
        if len(self.players) == 1:
            print "Last man"

        if player == self.players[-1]:
            self.river_rounds = self.river_rounds + 1

    def verb_add_player(self):
        if len(self.deck) < 2:
            raise GameError("Not enough cards")

        try:
            self.players.append(self.players[-1] + 1)
        except IndexError:
            self.players.append(1)
        self.bets.append(5000)
        hand = []
        hand.append(self.deck.pop()) # god help me
        hand.append(self.deck.pop()) # god help me
        self.hands.append(hand)
        return [hand, 5000]

    def verb_fold(self, player):
        self.players.remove(player)
        self.verb_end_turn(player)# end their turn for them

    def verb_score(self): # not sure how this one will work
        fold = list(bids)
        for n, i in enumerate(fold):
            fold[n] = False # false means folded; god help me

        for i in players:
            fold[i-1] = True# these are the guys that didn't fold
        #(bidArr, canWin, numPlayers, river, hands):
        s = score(self.bets, fold, len(self.bets), self.river, self.hands)

    def verb_bet(self, player, amount):
        #
        # BROKEN!!!!
        #self.gs.takeBids(player, bid_amount)
        amount = int(amount)
        player = int(player)
        print "Bet " + str(self.bets)
        print "Players " + str(self.players)
        print "Player" + str(player)
        b = self.bets[player - 1]
        print "Amount player has " + str(b)
        print "Amount being bet " + str(amount)
        if amount > b:
            raise GameError("Too big of a bet!")

        b = b - amount
        self.bets[player - 1] = b
        return b

    def verb_river(self):
        if self.river_rounds == 0:
            return []
        elif self.river_rounds == 1:
            return self.river[:3]
        elif self.river_rounds == 2:
            return self.river[:4]
        elif self.river_rounds == 3:
            return self.river




p = Poker()

class API(Resource):
    '''Virtual Directory for api'''
    isLeaf = True
    def render_GET(self, request):
        return self.render_POST(request) # cheat for easy debugging

    def render_POST(self, request):
        # on the last version "Well at least we can delete this abomination"
        action = request.args["action"][0]
        game   = request.args["game"][0]# later we can move this to virtual directories
        other_args = dict(request.args)
        other_args.pop("action")
        other_args.pop("game")
        processed_args = {}
        for k in other_args.keys():
            processed_args[k] = other_args[k][0]
        print processed_args
        x = p.verb(action, **processed_args)
        return "<html> <body> <code> %s </code> </body> </html>" % (x)

### API
from Games.TexasHoldem import getHands, generateDeck
class TH4Player(object):

    def __init__(self):
        self.deck = generateDeck()
        self.hands = getHands(4, 2, self.deck)
        ri = 4 * 2
        self.river = self.hands[ri:ri+5]
        self.money = [5000, 5000, 5000, 5000]
        self.player_count = 0
        self.players = []
        self.round = 0

    def reg_player(self, id):
        self.player_count = self.player_count + 1
        self.players.append(id)

    def get_hand(self, player):
        return self.hands[player]

    def inc_round(self ):
        self.round = self.round + 1

    def get_river(self):
        return self.river[self.round]

    def do_bet(self, player, amount):
        give = self.amount[player]
        if give > amount:
            give = give - amount
            self.amount[player] = give
            print "Player %s has %s left" % (player, give)
            return give
        else:
            raise RuntimeError("Too big of a bet")

i = 0
'''
class API(CardsResource):
    isLeaf = False
    def render_GET(self, request):
        return "<html><h1>API</h1></html>"

    def render_POST(self, request):
        print request.args
        if request.args["type"][0] == "pa":
            v = request.args["verb"][0]
            if v == "bet":
                try:
                    amount = request.args["amount"]
                    cookie = request.getCookie("platypus_id")
                    print "GOT COOKIE"
                    print IDs
                    print IDs[cookie]
                    game_id = IDs[cookie][0]
                    g = GAMEs[game_id]
                    give = g.do_bet(int(amount))
                except:
                    log.err()
                    d = {}
                    d["success"] = False
                    d["reason"] = "Too big of a bet"
                else:
                    d = {}
                    d["success"] = True
                    d["amount"] = give
                str = json.dumps(d)
                return str

            if v == "draw":
                try:
                    cookie = request.getCookie("platypus_id")
                    print "GOT COOKIE"
                    print IDs
                    print IDs[cookie]
                    game_id = IDs[cookie][0]
                    g = GAMEs[game_id]
                    p = g.players.index(cookie)
                    print "GAME ID"
                    print game_id
                    print "PLAYERs"
                    print p
                    hand = g.get_hand(int(p))
                except:
                    log.err()
                    d = {}
                    d["success"] = False
                    d["reason"] = "Unkown"
                else:
                    d = {}
                    d["success"] = True
                    d["hand"] = hand
                    global i
                    i = i + 1
                    print "i\n\n\n\n\n\n\n\n\n\n"
                    print i
                    if i == 1:
                        d["images"] = ["card_images/ace_of_clubs.png", "card_images/jack_of_hearts.png"]
                    else:
                        d["images"] = ["card_images/2_of_clubs.png", "card_images/ace_of_hearts.png"]
                    """
                    for i in hand:
                        p = list(i)
                        s = "html/card_images/%s*_of_%s*.png" % (p[1].lower(), p[0].lower())
                        print s
                        print glob.glob(s)
                        print glob.glob(s)[0]
                        print glob.glob(s)[0].replace("html/", "")
                        d["images"].append( glob.glob(s)[0].replace("html/", ""))
                    """
                str = json.dumps(d)
                print str
                return str
                
        return str(request.args)
'''

class Users(CardsResource):
    '''Renders a users page'''
    isLeaf = False
    def render_GET(self, request):
        return "<html><h1>User</h1></html>"

class GameResource(CardsResource):
    '''Renders the game app'''
    isLeaf = False
    def render_GET(self, request):
        a = request.args
        try:
            id = a["gid"]
            c = request.getCookie("platypus_id")
            assert c != None
        except:
            log.err()
        else:
            print "ID - GAME"
            print id
            print c

        print IDs
        IDs[c].append(c)
        print IDs
        try:
            g = GAMEs[c]
            g.reg_player(c)
        except:
            g = TH4Player()
            GAMEs[c] = g
            g.reg_player(c)

        return File("html/game.html").render_GET(request)

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


    # api
    root.putChild("api", api)

    import glob
    for i in glob.glob("html/*"):
        print i
        root.putChild(i.replace("html/", ""), File(i))