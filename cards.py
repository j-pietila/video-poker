"""
Video Poker - Legendary Finnish Jokeri Pokeri by RAY
cards.py: Card deck class for Video Poker
@author: Joonas Pietilä
"""

from random import randint

class CardDeck():
    """Playing card deck for Video Poker"""

    def __init__(self):
        self.buildDeck()

    def buildDeck(self):
        self.deck = ["Joker"]
        self.suits = ["C", "D", "H", "S"]
        self.faceValues = ["J", "Q", "K", "A"]

        for i in range(2, 11):
            for j in self.suits:
                self.deck.append(str(i) + j)

        for i in self.faceValues:
            for j in self.suits:
                self.deck.append(i + j)

    def shuffle(self):
        """Fisher-Yates-Knuth in-place shuffle algorithm for unbiased permutations"""
        # Initial unshuffled sublists border is last array index
        unShuffled = len(self.deck) - 1

        while unShuffled > 0:
            # Shuffled index has to be selected randomly
            toShuffle = randint(0, unShuffled)

            self.deck[toShuffle], self.deck[unShuffled] = self.deck[unShuffled], self.deck[toShuffle]

            # Update the unshuffled sublist border index
            unShuffled -= 1
