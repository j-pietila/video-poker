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
        self.isInitialDeal = True
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
        if self.isInitialDeal:
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
        if self.isInitialDeal:
            self.initialDeal()
        else:
            self.additionalDeal()

    def initialDeal(self):
        self.deck.buildDeck()
        self.deck.shuffle()

        self.dealtCards.clear()

        for i in range(5):
            self.dealtCards.append(self.deck.deck.pop(-1))

        self.isInitialDeal = False

    def additionalDeal(self):
        self.discardedCards = enumerate(self.holdCards)
        
        for i in self.discardedCards:
            if i[1] == 0:
                self.dealtCards[i[0]] = self.deck.deck.pop(-1)

        self.currentWinIndex = self.checkHand()

        if self.currentWinIndex == -1:
            self.currentWin = 0.00
        else:
            self.currentWin = self.winTables.get(self.betLevels[self.betLevel])[self.currentWinIndex]

        print("Won: {}".format(self.currentWin))

        self.holdCards = [0, 0, 0, 0, 0]

        self.isInitialDeal = True

    def hold(self, index):
        if not self.isInitialDeal:
            if self.holdCards[index] == 0:
                self.holdCards[index] = 1
            else:
                self.holdCards[index] = 0

    def prepHand(self):
        # Create copy of dealtCards to keep GUI card updates intact
        self.handToCheck = self.dealtCards.copy()
        self.jokers = []

        # Split cards to value and suit for processing sublists
        for i in range(len(self.handToCheck)):
            if self.handToCheck[i] != "Joker":
                self.card = [self.handToCheck[i][:-1], self.handToCheck[i][-1:]]
                self.handToCheck[i] = self.card

        # Remove Joker from checked hand because it doesn't have value or suit
        if "Joker" in self.handToCheck:
            index = self.handToCheck.index("Joker")
            self.jokers.append(self.handToCheck.pop(index))

        self.values = []
        self.suites = []

        for i in self.handToCheck:
            self.values.append(i[0])
            self.suites.append(i[1])

        # Values converted to integers for determining straights
        valueMap = {"J": 11, "Q": 12, "K": 13, "A1": 1, "A2": 14}

        for i in range(len(self.values)):
            self.numberCheck = self.values[i].isnumeric()
            if self.numberCheck:
                self.values[i] = int(self.values[i])
            elif self.values[i] != "A":
                self.values[i] = valueMap.get(self.values[i])

        # Ace can be 1 or 14, value determined by other cards and possible Jokers
        for i in self.values:
            if i == "A":
                index = self.values.index("A")
                lowerStraight = [2, 3, 4]
                if any(i in self.values for i in lowerStraight):
                    self.values[index] = valueMap.get("A1")
                else:
                    self.values[index] = valueMap.get("A2")

        self.values.sort()

    def checkHand(self):
        """Checks the prepared final hand and returns winTable index according to possible win"""
        self.prepHand()

        uniqueValues = set()
        uniqueSuits = set()

        for i in self.values:
            uniqueValues.add(i)

        for i in self.suites:
            uniqueSuits.add(i)

        # Counts are checked against length of values list, because possible jokers are removed from that lists
        # and so the possible jokers will always complete the hands accordingly

        # 1. Five-of-a-kind
        for i in uniqueValues:
            if self.values.count(i) == len(self.values):
                return 0

        # 2. Straight Flush
        if len(uniqueValues) == len(self.values) and len(uniqueSuits) == 1: # Every card must be unique value and same suit
            if len(self.values) == 5 and self.values[-1] - self.values[0] == 4: # Five cards, sorted highest and lowest value difference of 4
                return 1
            elif len(self.values) == 4 and self.values[-1] - self.values[0] == 4: # Four cards, sorted highest and lowest value difference of 4, joker completes middle
                return 1
            elif len(self.values) == 4 and self.values[-1] - self.values[0] + len(self.jokers) == 4: # Four cards, sorted highest and lowest value difference of 3, joker completes either end
                return 1

        # 3. Four-of-a-kind
        for i in uniqueValues:
            if self.values.count(i) == len(self.values) - 1: # By subtracting one from the len of values we account for possible jokers
                return 2

        # 4. Full house
        if len(uniqueValues) == 2: # Four-of-a-kind is already checked, if there are only two distinct values it must be full house
            return 3

        # 5. Flush
        if len(uniqueSuits) == 1: 
            return 4

        # 6. Straight
        if len(uniqueValues) == len(self.values): # Every card must be unique value
            if len(self.values) == 5 and self.values[-1] - self.values[0] == 4: # Five cards, sorted highest and lowest value difference of 4
                return 5
            elif len(self.values) == 4 and self.values[-1] - self.values[0] == 4: # Four cards, sorted highest and lowest value difference of 4, joker completes middle
                return 5
            elif len(self.values) == 4 and self.values[-1] - self.values[0] + len(self.jokers) == 4: # Four cards, sorted highest and lowest value difference of 3, joker completes either end
                return 5

        # 7. Three-of-a-kind
        for i in uniqueValues:
            if self.values.count(i) == len(self.values) - 2: # By subtracting two from the len of values we account for possible jokers
                return 6

        # 8. Two pairs
        if len(uniqueValues) == 3: # After all the other checks three distinct values leaves two pairs
            return 7

        # No win
        return -1
