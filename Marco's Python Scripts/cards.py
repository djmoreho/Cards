# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import random as random
__author__ = "marco"
__date__ = "$17-Oct-2015 1:58:30 PM$"

if __name__ == "__main__":
    print "Hello World"
    


class card(Object):
    #number coralating to suit ranged 0-3
    suit = 0
    #number coralating to card number ranged 0-12
    number = 0
    #Order of suits
    suits["Spade","Heart","Club","Diamond"]
    #Order of card numbers
    numbers["two","three","four","five","six","seven","eight","nine","ten","jack"
        ,"queen","king","ace"]
        
    #initialize the card
    def __init__(suit, number, self):
        self.suit = suit
        self.number = number
    
    #ToString of format:"[number] of [suit]" without a newline.
    def __str__(self):
        return numbers[number] + " of " + suits[suit] + 's'
    
    
class stack(Object):
    number_of_cards = 0
    #Array of cards
    stack=[]
    points = 0
    facedown = True
    
    def __init__(initial_Points,is_facedown,self):
        self.points = initial_points
        self.facedown = is_facedown
    
    #Add an array of cards to the top of the stack
    def add_Cards(cards_Added,self):
        for val in cards_Added:
            self.stack.append(val)
        self.number_of_cards += len(cards_Added)
    
    #Add a single card to the top of the stack        
    def add_A_Card(card,self):
        self.stack.append(card)
        self.number_of_cards += 1
        
    def shuffle(self):
        random.shuffle(self.stack)
            
    def pop_card(self):
        self.number_of_cards -= 1
        return self.stack.pop(len(self.stack) - 1)
    
    #Removes a specific card from the stack and returns it
    def remove_card(index,self):
        temp = self.stack[index]
        self.stack.del(index)
        self.number_of_cards -= 1
        return temp
    
    
    def dealTo(num_cards,to_stack,self):
        count = 0     
        while count < num_cards:
            count += 1
            to_stack.stack.append(self.pop_card)
            
        
    def __str__(self):
        out_string = ""
        for val in self.stack:
            out_string += val + ", "
        
        return out_string
        
class player(stack):   
    name = "0"
    
    def __init__(initial_Points, name, is_facedown, self):
        self.points = initial_Points
        self.facedown = is_facedown
        self.name = name
    
    def __str__(self):
        out_string = name + " has " + self.points + " points and a hand with: "
        for val in self.stack:
            out_string += val + ", "
        
        return out_string
    
    