from Settings import *
import random


class Agent:

    def __init__(self, deck):
        #this is the actual deck (it is shared memory so the agent may draw cards
        self.deck = deck

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
        print("Agent's Turn: \n")
        # the sum of all cards in the hand (simplifies code)
        # hand_sum[0] is the base hand, hand_sum[1] is only when the hands are split
        hand_sum = list()
        # create an array of the values of cards in hand (simplifies code)
        card_vals = []
        for i in range(0, len(self.hand)):
            card_vals.append(self.convert_handval(self.hand[i]))
        # if the cards are the same splitting is an option
        if self.hand[0].value == self.hand[1].value:
            if self.split(card_vals):
                # makes the second hand with the second card and removes it from the first hand
                self.splithand.append(self.hand.pop(1))
                # draws the extra cards for the two hands
                self.draw_card(self.deck.pop(0))
                card_vals.append(self.convert_handval(self.hand[1]))
                self.split_draw(self.deck.pop(0))
                card_vals.append(self.convert_handval(self.splithand[1]))
                # recalculates the hand sums
                hand_sum[0] = card_vals[0] + card_vals[2]
                hand_sum[1] = card_vals[1] + card_vals[3]
            # otherwise continue normally
            else:
                hand_sum[0] = sum(card_vals)
                # if there is an ace in the hand
                if 1 in card_vals:
                    hand_sum[0] += 10
                    # whatever value we have is considered a soft value (eg: soft 16 = Ace(11) + 5)
                    soft = True
        # otherwise continue normally
        else:
            hand_sum[0] = sum(card_vals)
            # if there is an ace in the hand
            if 1 in card_vals:
                hand_sum[0] += 10
                # whatever value we have is considered a soft value (eg: soft 16 = Ace(11) + 5)
                soft = True

        # TODO calculate odds of winning based on hits, stands, doubles, etc.
        # TODO Put all calculation logic here
        # TODO determine whether to hit, stand or double here (the actual work)

        if hand_sum[0] >= hand_sum[1]:
            return hand_sum[0]
        elif hand_sum[1] >= hand_sum[0]:
            return hand_sum[1]
        else:
            return 0

    def split(self, card_val):
        # card_val is the passed list of card values
        # the dealers card value
        DealerVal = self.convert_handval(self.SeenCard)
        # always split on 8s or aces
        if card_val[0] == 8 or card_val[0] == 1:
            return True
        # Never split on 10s, 5s, or 4s
        elif card_val[0] == 10 or card_val[0] == 5 or card_val[0] == 4:
            return False
        # special case for 2's and 3's cause Blackjack
        elif card_val[0] == 2 or card_val[0] == 3:
            # if DealerVal > 3 and DealerVal < 8:
            if 8 > DealerVal > 3:
                return True
            else:
                return False
        # special case for 9's as well
        elif card_val[0] == 9:
            if sum(card_val) > (self.convert_handval(self.SeenCard) + 10) or DealerVal == 8 or DealerVal == 9:
                return True
            else:
                return False
        # if your split wont result in you having disadvantage
        elif sum(card_val) > (self.convert_handval(self.SeenCard) + 10) or card_val[0] <= DealerVal:
            return True
        # if none of the conditions were met don't split
        return False

    def draw_card(self, card):
        self.hand.append(card)
        # TODO implement this forgetting code later, maybe after a round as the cards are discarded
        # rolls a number from 1 to 100, if its greater than the forget threshold don't remember it
        # if random.randint(1, 100) > self.forget:
        self.known_discard.append(card)
        self.known_deck.remove(card)

    def split_draw(self, card):
        self.splithand.append(card)
        self.known_discard.append(card)
        self.known_deck.remove(card)

    def see_card(self, card):
        self.known_deck.remove(card)
        self.known_discard.append(card)
        self.SeenCard = card

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
