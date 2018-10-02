import random
from Settings import *
from Dealer import *

game_mode = GameModes.CLASSIC
suitsList = ['heart', 'diamond', 'spade', 'clubs']
valuesList = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 'Jack', 'Queen', 'King']


def play_game(game_deck):
    # initialize the dealer, which also initializes the agent/player
    dealer = Dealer(game_deck, game_mode)
    dealer.deal()


class Card:
    def __init__(self, value, colour):
        self.value = value
        self.colour = colour


def shuffle(s_deck):
    # Shuffles the deck a random number of times (between 1 and 5)
    num_shuffle = random.randint(1, 5)
    for i in range(0, num_shuffle):
        random.shuffle(s_deck)


# initializes the deck
deck = [Card(value, suit) for value in valuesList for suit in suitsList]

# Shuffle the deck
shuffle(deck)
play_game(deck)
