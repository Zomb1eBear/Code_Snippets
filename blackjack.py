'''
Blackjack
'''
import random

# Global Variables
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
suits = ('Hearts', 'Clubs', 'Diamonds', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'
    
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        return self.deck.pop(0)

class Hand:
    def __init__(self): 
        self.cards = [] # cards in hand
        self.value = 0 # total value of hand
        self.aces = 0 # keep track of aces
    def add_card(self,card): 
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace': 
            self.aces += 1
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips: 
    def __init__(self): 
        self.total = 100
        self.bet = 0

    def win_bet(self): 
        self.total += self.bet
    
    def lose_bet (self): 
        self.total -= self.bet

def take_bet(chips): 
    while True: 
        try: 
            chips.bet = int(input('How much would you like to bet? '))
        except ValueError:
            print('Sorry, make it an integer')
        else: 
            if chips.bet > chips.total: 
                print (f"sorry, your bet can't exceed {chips.total}")
            else:
                break

# Get play action - Hit or Stay 
def hit (deck,hand): 
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand): 
    global playing # control game while loop

    while True: 
        act = input ("Hit or Stand? Enter 'h' or 's'")

        if act[0].lower() == 'h': 
            hit(deck,hand)
        elif act[0].lower() == 's':
            print ("Player Stands, dealer turn")
            playing = False
        else: 
            print ('That is not a correct value')
            continue
        break

# print board state

def show_some (player,dealer,chips): 
    print ("\nDealer's Hand:")
    print (" <card hidden> ")
    print ('',dealer.cards[1]) # ' ' just adds empty space
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')
    print (f"Player Chips remaing is {chips.value}")
    
def show_all(player,dealer,chips): 
    print("\nDealer's Hand: ", *dealer.cards, sep='\n ') # * prints every item in a collection
    print("Dealer's Hand = ", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep='\n ') # *player.cards prints out each card in the list with sep = adding a new line separator between each
    print("Player's Hand = ", player.value)
    print (f"Player Chips remaing is {chips.value}")

# Win/Lose bet conditions

def player_busts(player,dealer,chips): 
    print ('Player busts!')
    chips.lose_bet()
def player_wins (player,dealer,chips): 
    print ("Player Wins!")
    chips.win_bet()
def dealer_busts(player,dealer,chips):
    print('Dealer busts!')
    chips.win_bet()
def dealer_wins(player,dealer,chips):
    print('Dealer Wins!')
    chips.lose_bet()
def push (player,dealer): 
    print("Player and Dealer tie, it's a push")

while True: 
    print ('welcome to black jack. Get as close to 21 as  you can without going over!\n Dealer hits until they reach or exceed 17. Aces count as 1 or 11')

    #create deck and shuffle it
    deck = Deck()
    deck.shuffle()
    
    #create hands
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range (2):
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

    #player chips
    player_chips = Chips()

    show_some(player_hand, dealer_hand,player_chips)

    #prompt for bet
    take_bet(player_chips)

    while playing: # called in Hit or Stand function
        hit_or_stand(deck,player_hand)
        show_some (player_hand,dealer_hand,player_chips)

        # Bust check 
        if player_hand.value > 21: 
            player_busts(player_hand,dealer_hand,player_chips)
            break
    
    if player_hand.value <= 21: 
        while dealer_hand.value < 17: 
            hit(deck,dealer_hand)
        
        show_all(player_hand,dealer_hand,player_chips)

        if dealer_hand.value > 21: 
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value: 
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value: 
            player_wins(player_hand,dealer_hand,player_chips)
        else: 
            push(player_hand,dealer_hand)
    
    print ("\n Player's winnings at ", player_chips.total)

    new_game = input ("would you like to play another hand? y or n ") 

    if new_game[0].lower() == 'y': 
        playing = True
        continue
    else: 
        print ("thanks for playing")
        break
        
