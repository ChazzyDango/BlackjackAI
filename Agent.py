from Settings import *
import random


class Agent:

    def __init__(self, deck):
        self.known_deck = list()
        for cards in deck:
            self.known_deck.append(cards)
        self.hand = list()

        # This array is the cards known to be discarded, it exists for debugging purposes and data analysis
        self.known_discard = []
        # in case i want to make the agent forget cards ocassionally (From Settings.py)
        self.forget = forgetfullness

    def agent_turn(self):
        # TODO calculate odds of winning based on hits, stands, doubles, etc.
        # TODO Put all calculation logic here
        print("Hewwo 2")
        return 1

    def draw_card(self, card):
        self.hand.append(card)

        # TODO implement this forgetting code later, maybe after a round as the cards are discarded
        # rolls a number from 1 to 100, if its greater than the forget threshold don't remember it
        # if random.randint(1, 100) > self.forget:
        self.known_discard.append(card)
        self.known_deck.remove(card)

    def see_card(self, card):
        self.known_deck.remove(card)
        self.known_discard.append(card)

