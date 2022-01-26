"""
Video Poker - Legendary Finnish Jokeri Pokeri by RAY
cards.py: Card deck class for Video Poker
@author: Joonas Pietilä
"""

from random import randint

class CardDeck():
    """Playing card deck for Video Poker"""

    def __init__(self):
        self.build_deck()

    def build_deck(self):
        """Build a standard 52 card deck with one Joker. Deck is
        a list of strings "value+suit" representing cards."""
        self.deck = ["Joker"]

        suit = ["C", "D", "H", "S"]
        face_values = ["J", "Q", "K", "A"]

        for value in range(2, 11):
            for suite in suit:
                self.deck.append(str(value) + suite)

        for face in face_values:
            for suite in suit:
                self.deck.append(face + suite)

    def shuffle(self):
        """Fisher-Yates-Knuth in-place shuffle algorithm
        for unbiased permutations"""
        # Initial unshuffled sublists border is last array index
        un_shuffled = len(self.deck) - 1

        while un_shuffled > 0:
            # Shuffled index has to be selected randomly
            to_shuffle = randint(0, un_shuffled)

            self.deck[to_shuffle], self.deck[un_shuffled] \
                = self.deck[un_shuffled], self.deck[to_shuffle]

            # Update the unshuffled sublist border index
            un_shuffled -= 1
