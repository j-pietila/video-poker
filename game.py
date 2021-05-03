"""
Video Poker - Legendary Finnish Jokeri Pokeri by RAY
game.py: Game data and logic containing class for Video Poker
@author: Joonas Pietilä
"""

class PokerGame():
    """Game class for Video Poker"""

    def __init__(self, bet=0):
        self.betLevel = bet
        self.betLevels = [0.20, 0.40, 0.60, 0.80, 1.00]

    @property
    def betLevel(self):
        return self.__betLevel

    @betLevel.setter
    def betLevel(self, bet):
        if bet < 5:
            self.__betLevel = bet
        else:
            self.__betLevel = 0

    def changeBet(self):
        self.betLevel += 1
