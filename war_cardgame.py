import random
import pdb # This is python's in built debug library

#Global Var
values = {'Two':2,'Three':3,'Four':4,'Five':5, 'Six':6, 'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':11,'Queen':12,'King':13, 'Ace':14}
suits = ('Hearts','Clubs','Diamonds','Spades')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')

# dont forget that self ref
class Card  (): 
    '''
    Card base class
    '''
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        # rank takes in the global dictionary, 
        # values[rank] gets the value of the key
        self.value = values[rank]

    #string method
    def __str__(self): 
        return self.rank + ' of ' + self.suit
#this is correct

class Deck():
    '''
    Deck class
    '''
    def __init__(self):
        ''' all_cards wil be the same each time it is run
        as such, no user input is needed, so it's not called
        in the parameters'''
    
        self.all_cards = []
        created_card = ' '
        for suit in suits: 
            for rank in ranks: 
                #create the Card obj
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)
    
    def shuffle(self): 
        '''If you use from random import shuffle, you can call 
        shuffle directly onto a function. If you just call the random
        library, however,  you will have to call random, then call
        the function'''

        random.shuffle(self.all_cards)
        ''' no return is necessary on shuffle, it performs function in
        place and can't be stored in a local variable'''
    
    def deal_one (self):
        # the .pop() argument both returns AND removes, not just removes 
        return self.all_cards.pop(0)
# this is correct

class Player(): 
    '''
    Player class
    '''
    def __init__(self,name):
        self.name = name
        self.all_cards = []

    def play_card(self):
        return self.all_cards.pop(0)
    
    def add_card(self,newcards):
        '''can't use .append() here.
        .append() on a list would add the item as a list to the 
        original list, not append each item. .extend adds each item instead
        '''
        if type(newcards)== type([]):
            self.all_cards.extend(newcards)

        # if it's just one card, you can still use append()
        else: 
            self.all_cards.append(newcards)

    def __str__(self):
        return f'Player {self.name} has {len(self.all_cards)} cards'
# This ic correct

def deal (): 
    for x in range (26):
        player1.add_card(newdeck.deal_one())
        player2.add_card(newdeck.deal_one())
#This should be correct

def win_lose(): 
    if len(player1.all_cards) == 0: 
        print (f'{player1.name} loses, {player2.name} wins!')
        return False
    elif len(player2.all_cards) == 0: 
        print (f'{player2.name} loses, {player1.name} wins!')
        return False
    else: 
        return True
        
gameon = True
round_num = 0
player1 = Player('Red')
player2 = Player('Blue')   
newdeck = Deck()
newdeck.shuffle()
deal()

while gameon: 
    round_num = round_num + 1
    print (round_num)
    #start the game
    
    gameon = win_lose()
    
    if gameon == False: 
        break
    
    p1=[]
    p2=[]
    p1.append(player1.play_card())
    p2.append(player2.play_card())
    
    at_war = True
    while at_war:
        print(p1[-1])
        print (p2[-1])

        if p1[-1].value > p2[-1].value: 
            player1.add_card(p1)
            player1.add_card(p2)
            at_war = False
        elif p2[-1].value > p1[-1].value: 
            player2.add_card(p2)
            player2.add_card(p1)
            at_war = False
        else: 
            print ('WAR!')
            if len(player1.all_cards)<3: 
                print (' player cannot play war')
                print (f'{player1} loses, {player2} wins!')
                game_on = False
                break
            elif len(player2.all_cards)<3: 
                print (' player cannot play war')
                print (f'{player2} loses, {player1} wins!')
                game_on = False
                break
            else: 
                for num in range(3):
                    p1.append(player1.play_card())
                    p2.append(player2.play_card()) 

    gameon = win_lose()
    if gameon == False: 
        break

