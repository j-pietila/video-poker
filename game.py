"""
Video Poker - Legendary Finnish Jokeri Pokeri by RAY
game.py: Game data and logic containing class for Video Poker
@author: Joonas Pietilä
"""

from cards import CardDeck

class PokerGame():
    """Game class for Video Poker"""

    def __init__(self, bet=0):
        self.betLevel = bet
        self.betLevels = [0.20, 0.40, 0.60, 0.80, 1.00]
        self.dealtCards = ["empty" for i in range(5)]
        self.deck = CardDeck()
        self.holdCards = [0, 0, 0, 0, 0]
        self.winTables = {
            0.20: [8.00, 8.00, 3.00, 1.60, 0.80, 0.60, 0.40, 0.40],
            0.40: [16.00, 16.00, 6.00, 3.20, 1.60, 1.20, 0.80, 0.80],
            0.60: [24.00, 24.00, 9.00, 4.80, 2.40, 1.80, 1.20, 1.20],
            0.80: [32.00, 32.00, 12.00, 6.40, 3.20, 2.40, 1.60, 1.60],
            1.00: [40.00, 40.00, 16.00, 8.00, 4.00, 3.00, 2.00, 2.00]
        }

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

    def changeWinTable(self):
        winTable = self.winTables.get(self.betLevels[self.betLevel])

        if winTable[1] < 10:
            winTableStr = """
                        Five-of-a-kind          {:.2f}
                        Straight Flush          {:.2f}
                        Four-of-a-kind          {:.2f}
                        Full house              {:.2f}
                        Flush                   {:.2f}
                        Straight                {:.2f}
                        Three-of-a-kind         {:.2f}
                        Two pairs               {:.2f}
                        """.format(*winTable)
        elif winTable[2] < 10:
            winTableStr = """
                        Five-of-a-kind         {:.2f}
                        Straight Flush         {:.2f}
                        Four-of-a-kind          {:.2f}
                        Full house              {:.2f}
                        Flush                   {:.2f}
                        Straight                {:.2f}
                        Three-of-a-kind         {:.2f}
                        Two pairs               {:.2f}
                        """.format(*winTable)
        else:
            winTableStr = """
                        Five-of-a-kind         {:.2f}
                        Straight Flush         {:.2f}
                        Four-of-a-kind         {:.2f}
                        Full house              {:.2f}
                        Flush                   {:.2f}
                        Straight                {:.2f}
                        Three-of-a-kind         {:.2f}
                        Two pairs               {:.2f}
                        """.format(*winTable)

        return winTableStr

    def deal(self):
        self.deck.buildDeck()
        self.deck.shuffle()

        self.dealtCards.clear()

        for i in range(5):
            self.dealtCards.append(self.deck.deck.pop(-1))

    def hold(self, index):
        if self.holdCards[index] == 0:
            self.holdCards[index] = 1
        else:
            self.holdCards[index] = 0
