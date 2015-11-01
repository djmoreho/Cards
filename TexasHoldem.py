#Gamestate for Texas Hold'em
#@author Ian Glazko

class GameState:
	players #Array of players
	deck = Stack(0)
	river = [Stack(0) for x in range(5)] #river is 5 face-up stacks

	def __init__(self, numPlayers):
		self.players = [Player("") for x in range(numPlayers)]

	#Plays one hand of Texas Holdem
	def playHand(self):
		bids = [0 for i in range(len(players))]
		handPlayers = [True for x in range(len(players))] #False indicates player folded

		for i in range(2):
			for player in players:
				self.draw(player, deck)

		self.takeBids(bids)

		#Fill first 3 cards of river
		for i in range(3):
			self.draw(river[i], deck)

		self.takeBids(bids, handPlayers)
		self.draw(river[4], deck)
		self.takeBids(bids, handPlayers)
		self.draw(river[5], deck)
		self.takeBids(bids, handPlayers)

		#Score hands, distribute bets
		self.score(bids, handPlayers)

	#checks if the end condition has been met
	def isEnd(self):
		return len(players) == 1

	#draws a card from src to dest
	def draw(self, dest, src):
		deck.dealTwo(1, dest)

	#Takes bids from each player and stores in bidArr
	#Players that fold are removed from further bids in same round
	#  after bidding
	#TODO check player money and actually deduct
	def takeBids(self, bidArr, foldArr):
		keepBidding = True
		lastRaise = -1
		while keepBidding:
			for i in range(len(players)]):
				if i == lastRaise:
					keepBidding = False; #If everyone calls/checks/folds stop bidding
					break;

				if foldArr[i]:
					bid = 0 #TODO ask players[i] for bid
					if bid < 0:
						foldArr[i] = False #Player folds
					elif bid = 0:
						if players[i].score < bidArr[lastRaise]:
							bidArr[i] = players[i].score() #all in to call
						else:
							bidArr = bidArr[lastRaise] #call
					else:
						bidArr[i] = bidArr[lastRaise]
						bidArr[i] += bid #Player raises

						if bidArr[i] > players[i].score:
							bidArr[i] = players[i].score #max out all in

						lastRaise = i #they are now the bid to match
			#END FOR
		#END WHILE
	

	#Scores a hand
	#Deducts bids from losers' scores, splits pot among winners	
	def score(self, bidArr, canWin):
		scoreArr = [0 for p in Players]; #Stores hand "scores" to compare

		#May leave this loop out if players score own
		for p in range(len(Players)):
			fullHand = [river[0].top, river[1].top, river[2].top, river[3].top, river[4].top, Players[p].hand.top, Players[p].hand.bot] #TODO Check syntax, should be array of 7 cards
			
			#if the player folded, their score is 0
			if !canWin[p]:
				break;

			#Checks score for each possible hand, keeps greatest
			for exOne in range(0,6):
				for exTwo in range(exOne, 7):
					checkFive = [fullHand[i] for i in range(7) if i not in [exOne, exTwo]]

					#sort high to low
					for i in range(0,4):
						for j in range(i,5):
							if checkFive[j].val > checkFive[i].val:
								tmp = checkFive[i]
								checkFive[i] = checkFive[j]
								checkFive[j] = tmp

					straightProgression = 0
					straightNum = 99

					flushProgS = 0		#flush count with Spades
					flushProgH = 0		#flush count with Hearts
					flushProgC = 0		#flush count with clubs
					flushProgD = 0		#flush count with diamonds

					hasFour = 0		#hasX vars are not cumulative 
					hasThree = 0		#four of a kind = hasFour but not hasThree
					hasTwo = 0		#0 is false, other is card val of set
					hasTP = 0		#Two Pair
					cardCount = [0 for i in range(0,14)] #whether seen cards through ace(14)

					for card in checkFive:
						if card.val == straightNum - straightProgression:
							straightProgression ++
						elif card.val < straightNum - straightProgression:
							straightNum = card.val
							straightProgression = 1

						if card.suit == 0:
							flushProgS++
						elif card.suit == 1:
							flushProgH++
						elif card.suit == 2:
							flushProgC++
						else
							flushProgD++

						cardCount[card.val]++

					#Check multiples
					for c in range(0,len(cardCount)):
						if c == 4:
							hasFour = c
							break;
						elif c == 3:
							hasThree = c
						elif c == 2:
							if hasTwo:
								hasTP = c
							else:
								hasTwo = c

					hasFlush = flushProgS == 5 or flushProgH == 5 or flushProgC == 5 or flushProgD == 5
					score = 0

					if straightProgression == 5 and hasFlush:
						if straightNum == 14:
							scoreArr[p] = 90000000000 #Val for Royal Flush, always top
							break #Don't test other hands
						else
							score = 80000000000 #base for Straight Flush
							score += checkFive[0] * 100000000 #2nd two digits become val of top card
					elif hasFour != 0:
						score = 70000000000 #base for 4oaK
						score += hasFour * 100000000
						#no need to test high card for 4oaK
					elif hasThree != 0 and hasTwo != 0:
						score = 60000000000 #base for Full House
						score += hasThree * 100000000
						score += hasTwo * 1000000
					elif hasFlush:
						score = 50000000000 #base for flush
						score += checkFive[0] * 100000000
						score += checkFive[1] * 1000000
						score += checkFive[2] * 10000
						score += checkFive[3] * 100
						score += checkFive[4]
					elif straightProgression == 5:
						score = 40000000000 #base for Straight
						score += straightNum * 100000000
					elif hasThree != 0:
						score = 30000000000 #base for 3oaK
						score += hasThree * 100000000
						if checkFive[0] == hasThree:
							score += checkFive[3] * 1000000
							score += checkFive[4] * 10000
						else:
							score += checkFive[0] * 1000000
							if checkFive[4] == hasThree:
								score += checkFive[1] * 10000
							else:
								score += checkFive[4] * 10000
					elif hasTP != 0:
						score = 20000000000 #base for two pair
						if hasTwo > hasTP:
							score += hasTwo * 100000000
							score += hasTP * 1000000
						else:
							score += hasTwo * 1000000
							score += hasTP * 100000000
						
						if checkFive[0] != hasTwo and checkFive[0] != hasTP:
							score += checkFive[0]
						elif checkFive[4] != hasTwo and checkFive[4] != hasTP:
							score += checkFive[4]
						else:
							score += checkFive[2]
					elif hasTwo != 0:
						score = 10000000000 #base for one pair
						score += hasTwo * 100000000
						
						if checkFive[0] == hasTwo:
							score += checkFive[2] * 1000000
							score += checkFive[3] * 10000
							score += checkFive[4] * 100
						elif checkFive[0] == hasTwo:
							score += checkFive[0] * 1000000
							score += checkFive[3] * 10000
							score += checkFive[4] * 100
						elif checkFive[0] == hasTwo:
							score += checkFive[0] * 1000000
							score += checkFive[1] * 10000
							score += checkFive[4] * 100
						else:
							score += checkFive[0] * 1000000
							score += checkFive[1] * 10000
							score += checkFive[2] * 100
					else:
						#High card
						score += checkFive[0] * 100000000
						score += checkFive[1] * 1000000
						score += checkFive[2] * 10000
						score += checkFive[3] * 100
						score += checkFive[4]
					#End cases if
					if score > scoreArr[p]:
						scoreArr[p] = score
				#End exTwo loop
			#End exOne loop
		#End players loop
		didWin = [False for player in [players]
		winCount = 0 #How many won, must split pot
		topScore = max(scoreArr)

		for p in range(0,len(scoreArr)):
			if scoreArr[p] == topScore:
				#See if they won
				didWin[p] = True
				winCount++

		for p in range(0,len(players)):
			if didWin[p]:
				#win the pot, shared with other winners
				players[p].score += sum(bidArr)/winCount
			else:
				#lose their bet
				players[p].score -= bidArr[p]
	#End score method
#End class GameStates
