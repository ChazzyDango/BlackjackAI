import random
from Settings import *
from Dealer import *

game_mode = GameModes.CLASSIC
suitsList = ['heart', 'diamond', 'spade', 'clubs']
valuesList = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']


def play_game(game_deck):
    # initialize the dealer, which also initializes the agent/player
    dealer = Dealer(game_deck, game_mode)
    dealer.deal()
    dealer.play()
    # TODO Reward Agent with win/loss (+1/-1)


class Card:
    def __init__(self, value, colour, decknum):
        self.value = value
        self.colour = colour
        self.decknum = decknum


def shuffle(s_deck):
    # Shuffles the deck a random number of times (between 1 and 5)
    num_shuffle = random.randint(1, 5)
    for i in range(0, num_shuffle):
        random.shuffle(s_deck)


deck = []
# initializes the deck(s) depending on the number of decks
for i in range(1, NUM_DECKS+1):
    deck += [Card(value, suit, i) for value in valuesList for suit in suitsList]

# Shuffle the deck
shuffle(deck)
play_game(deck)
