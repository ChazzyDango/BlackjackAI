from Settings import *
import numpy
import time
from Agent import *


class NeuralDealer:

    # when the game is first initialized the dealer is handed the shuffled deck
    def __init__(self, deck):
        # makes an instance of the deck for themself, this
        self.game_deck = list()
        for cards in deck:
            self.game_deck.append(cards)
        self.hand = list()

        # initializes the Agent(Other Player)
        self.opponent_hand = list

        # if the game mode is classic (dealer hits up to 17 always

    # deals cards to the agent and dealer and remove them from deck
    def deal(self):
        # dealer draws a card
        self.hand.append(self.game_deck.pop())
        # dealer deals a card to the agent
        self.opponent_hand.append(self.game_deck.pop())
        self.hand.append(self.game_deck.pop())
        # dealer deals a card to the agent
        self.opponent_hand.append(self.game_deck.pop())


    # a method for understanding the values on a card (eg: King = 10)
    def convert_handval(self, card):
        # if the card is an ace we must have a special condition for it
        # An ace is considered a one when returned, the calculation determines if it can be an 11
        if card.value == 'Ace':
            return 1
        # if the card is a face card
        elif card.value == 'King' or card.value == 'Jack' or card.value == 'Queen':
            return 10
        # otherwise the card is from 2-9 and doesn't require translation
        else:
            return card.value


