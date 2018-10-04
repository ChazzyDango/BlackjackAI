from Settings import *
import random


class Agent:

    def __init__(self, deck):
        # this is the actual deck (it is shared memory so the agent may draw cards
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
        hand_sum = [0, 0]
        # a simple condition to check if we have split yet
        split = False
        soft = [False, False]
        # create an array of the values of cards in hand (simplifies code)
        card_vals = []
        for i in range(0, len(self.hand)):
            card_vals.append(self.convert_handval(self.hand[i]))
        # if the cards are the same splitting is an option
        if self.hand[0].value == self.hand[1].value:
            if self.split(card_vals):
                split = True
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
                    soft[0] = True
        # otherwise continue normally
        else:
            hand_sum[0] = sum(card_vals)
            # if there is an ace in the hand
            if self.hand[0].value == 'Ace' or self.hand[1].value == 'Ace':
                hand_sum[0] += 10
                # whatever value we have is considered a soft value (eg: soft 16 = Ace(11) + 5)
                soft[0] = True
            if split:
                # if there is an ace in the split hand
                if self.splithand[0].value == 'Ace' or self.splithand[1].value == 'Ace':
                    hand_sum[1] += 10
                    soft[1] = True

        # TODO calculate odds of winning based on hits, stands, doubles, etc.
        # TODO Put all calculation logic here
        # TODO determine whether to hit, stand or double here (the actual work)
        DealerVal = self.convert_handval(self.SeenCard)
        if DealerVal == 1:
            DealerVal = 11
        for j in range(0, len(hand_sum)):
            # if we iterate to the other split pair and we didn't split
            if hand_sum[j] == 0:
                break
            Stand = False
            while(Stand == False):
                # this will be the loop where moves are decided
                # Number of cards left in the deck
                CardsLeft = len(self.known_deck)
                fail = 0
                Dwin = 0
                adv = 0
                # TODO manage aces within the calculations
                # a look to scan through all cards still left in the deck (that we know of)
                for i in range(0, CardsLeft):
                    Cardi = self.convert_handval(self.known_deck[i])
                    if soft[j] == False:
                        # if the card it is currently looking at would bust us on a hit
                        if (hand_sum[j] + Cardi) > 21:
                            fail += 1
                    elif soft[j]:
                        # if we hit and we end up with a lower value when soft
                        if (hand_sum[j] + Cardi) > 21:
                            if hand_sum[j] + Cardi - 10 < hand_sum[j]:
                                fail += 1
                    # if your hand is really low and the simulated card is an ace
                    if hand_sum[j] <= 10 and soft[j] == True:
                        if Cardi == 1:
                            Cardi = 11
                        # if hitting would not bust us and give us advantage!
                        if 22 > (hand_sum[j] + Cardi) > (DealerVal + 10):
                            adv += 1
                    else:
                        # if hitting would not bust us and give us advantage!
                        if 22 > (hand_sum[j] + Cardi) > (DealerVal + 10):
                            adv += 1
                    # handling hidden aces for the dealer
                    if Cardi == 1:
                        Cardi = 11
                    # the amount of cards the dealer could get that beat our hand currently + 6 average
                    if (22 > (DealerVal + Cardi) >= hand_sum[j]) and \
                            ((DealerVal + Cardi >= 17) or (Cardi == 11 and DealerVal + Cardi > 17)):
                        Dwin += 1
                    # adv should always be less than fail
                    # the closer they are and the lower they are the more likely we hit
                print("Current Total: %f \n" % hand_sum[j])
                print("Odds of Busting: %f" % (fail/CardsLeft))
                print("Odds of gaining advantage: %f" % (adv / CardsLeft))
                print("Odds of dealer winning with the hidden card if we stand now: %f" % (Dwin/CardsLeft))

                if soft[j] == True and hand_sum[j] >= 19 and Stand == False:
                    if Stand == False:
                        print("Stand")
                    Stand = True
                elif hand_sum[j] >= 17 and soft[j] == False and Stand == False:
                    if Stand == False:
                        print("Stand")
                    Stand = True
                elif hand_sum[j] >= 20 and Stand == False:
                    if Stand == False:
                        print("Stand")
                    Stand = True

                FailMinusAdv = (fail/CardsLeft) - (adv / CardsLeft)
                if FailMinusAdv < 0:
                    FailMinusAdv = 0

                if (FailMinusAdv) >= (Dwin/CardsLeft) and (fail/CardsLeft) > 0.45 or Stand == True:
                    if Stand == False:
                        print("Stand")
                    Stand = True
                elif (adv / CardsLeft) > (((fail/CardsLeft))+(Dwin/CardsLeft)) or (Dwin/CardsLeft) > 0.45 or \
                        (soft[j] == False and (fail/CardsLeft) <= 0.10):
                    print("Hit")
                    NewCard = self.deck.pop()
                    if j == 0:
                        self.draw_card(NewCard)
                    elif j == 1:
                        self.split_draw(NewCard)
                    hand_sum[j] += self.convert_handval(NewCard)
                    if hand_sum[j] > 21:
                        Stand = True
                        print("Agent Bust!")
                    else:
                        print ("New Total Is %d" % hand_sum[j])

                # the dealer has to have at least 17
                # if your score is below 17 all
                # you care about is if your odds of not busting are greater than them not busting

                # if youre over 17 all you care about is the odds of the dealer beating you right now (Dwin)

                # if were at a hard 11 or below we always hit (its impossible to bust)
                # also if the odds of busting are less than 10% we hit
                if (soft[j] == False) and hand_sum[j] <= 11:
                    # HIT
                    print("Hit")
                    NewCard = self.deck.pop()
                    if j == 0:
                        self.draw_card(NewCard)
                    elif j == 1:
                        self.split_draw(NewCard)
                    hand_sum[j] += self.convert_handval(NewCard)
                    print("New Total Is %d" % hand_sum[j])
                    if hand_sum[j] > 21:
                        print("Agent Bust!")
                        Stand = True
                # if were at a soft 17 or below we always hit as well
                if (soft[j] == True) and hand_sum[j] <= 17:
                    # HIT
                    print("Hit")
                    NewCard = self.deck.pop()
                    if j == 0:
                        self.draw_card(NewCard)
                    elif j == 1:
                        self.split_draw(NewCard)
                    hand_sum[j] += self.convert_handval(NewCard)
                    # since its a soft hand if we go over we can just decrease the hand by 10 and make it not soft
                    if hand_sum[j] > 21:
                        hand_sum[j] -= 10
                        soft[j] = False
                    print("New Total Is %d" % hand_sum[j])
                if soft[j] == True and hand_sum[j] >= 19 and Stand == False:
                    if Stand == False:
                        print("Stand")
                    Stand = True
                elif hand_sum[j] >= 17 and soft[j] == False and Stand == False:
                    if Stand == False:
                        print("Stand")
                    Stand = True
                elif hand_sum[j] >= 20 and Stand == False:
                    if Stand == False:
                        print("Stand")
                    Stand = True

        # TODO check known conditions
        if hand_sum[0] > 21:
            hand_sum[0] = 0
        if hand_sum[1] > 21:
            hand_sum[1] = 0
        if hand_sum[0] == 0 and hand_sum[1] == 0:
            return 0
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
        print("Got a %s of %s" % (card.value, card.colour))
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
