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

    # discards the hand at the end of the round
    def discard_hand(self):
        self.hand = []

    def dealer_turn(self):
        # the sum of all cards in the hand (simplifies code)
        hand_sum = 0
        # create an array of the values of cards in hand (simplifies code)
        card_vals = []
        for i in range(0, len(self.hand)):
            card_vals.append(self.convert_handval(self.hand[i]))
        hand_sum = sum(card_vals)
        # if one of the cards is an Ace, check if it should be an 11 or 1
        if 1 in card_vals:
            if hand_sum <= 11:
                hand_sum += 10
        # in classic blackjack a dealer hits on 17 or lower (even soft 17s)
        if self.game_mode == GameModes.CLASSIC:
            # if the dealer should hit
            while hand_sum <= 17:
                # dealer draws a card
                self.hand.append(self.game_deck.pop())
                # appends the newly drawn card's value to the cardval array
                card_vals.append(self.convert_handval(self.hand[-1]))
                # recalculates the hand sum
                hand_sum = sum(card_vals)
                # if one of the cards is an Ace, check if it should be an 11 or 1
                if 1 in card_vals:
                    if hand_sum <= 11:
                        hand_sum += 10
            # now the dealer is done hitting and has their final value
            if hand_sum > 21:
                print("Dealer BUST \n")
                return 0
                # TODO implement logic for when the dealer busts
            else:
                return hand_sum

    def play(self):
        # the player always goes before the dealer in case they bust
        player_sum = self.opponent.agent_turn()
        # if the player didn't bust
        if player_sum > 0:
            # the dealer does their moves
            dealer_sum = self.dealer_turn()
            if dealer_sum == player_sum:
                print("Push \n")
            elif dealer_sum > player_sum:
                print("Dealer Wins! \n")
            elif player_sum > dealer_sum:
                print("Agent Wins! \n")
        else:
            print("Dealer Wins \n")
