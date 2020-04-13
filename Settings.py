from enum import Enum

# How likely the ai is to forget a card as its put in the discard
forgetfullness = (0/100)

# how much time to wait between moves (helps keep track of whats going on)
wait = 0.5

AI_MODE = 1
SLOW_MODE = True
SLEEP_TIME = 3

# the number of decks to shuffle together before the game starts
NUM_DECKS = 4
NUM_GAMES = 1

class GameModes(Enum):
    """ Modes that the simulation can be in for game play.
    """
    CLASSIC = 1
    SMARTDEALER = 2
