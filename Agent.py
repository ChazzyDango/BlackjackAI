from Settings import *
import random


class Agent:

    def __init__(self, deck):
        self.known_deck = list()
        for cards in deck:
            self.known_deck.append(cards)
        self.hand = list()
        self.splithand = list()
        # the card the agent sees that the dealer reveals
        self.SeenCard = None

        # This array is the cards known to be discarded, it exists for debugging purposes and data analysis
        self.known_discard = []
        # in case i want to make the agent forget cards ocassionally (From Settings.py)
        self.forget = forgetfullness

    def agent_turn(self):
        # TODO calculate odds of winning based on hits, stands, doubles, etc.
        # TODO Put all calculation logic here
        # TODO don't forget splitting pairs here
        print("Agent's Turn: \n")
        # the sum of all cards in the hand (simplifies code)
        # hand_sum[0] is the base hand, hand_sum[1] is only when the hands are split
        hand_sum = list()
        # create an array of the values of cards in hand (simplifies code)
        card_vals = []
        for i in range(0, len(self.hand)):
            card_vals.append(self.convert_handval(self.hand[i]))
        # if the cards are the same splitting is an option
        if card_vals[0] == card_vals[1]:
            if self.split():
                # makes the second hand with the second card and removes it from the first hand
                self.splithand.append(self.hand.pop(1))
            # recalculates the hand sums
            hand_sum[0] = card_vals[0]
            hand_sum[1] = card_vals[1]
        # otherwise continue normally
        else:
            hand_sum[0] = sum(card_vals)
            # if there is an ace in the hand
            if 1 in card_vals:
                hand_sum[0] += 10
                # whatever value we have is considered a soft value (eg: soft 16 = Ace(11) + 5)
                soft = True

        # TODO determine whether to hit, stand or double here

        if hand_sum[0] >= hand_sum[1]:
            return hand_sum[0]
        elif hand_sum[1] >= hand_sum[0]:
            return hand_sum[1]
        else:
            return 0

    def split(self):
        # TODO check if the agent should split on pairs
        print("Should I Split?")
        return False

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
        self.SeenCard = card

