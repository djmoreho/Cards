## Games.py
from twisted.python import log
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

    def verb(self, verb, player, *args, **kw):
        s = "verb_%s" % verb.lower()
        h = getattr(self, s)

        try:
            ret = h(player, *args, **kw)
            self.called_verbs[player - 1].append(verb.lower())
            return ret
        except TypeError:
            raise GameError("Incorrect arguments")
            


    def check_musts(self, player):
        c = list(self.called_verbs[player-1])
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


from TexasHoldem import score
from TexasHoldem import getHands, generateDeck


class Poker(Game):
    verbs = ["bet", "fold", "score", "river"]
    name = "poker"

    def __init__(self):
        Game.__init__(self)
        #self.gs = GameState() # can have optional logic outside class
        self.bets = []
        self.deck = generateDeck()
        self.hands = []
        self.river = []
        self.called_verbs = []
        self.intial_players = 0
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

    def __str__(self):
        return """Poker(CurrentPlayer=%s,\n
                        IntialPlayers=%s,\n
                        Players=%s,\n
                        Bets=%s,\n
                        Hands=%s,\n
                        Rivers=%s,\n
                        RiverRound=%s)""" % (self.current_player,
                                         self.intial_players,
                                         len(self.players),
                                         self.bets,
                                         self.hands,
                                         self.river,
                                         self.river_rounds)
            
    ## add player, intialize player to game

    def add_player(self):
        """
        returns: [player number, [h1, h2], amount of chips]
        """
        if len(self.deck) < 2:
            raise GameError("Not enough cards")

        self.intial_players = self.intial_players + 1

        try:
            self.players.append(self.players[-1] + 1)
        except IndexError:
            self.players.append(1)

        self.called_verbs.append([])

        self.bets.append(5000)
        hand = []
        hand.append(self.deck.pop()) # god help me
        hand.append(self.deck.pop()) # god help me
        self.hands.append(hand)

        return [self.players[-1], hand, 5000]

    ### Game Verbs    

    def check_musts(self, player):
        # if either are in there
        if "bet" in self.called_verbs[player-1]:
            return
        # need this as check musts ends the turn
        # and we want to allow fold to end a turn
        # so allo check musts to pass    
        if "fold" in self.called_verbs[player-1]:
            return

        raise GameError("You have not done everything you need to do.")

    def verb_player_number(self, player):
        return self.current_player

    def verb_get_player_details(self, player):
        h = self.hands[player - 1]
        b = self.bets[player - 1]
        p = player

        return [h, b, p]

    def verb_end_turn(self, player):
        if self.current_player == player:
            self.check_musts(player)
            # past check musts
            self.called_verbs[player-1] = []
            if self.current_player == self.players[-1]:
                self.river_rounds = self.river_rounds + 1
                self.current_player = self.players[0]
            else:
                # find next player
                for n,i in enumerate(self.players):
                    if i > player:
                        break

                self.current_player = self.players[n]

            return None
        else:
            raise GameError("Not your turn!")

    def verb_fold(self, player):
        if self.current_player == player:
            self.called_verbs[player-1].append("fold")
            self.verb_end_turn(player)# end their turn for them
            new_player_index = self.players.index(self.current_player)
            self.players.remove(self.players[new_player_index - 1])

        else:
            raise GameError("Not your turn!")


    def verb_score(self, player): # not sure how this one will work
        # make sure this is only return at the end
        # last player or everyone has gone in the 3rd round so it's the 4th

        # this does allow the first client to get their score
        # when they first join
        last_player_left = (len(self.players) == 1 and self.intial_players > 1) # make sure it
                                                                                # isn't the only player to have joined

        if last_player_left or self.river_rounds == 3:
            fold = list(self.bets)
            for n, i in enumerate(fold):
                fold[n] = False # false means folded; god help me

            for i in self.players:
                fold[i-1] = True# these are the guys that didn't fold

            #(bidArr, canWin, numPlayers, river, hands):
            s = score(fold, self.river, self.hands)
            return s
        else:
            raise GameError("Not end of game. Scores not available")
        

    def verb_bet(self, player, amount):
        #
        # BROKEN!!!!
        #self.gs.takeBids(player, bid_amount)
        if self.current_player == player:
            amount = int(amount)
            b = self.bets[self.current_player - 1]
            if amount > b or amount < 0:
                # remove the bad bet
                raise GameError("Not a valid bet!")

            b = b - amount
            self.bets[self.current_player - 1] = b
            return b
        else:
            raise GameError("Not your turn!")

    def verb_river(self, player):
        if self.river_rounds == 0:
            return []
            
        elif self.river_rounds == 1:
            return self.river[:3]
            
        elif self.river_rounds == 2:
            return self.river[:4]
            
        else: 
            return self.river

    def verb_update(self, player):
        if self.current_player == player:
            return [True, self.bets]

        else:
            return [False, self.bets]


GAMES_LIST = {"poker":Poker}
