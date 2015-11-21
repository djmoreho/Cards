import hashlib
import random #will use better randomness for final
import itertools

def generateDeck():
	suits = ["C", "H", "S", "D"]
	ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
	deck = []
	for suit in suits:
		for rank in ranks:
			deck.append("%s%s" % (suit, rank))
	random.shuffle(deck)
	return deck
	
def getHands(numPlayers, numCards, deck):
	hands = [[] for i in range(numPlayers)]
	for i in range(numCards):
		for j in range(numPlayers):
			card = random.choice(deck)
			deck.remove(card)
			hands[j].append(card)
	return hands
	
def formatCards(hands, river):
	formattedCards = ["" for i in range(len(hands))]
	r = "_"
	for card in river:
		r += card
	for i in range(len(hands)):
		for card in hands[i]:
			formattedCards[i] += card
	for i in range(len(hands)):
		formattedCards[i] += r
	return formattedCards
	
def round(numPlayers, bank, river, hands):
	bidArr = [0 for i in range(numPlayers)]
	foldArr = [True for i in range(numPlayers)]
	numFolds = 0
	for i in range(3):
		#print "Bidding %d" % i
		takeBids(bidArr, foldArr, numPlayers, bank)
		numFolds = 0
		for notFold in foldArr:
			if not notFold:
				numFolds += 1
		if numFolds == numPlayers - 1:
			break
	winners = []
	topScore = 0
	if numFolds != numPlayers - 1:
		winners, topScore = score(bidArr, foldArr, numPlayers, river, hands)
	else:
		for i in range(numPlayers):
			if foldArr[i]:
				winners.append(i)
				break
				
	for p in range(numPlayers):
		if p in winners:
			#win the pot, shared with other winners
			bank[p] += sum(bidArr)/len(winners)
		else:
			#lose their bet
			bank[p] -= bidArr[p]
	#print winners
	#print bank
	

def takeBids(bidArr, foldArr, numPlayers, bank):
	lastRaise = -1
	while 1:
		for i in range(numPlayers):
			if i == lastRaise:
				return

			if foldArr[i]:
				bid = int(raw_input())
				if bid < 0:
					#print "Player %d folds" % i
					foldArr[i] = False #Player folds
				elif bid == 0:
					if bank[i] < bidArr[lastRaise]:
						#print "Player %d goes all in" % i
						bidArr[i] += bank[i] #all in to call
						bank[i] = 0
					else:
						#print "Player %d calls" % i
						bank[i] -= bidArr[lastRaise] - bidArr[i]
						bidArr[i] = bidArr[lastRaise] #call
				else:
					#print "Player %d bids %d" % (i, bid)
					bidArr[i] = bidArr[lastRaise]
					bidArr[i] += bid #Player raises
					if bidArr[i] > bank[i]:
						bidArr[i] += bank[i] #max out all in
						bank[i] = 0
					else:
						bank[i] -= bid
					lastRaise = i #they are now the bid to match
					
def getValue(card):
	rank = card[1:]
	if rank in ("2", "3", "4", "5", "6", "7", "8", "9"):
		return int(rank) - 2
	if rank == "T":
		return 8
	if rank == "J":
		return 9
	if rank == "Q":
		return 10
	if rank == "K":
		return 11
	if rank == "A":
		return 12
	print "something is terribly wrong %s" % rank
	return -1
	

def score(canWin, river, hands):
	'''
	@canWin: Array of booleans, false is you folded
	@numPlayers: number of players
	'''
	numPlayers = len(hands) # find the number of players in this game
	scoreArr = [0 for p in xrange(numPlayers)] #Stores hand "scores" to compare

	#May leave this loop out if players score own
	playerBestCombinations = {}
	for p in range(numPlayers):
		playerBestCombinations[p] = {}
	for p in range(numPlayers):
		fullHand = [river[0], river[1], river[2], river[3], river[4], hands[p][0], hands[p][1]] #TODO Check syntax, should be array of 7 cards
		
		#if the player folded, their score is 0
		if not canWin[p]: # if they folded we say they had 0, basically ignore folded cards
			break

		#Checks score for each possible hand, keeps greatest
		for checkFive in itertools.permutations(fullHand, 5):
			#checkFive = [river[0], river[1], river[2], river[3], river[4]]
			# check five
			#sort high to low
			checkFive = list(checkFive)
			for i in range(0,4):
				for j in range(i,5):
					if getValue(checkFive[j]) > getValue(checkFive[i]):
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
			# find how often you see 2 ... A
			cardCount = [0 for i in range(0,13)] #whether seen cards through ace(14)
			for card in checkFive:
				if getValue(card) == straightNum - straightProgression:
					straightProgression += 1
				elif getValue(card) < straightNum - straightProgression:
					straightNum = getValue(card)
					straightProgression = 1

				if card[:1] == "S":
					flushProgS += 1
				elif card[:1] == "H":
					flushProgH += 1
				elif card[:1] == "D":
					flushProgC += 1
				else:
					flushProgD += 1

				cardCount[getValue(card)] += 1

			#Check multiples
			for c in cardCount:
				if c == 4:
					hasFour = c
				elif c == 3:
					hasThree = c
				elif c == 2:
					if hasTwo:
						hasTP = c
					else:
						hasTwo = c

			hasFlush = flushProgS == 5 or flushProgH == 5 or flushProgC == 5 or flushProgD == 5
			score = 0

			t = []
			for i in checkFive:
				t.append(getValue(i))
				
			checkFiveOld = checkFive
			checkFive = t
			# score -> hand

			if straightProgression == 5 and hasFlush:
				if straightNum == 12:
					score = 90000000000 #Val for Royal Flush, always top
					score += 0 # no differentiating factor, all royal flushes are equal!
							   # where you can have that with other combos
				else:
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

			playerBestCombinations[p][score] = checkFiveOld
						
		# end loop
	#End players loop

	scores = []
	for i in playerBestCombinations.keys():
		scores.append([])
	
	for n,i in enumerate(playerBestCombinations.keys()):# iterate through players
		for j in playerBestCombinations[i].keys():# get the scores?
			scores[n].append(j)
	
	allScores = []
	for i in playerBestCombinations.keys():
		l = []
		allScores.append(l)
		for j in playerBestCombinations[i].keys():
			l.append(j)
		l.sort() # low to high
		l.reverse() # high to low

	m = max(allScores)
	winning_players = []
	for n,i in enumerate(allScores):
		if i == m: # if they have the max score
			winning_players.append(n)
			
	return winning_players

if __name__ == "__main__":
	numPlayers = 4
	deck = generateDeck()
	hands = getHands(numPlayers, 2, deck)
	river = [deck[-1], deck[-2], deck[-3], deck[-4], deck[-5]]
	formattedCards = formatCards(hands, river)
	bank = [100 for i in range(numPlayers)]
	round(numPlayers, bank, river, hands)