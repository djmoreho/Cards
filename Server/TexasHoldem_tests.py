import unittest
from TexasHoldem import score

class PokerScore(unittest.TestCase):
	
	def test_high_tie(self):
		canWin = [True, True] # no one folded
		river = ["ST", "SJ", "SQ", "SK", "SA"]
		hands = [None, None]
		hands[0] = ["H2", "D4"]
		hands[1] = ["D2", "C4"]
		result = score(canWin, river, hands)
		self.assertEqual(result, [0, 1]) # assert both our tied
		
	def test_royal_flush(self):
		canWin = [True, True] # no one folded
		river = ["ST", "SJ", "SQ", "SK", "SA"]
		hands = [None, None]
		hands[0] = ["H2", "D3"]
		hands[1] = ["D2", "C5"] # high value of 5
		result = score(canWin, river, hands)
		self.assertEqual(result, [1]) 
		
		
	def test_high_card(self):
		canWin = [True, True] # no one folded
		river = ["D2", "H5", "H3", "S7", "C8"]
		hands = [None, None]
		hands[0] = ["HA", "CJ"] # Ace should win out
		hands[1] = ["DK", "DJ"]
		result = score(canWin, river, hands)
		self.assertEqual(result, [0]) # assert fold doesn't count
		
	def test_one_fold(self):
		canWin = [True, False, True] # no one folded
		river = ["D2", "H5", "H3", "S7", "C8"]
		hands = [None, None, None]
		hands[0] = ["HA", "CJ"] # Ace should win out
		hands[1] = ["DK", "DJ"]
		hands[2] = ["HJ", "DT"]
		result = score(canWin, river, hands)
		self.assertEqual(result, [0]) # assert fold doesn't count

		
	def test_full_house(self):
		canWin = [True, True] # no one folded
		river = ["C3", "D3", "D7", "DA", "DJ"]
		hands = [None, None]
		hands[0] = ["S3", "SJ"] # full house should beat
		hands[1] = ["D2", "D5"] # flush should lose
		result = score(canWin, river, hands)
		self.assertEqual(result, [0]) 
		
	def test_four_of_a_kind(self):
		canWin = [True, True] # no one folded
		river = ["HK", "DK", "SA", "S5", "D2"]
		hands = [None, None]
		hands[0] = ["CK", "SK"] # four of a kind
		hands[1] = ["DA", "CA"] # full house
		result = score(canWin, river, hands)
		self.assertEqual(result, [0]) 
		

	def test_fold(self):
		canWin = [True, False]
		river = ["ST", "SJ", "SQ", "SK", "SA"]
		hands = [None, None]
		hands[0] = ["H2", "D4"]
		hands[1] = ["D2", "C4"]
		result = score(canWin, river, hands)
		self.assertEqual(result, [0]) # assert fold doesn't count
	
	
	def test_fold(self):
		canWin = [True, False] # no one folded
		river = ["ST", "SJ", "SQ", "SK", "SA"]
		hands = [None, None]
		hands[0] = ["H2", "D4"]
		hands[1] = ["D2", "C4"]
		result = score(canWin, river, hands)
		self.assertEqual(result, [0]) # assert fold doesn't count
	
	def test_all_fold(self):
		canWin = [False, False] # no one folded
		river = ["ST", "SJ", "SQ", "SK", "SA"]
		hands = [None, None]
		hands[0] = ["H2", "D4"]
		hands[1] = ["D2", "C4"]
		result = score(canWin, river, hands)
		self.assertEqual(result, [0, 1]) # assert fold doesn't count
	
		
if __name__ == '__main__':
    unittest.main()