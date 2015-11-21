### Games_tests.py

import unittest
from Games import Poker, War, GameError
import sys
import os

class PokerTests(unittest.TestCase):
    
    def test_normal_game(self):
        p = Poker()
        pn, hand, amount = p.add_player()
        self.assertEqual(pn, 1)
        self.assertEqual(len(hand), 2)
        pn, hand, amount = p.add_player()
        self.assertEqual(pn, 2)
        self.assertEqual(len(hand), 2)
        pn, hand, amount = p.add_player()
        self.assertEqual(pn, 3)
        self.assertEqual(len(hand), 2)
        
        ## now start the game
        # round 1
        self.assertEqual(len(p.verb("river", 1)), 0) 
        self.assertEqual(p.verb("bet", 1, amount=500), 4500)
        self.assertEqual(p.verb("end_turn", 1), None)
        
        self.assertEqual(p.verb("bet", 2, amount=1000), 4000)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=700), 4300)
        self.assertEqual(p.verb("end_turn", 3), None)
        
        # round 2
        self.assertEqual(len(p.verb("river", 1)), 3) 
        
        # everyone bets
        self.assertEqual(p.verb("bet", 1, amount=500), 4000)
        self.assertEqual(p.verb("end_turn", 1), None)
        
        self.assertEqual(p.verb("bet", 2, amount=500), 3500)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=500), 3800)
        self.assertEqual(p.verb("end_turn", 3), None)

        # round 3
        self.assertEqual(len(p.verb("river", 1)), 4) 
        
        # everyone bets
        self.assertEqual(p.verb("bet", 1, amount=500), 3500)
        self.assertEqual(p.verb("end_turn", 1), None)
        
        self.assertEqual(p.verb("bet", 2, amount=600), 2900)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=400), 3400)
        self.assertEqual(p.verb("end_turn", 3), None)
        
        # round 4
        self.assertEqual(len(p.verb("river", 1)), 5) 
        
        # everyone bets
        self.assertEqual(p.verb("bet", 1, amount=600), 2900)
        self.assertEqual(p.verb("end_turn", 1), None)
        
        self.assertEqual(p.verb("bet", 2, amount=1000), 1900)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=400), 3000)
        self.assertEqual(p.verb("end_turn", 3), None)
        
        # now check score
        from TexasHoldem import score
        winner = score([True, True, True], 
                      p.verb("river", 1), 
                      p.hands)
                      
        self.assertEqual(p.verb("score", 1), winner)

    def test_folds(self):
        p = Poker()
        pn, hand, amount = p.add_player()
        self.assertEqual(pn, 1)
        self.assertEqual(len(hand), 2)
        pn, hand, amount = p.add_player()
        self.assertEqual(pn, 2)
        self.assertEqual(len(hand), 2)
        pn, hand, amount = p.add_player()
        self.assertEqual(pn, 3)
        self.assertEqual(len(hand), 2)
        
        ## now start the game
        # round 1
        self.assertEqual(len(p.verb("river", 1)), 0) 
        self.assertEqual(p.verb("bet", 1, amount=500), 4500)
        self.assertEqual(p.verb("end_turn", 1), None)
        
        self.assertEqual(p.verb("bet", 2, amount=1000), 4000)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=700), 4300)
        self.assertEqual(p.verb("end_turn", 3), None)
        
        # round 2
        self.assertEqual(len(p.verb("river", 1)), 3) 
        
        # everyone bets
        self.assertEqual(p.verb("bet", 1, amount=500), 4000)
        self.assertEqual(p.verb("end_turn", 1), None)
        
        self.assertEqual(p.verb("bet", 2, amount=500), 3500)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=500), 3800)
        self.assertEqual(p.verb("end_turn", 3), None)

        # round 3
        self.assertEqual(len(p.verb("river", 1)), 4) 
        
        # everyone bets
        self.assertEqual(p.verb("bet", 1, amount=500), 3500)
        self.assertEqual(p.verb("end_turn", 1), None)
        
        self.assertEqual(p.verb("fold", 2), None)

        self.assertEqual(p.verb("fold", 3), None)

        # round 4
        self.assertEqual(len(p.verb("river", 1)), 5) 

        # everyone bets
        
        self.assertEqual(p.verb("bet", 1, amount=600), 2900)
        self.assertEqual(p.verb("end_turn", 1), None)
        
        # after you fold you can't bet
        self.assertRaises(GameError, p.verb, "bet", 2, amount=400)
        self.assertRaises(GameError, p.verb, "end_turn", 2)
                
        self.assertRaises(GameError, p.verb, "bet", 3, amount=400)
        self.assertRaises(GameError, p.verb, "end_turn", 3)

        # now check score
        from TexasHoldem import score
        winner = score([True, False, False], 
                      p.verb("river", 1), 
                      p.hands)
                      
        self.assertEqual(p.verb("score", 1), winner)
        
    def test_errors(self):
        p = Poker()
        pn, hand, amount = p.add_player()
        self.assertEqual(pn, 1)
        self.assertEqual(len(hand), 2)
        pn, hand, amount = p.add_player()
        self.assertEqual(pn, 2)
        self.assertEqual(len(hand), 2)
        pn, hand, amount = p.add_player()
        self.assertEqual(pn, 3)
        self.assertEqual(len(hand), 2)
        
        ## now start the game
        # round 1
        ## test out of order

        ## test that you must bet for 1
        self.assertRaises(GameError, p.verb, "end_turn", 1)
        
        # 2 goes before 1 did
        self.assertRaises(GameError, p.verb, "bet", 2, amount=1000)
        self.assertRaises(GameError, p.verb, "end_turn", 2)

        ## test that you must bet for 1
        self.assertRaises(GameError, p.verb, "end_turn", 1)
        
        ## test too big of a bet for 1
        self.assertRaises(GameError, p.verb, "bet", 1, amount=10000)

        ## test that you must bet for 1
        self.assertRaises(GameError, p.verb, "end_turn", 1)
        
        ## or fold
        self.assertEquals(p.verb("fold", 1), None)
 
        ## normal code make sure it works
        
        self.assertEqual(p.verb("bet", 2, amount=1000), 4000)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=700), 4300)
        self.assertEqual(p.verb("end_turn", 3), None)
        
        # round 2
        self.assertEqual(len(p.verb("river", 1)), 3) 
        
        # everyone bets
        self.assertEqual(p.verb("bet", 2, amount=500), 3500)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=500), 3800)
        self.assertEqual(p.verb("end_turn", 3), None)

        # round 3
        self.assertEqual(len(p.verb("river", 1)), 4) 
        
        # everyone bets
        self.assertEqual(p.verb("bet", 2, amount=600), 2900)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=400), 3400)
        self.assertEqual(p.verb("end_turn", 3), None)
        
        # round 4
        self.assertEqual(len(p.verb("river", 1)), 5) 
        
        # everyone bets
        self.assertEqual(p.verb("bet", 2, amount=1000), 1900)
        self.assertEqual(p.verb("end_turn", 2), None)
        
        self.assertEqual(p.verb("bet", 3, amount=400), 3000)
        self.assertEqual(p.verb("end_turn", 3), None)
        
        # now check score
        # make sure though that 1 can get the river and score
        # after folding (so they can move to the next game as well)
        from TexasHoldem import score
        winner = score([False, True, True], 
                      p.verb("river", 1), 
                      p.hands)
                      
        self.assertEqual(p.verb("score", 1), winner)
        

