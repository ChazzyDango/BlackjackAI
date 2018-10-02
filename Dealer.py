from Settings import *
import numpy
from Agent import *


class Dealer:

    # when the game is first initialized the dealer is handed the shuffled deck
    def __init__(self, deck, game_mode):
        # makes an instance of the deck for themself, this
        self.game_deck = list()
        for cards in deck:
            self.game_deck.append(cards)
        self.hand = list()
        self.game_mode = game_mode

        # initializes the Agent(Other Player)
        self.opponent = Agent(self.game_deck)

        # if the game mode is classic (dealer hits up to 17 always
        # TODO wait for the agent's actions
        # TODO Finish hitting/standing with its own hand
        # TODO Reward Agent with win/loss (+1/-1)

    # deals cards to the agent and dealer and remove them from deck
    def deal(self):
        # dealer draws a card
        self.hand.append(self.game_deck.pop())
        # dealer deals a card to the agent
        self.opponent.draw_card(self.game_deck.pop())
        self.hand.append(self.game_deck.pop())
        # reveals the one card from the dealers hand to the agent
        self.opponent.see_card(self.hand[1])
        self.opponent.draw_card(self.game_deck.pop())

    # a method for understanding the values on a card (eg: King = 10)
    def convert_handval(self, card):
        #if the card is an ace we must have a special condition for it
        if card.value == 'Ace':
            # TODO figure out how to handle aces
            print("uh oh")
        # if the card is a face card
        elif card.value == 'King' or card.value == 'Jack' or card.value == 'Queen':
            return 10
        # otherwise the card is from 2-9 and doesn't require translation
        else:
            return card.value

    # discards the hand at the end of the round
    def discard_hand(self):
        self.hand = []

    def dealer_turn(self):
        hand_sum = 0
        for i in range(0, len(self.hand)):
            hand_sum += self.convert_handval(self.hand[i])

        # in classic blackjack a dealer hits on 17 or lower (even soft 17s)
        if self.game_mode == GameModes.CLASSIC:
            # if the dealer should hit
            while hand_sum <= 17:
                # dealer draws a card
                self.hand.append(self.game_deck.pop())
                # resets the hand sum value and recalculates it
                hand_sum = 0
                for i in range(0, len(self.hand)):
                    hand_sum += self.convert_handval(self.hand[i])
            # now the dealer is done hitting and has their final value
            if hand_sum > 21:
                print("Dealer BUST")
                # TODO implement logic for when the dealer busts

