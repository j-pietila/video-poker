"""
Video Poker - Legendary Finnish Jokeri Pokeri by RAY
game.py: Game data and logic containing class for Video Poker
@author: Joonas Pietilä
"""

from cards import CardDeck

class PokerGame():
    """Game class for Video Poker"""

    def __init__(self, bet=0):
        self.deck = CardDeck()
        self.dealt_cards = ["empty" for _ in range(5)]
        self.hold_card_flags = [0, 0, 0, 0, 0]
        self.bet_level = bet
        self.bet_levels = [0.20, 0.40, 0.60, 0.80, 1.00]
        self.winnings = 0.0
        self.current_win = 0.0
        self.win_tables = {
            0.20: [8.00, 8.00, 3.00, 1.60, 0.80, 0.60, 0.40, 0.40],
            0.40: [16.00, 16.00, 6.00, 3.20, 1.60, 1.20, 0.80, 0.80],
            0.60: [24.00, 24.00, 9.00, 4.80, 2.40, 1.80, 1.20, 1.20],
            0.80: [32.00, 32.00, 12.00, 6.40, 3.20, 2.40, 1.60, 1.60],
            1.00: [40.00, 40.00, 16.00, 8.00, 4.00, 3.00, 2.00, 2.00]
        }

    @property
    def bet_level(self):
        """Return __bet_level."""
        return self.__bet_level

    @bet_level.setter
    def bet_level(self, bet):
        """Set __bet_level with roll-over point at five."""
        if bet < 5:
            self.__bet_level = bet
        else:
            self.__bet_level = 0

    def change_bet(self):
        """Increase bet level by one, if game
        is in initial deal phase."""
        self.bet_level += 1

    def change_win_table(self):
        """Change current win table string according
        to current bet level."""
        win_table = self.win_tables.get(self.bet_levels[self.bet_level])

        if win_table[1] < 10:
            win_table_str = """
                        Five-of-a-kind          {:.2f}
                        Straight Flush          {:.2f}
                        Four-of-a-kind          {:.2f}
                        Full house              {:.2f}
                        Flush                   {:.2f}
                        Straight                {:.2f}
                        Three-of-a-kind         {:.2f}
                        Two pairs               {:.2f}
                        """.format(*win_table)
        elif win_table[2] < 10:
            win_table_str = """
                        Five-of-a-kind         {:.2f}
                        Straight Flush         {:.2f}
                        Four-of-a-kind          {:.2f}
                        Full house              {:.2f}
                        Flush                   {:.2f}
                        Straight                {:.2f}
                        Three-of-a-kind         {:.2f}
                        Two pairs               {:.2f}
                        """.format(*win_table)
        else:
            win_table_str = """
                        Five-of-a-kind         {:.2f}
                        Straight Flush         {:.2f}
                        Four-of-a-kind         {:.2f}
                        Full house              {:.2f}
                        Flush                   {:.2f}
                        Straight                {:.2f}
                        Three-of-a-kind         {:.2f}
                        Two pairs               {:.2f}
                        """.format(*win_table)

        return win_table_str

    def initial_deal(self) -> None:
        """
        Build and shuffle a new card deck and pop five
        cards from deck to dealt cards.
        """
        self.deck.build_deck()
        self.deck.shuffle()

        self.dealt_cards.clear()

        for _ in range(5):
            self.dealt_cards.append(self.deck.deck.pop(-1))

    def additional_deal(self) -> tuple[list[int], list[str]]:
        """
        Discard cards with hold card flag set to 0 replacing them
        with new cards popped from the deck. Reset hold card flags.
        Return lists of discarded cards indexes and strings.
        """
        discarded_cards = []
        discarded_cards_indexes = []
        discarded_cards_flags = enumerate(self.hold_card_flags)

        for i in discarded_cards_flags:
            if i[1] == 0:
                discarded_cards.append(self.dealt_cards[i[0]])
                discarded_cards_indexes.append(i[0])
                self.dealt_cards[i[0]] = self.deck.deck.pop(-1)

        current_win_index = self.check_win_category()

        if current_win_index == -1:
            self.current_win = 0.00
        else:
            self.current_win = \
                self.win_tables.get(self.bet_levels[self.bet_level])[current_win_index]

        self.hold_card_flags = [0, 0, 0, 0, 0]

        return discarded_cards_indexes, discarded_cards

    def hold(self, index):
        """
        Change cards hold flag at given index
        between 0 and 1 to indicate hold state.
        """
        if self.hold_card_flags[index] == 0:
            self.hold_card_flags[index] = 1
        else:
            self.hold_card_flags[index] = 0

    def prep_hand_for_checking(self):
        """Destructure the final hand to lists of jokers, values
        and suits. Return lists for the check_win_category function."""
        # Create copy of dealt_cards to keep GUI card updates intact.
        hand_to_check = self.dealt_cards.copy()

        jokers = []
        values = []
        suits = []

        # Split cards to value and suit for processing sublists.
        for i in range(len(hand_to_check)):
            if hand_to_check[i] != "Joker":
                card = [hand_to_check[i][:-1], hand_to_check[i][-1:]]
                hand_to_check[i] = card

        # Remove Joker from checked hand because it doesn't have value or suit.
        if "Joker" in hand_to_check:
            index = hand_to_check.index("Joker")
            jokers.append(hand_to_check.pop(index))

        for i in hand_to_check:
            values.append(i[0])
            suits.append(i[1])

        # Map face values to integers for determining straights.
        face_value_map = {"J": 11, "Q": 12, "K": 13, "A1": 1, "A2": 14}

        for i in range(len(values)):
            number_check = values[i].isnumeric()
            if number_check:
                values[i] = int(values[i])
            elif values[i] != "A":
                values[i] = face_value_map.get(values[i])

        # Ace can be 1 or 14, value determined by other cards.
        for i in values:
            if i == "A":
                index = values.index("A")
                lower_straight = [2, 3, 4]
                if any(i in values for i in lower_straight):
                    values[index] = face_value_map.get("A1")
                else:
                    values[index] = face_value_map.get("A2")

        values.sort()

        return jokers, values, suits

    def check_win_category(self):
        """Check the final hand and return win_table index
        according to win category. Return -1 for no win."""
        jokers, values, suits = self.prep_hand_for_checking()

        unique_values = set()
        unique_suits = set()

        for i in values:
            unique_values.add(i)

        for i in suits:
            unique_suits.add(i)

        # Check counts against value list length. Possible jokers are removed from it
        # and therefore jokers will always complete the hands accordingly.

        # 1. Five-of-a-kind
        for i in unique_values:
            if values.count(i) == len(values):
                return 0

        # 2. Straight Flush
        # Every card must be unique value and same suit.
        if len(unique_values) == len(values) and len(unique_suits) == 1:
            # Five cards, highest and lowest value difference of 4.
            if len(values) == 5 and values[-1] - values[0] == 4:
                return 1
            # Four cards, highest and lowest value difference of 4, joker completes middle.
            elif len(values) == 4 and values[-1] - values[0] == 4:
                return 1
            # Four cards, highest and lowest value difference of 3, joker completes either end.
            elif len(values) == 4 and values[-1] - values[0] + len(jokers) == 4:
                return 1

        # 3. Four-of-a-kind
        for i in unique_values:
            # Account for possible jokers by subtracting one from the values length.
            if values.count(i) == len(values) - 1:
                return 2

        # 4. Full house
        # Four-of-a-kind already checked. If there are only two distinct values, it is full house.
        if len(unique_values) == 2:
            return 3

        # 5. Flush
        if len(unique_suits) == 1:
            return 4

        # 6. Straight
        # Every card must be of unique value.
        if len(unique_values) == len(values):
            # Five cards, highest and lowest value difference of 4.
            if len(values) == 5 and values[-1] - values[0] == 4:
                return 5
            # Four cards, highest and lowest value difference of 4, joker completes middle.
            elif len(values) == 4 and values[-1] - values[0] == 4:
                return 5
            # Four cards, highest and lowest value difference of 3, joker completes either end.
            elif len(values) == 4 and values[-1] - values[0] + len(jokers) == 4:
                return 5

        # 7. Three-of-a-kind
        for i in unique_values:
            # Account for possible jokers by subtracting two from the values length.
            if values.count(i) == len(values) - 2:
                return 6

        # 8. Two pairs
        # After all the other checks three distinct values leaves two pairs.
        if len(unique_values) == 3:
            return 7

        # 9. No win
        return -1

    def double(self):
        """Double current win and deal one random card from
        newly built and shuffled card deck."""
        self.current_win *= 2

        self.deck.build_deck()
        self.deck.shuffle()

        self.dealt_cards = ["empty" for i in range(5)]
        self.dealt_cards[2] = self.deck.deck.pop(-1)

    def check_doubling_result(self, double_choice):
        """Return True for succesfull doubling if doubling card is
        Joker or in double choice from GUI. Return False if not."""
        if self.dealt_cards[2][:-1] in double_choice:
            return True
        if self.dealt_cards[2] == "Joker":
            return True

        self.current_win = 0.0

        return False

    def collect_current_win(self):
        """Transfer current win to overall winnings."""
        self.winnings += self.current_win
        self.current_win = 0.0