class Wars(unittest.TestCase):
    
    def test_normal_War(self):
    	w = War()
    	pn, hand, dis = w.add_player()
        self.assertEqual(pn, 1)
        self.assertEqual(len(hand), 26)
        pn, hand, dis = w.add_player()
        self.assertEqual(pn, 2)
        self.assertEqual(len(hand), 26)
        w.hands[0] = ["HA", "D3", "C3"]
        w.hands[1] = ["H2", "S2", "S4"]
        w.verb("update", 1)
        w.verb("update", 2)
        self.assertEqual(len(w.hands[0]), 2)
        self.assertEqual(len(w.hands[1]), 2)
        w.verb("update", 1)
        w.verb("update", 2)
        self.assertEqual(len(w.hands[0]), 1)
        self.assertEqual(len(w.hands[1]), 1)
        w.verb("update", 1)
        w.verb("update", 2)
        self.assertEqual(len(w.hands[0]), 2)
        self.assertEqual(len(w.hands[1]), 2)
    
    def test_endgame(self):
    	w = War()
    	w.add_player()
    	w.add_player()
    	w.hands[0] = ["HA", "D3", "C4"]
        w.hands[1] = ["H2", "S2", "S3"]
        w.verb("update", 1)
        w.verb("update", 2)
        self.assertEqual(len(w.hands[0]), 2)
        self.assertEqual(len(w.hands[1]), 2)
        w.verb("update", 1)
        w.verb("update", 2)
        self.assertEqual(len(w.hands[0]), 1)
        self.assertEqual(len(w.hands[1]), 1)
        w.verb("update", 1)
        self.assertEqual(w.verb("update", 2), (-1, 0, None))
        self.assertEqual(len(w.hands[0]), 4)
        self.assertEqual(len(w.hands[1]), 0)
    
    def test_War(self):
    	w = War()
    	w.add_player()
    	w.add_player()
    	w.hands[0] = ["C4", "HA", "D2", "D3", "C3"]
        w.hands[1] = ["C2", "H2", "D3", "S2", "S3"]
        w.verb("update", 1)
        w.verb("update", 2)
        self.assertEqual(len(w.hands[0]), 1)
        self.assertEqual(len(w.hands[1]), 1)
        w.verb("update", 1)
        self.assertEqual(w.verb("update", 2), (-1, 0, None))
        self.assertEqual(len(w.hands[0]), 8)
        self.assertEqual(len(w.hands[1]), 0)
    
    def test_error(self):
    	w = War()
    	w.add_player()
    	w.add_player()
    	w.hands[0] = ["HA", "D3", "C4"]
        w.hands[1] = ["H2", "S2", "S3"]
        
        #make sure 2 can't go out of turn
        self.assertRaises(GameError, w.verb, "update", 2)
        
if __name__ == '__main__':
    unittest.main()
