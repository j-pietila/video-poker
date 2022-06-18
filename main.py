"""
Video Poker - Legendary Finnish Jokeri Pokeri by RAY
main.py: Main program file for Video Poker containing the tkinter GUI class
@author: Joonas Pietilä
"""

import tkinter as tk

from PIL import ImageTk, Image

from game import PokerGame

class PokerGUI(tk.Tk):
    """Tkinter GUI class for Video Poker"""

    def __init__(self):
        super().__init__()
        self.game = PokerGame()
        self.dealt_hand = self.load_card_images(self.game.dealt_cards)
        self.first_deal = True
        self.doubling_active = False
        self.doubling_choice_active = False
        self.create_layout()

    @staticmethod
    def resize_and_create_image_object(image_path: str) -> ImageTk.PhotoImage:
        """Resize and create image object for tkinter."""
        card = Image.open(image_path)
        card = card.resize((140, 215))
        return ImageTk.PhotoImage(card)

    def load_card_images(self, dealt_cards: list[str]) -> list[ImageTk.PhotoImage]:
        """
        Load card image files for dealt cards based on
        the dealt_cards list in the game module.
        """
        self.card_back = self.resize_and_create_image_object("./PlayingCards/cardBack.png")
        self.empty_card = self.resize_and_create_image_object("./PlayingCards/empty.png")

        dealt_hand = []

        for i in range(5):
            dealt_hand.append(self.resize_and_create_image_object(
                f"./PlayingCards/{dealt_cards[i]}.png"))

        return dealt_hand

    def update_hold_labels(self, index):
        """Update GUI hold card label visibility status."""
        hold_labels = {
            0: self.first_card_hold_label_window,
            1: self.second_card_hold_label_window,
            2: self.third_card_hold_label_window,
            3: self.fourth_card_hold_label_window,
            4: self.fifth_card_hold_label_window
        }

        if self.game.hold_card_flags[index] == 0:
            self.bottom_bar.itemconfigure(hold_labels.get(index), state="hidden")
        else:
            self.bottom_bar.itemconfigure(hold_labels.get(index), state="normal")

    def clear_hold_labels(self):
        """Set all GUI hold card labels to hidden status."""
        self.bottom_bar.itemconfigure(self.first_card_hold_label_window, state="hidden")
        self.bottom_bar.itemconfigure(self.second_card_hold_label_window, state="hidden")
        self.bottom_bar.itemconfigure(self.third_card_hold_label_window, state="hidden")
        self.bottom_bar.itemconfigure(self.fourth_card_hold_label_window, state="hidden")
        self.bottom_bar.itemconfigure(self.fifth_card_hold_label_window, state="hidden")

    def winning_hand_view(self):
        """Update GUI to show winning hand view."""
        if self.game.current_win > 0:
            self.bottom_bar.configure(bg="DeepPink3")
            self.rolling_double_options_label.config(bg="DeepPink3")
            self.bottom_bar.coords(self.current_win_window, 600, 18)
            self.current_win.set(f"{self.game.current_win:.2f}")
            self.bottom_bar.itemconfigure(self.current_win_window, state="normal")
            self.bottom_bar.itemconfigure(self.double_question_window, state="normal")
            self.bottom_bar.itemconfigure(self.active_doubling_window, state="hidden")

    def no_win_view(self):
        """Update GUI to show losing hand view."""
        self.bottom_bar.configure(bg="snow4")
        self.rolling_double_options_label.config(bg="snow4")
        self.bottom_bar.coords(self.current_win_window, 600, 18)
        self.current_win.set(f"{self.game.current_win:.2f}")
        self.bottom_bar.itemconfigure(self.current_win_window, state="hidden")
        self.bottom_bar.itemconfigure(self.double_question_window, state="hidden")
        self.bottom_bar.itemconfigure(self.active_doubling_window, state="hidden")

    def active_doubling_view(self):
        """Update GUI to show active doubling view."""
        self.bottom_bar.coords(self.current_win_window, 270, 16)
        self.current_win.set(f"{self.game.current_win:.2f}")
        self.rolling_double_options_label.config(bg="DeepPink3")
        self.bottom_bar.itemconfigure(self.double_question_window, state="hidden")
        self.bottom_bar.itemconfigure(self.active_doubling_window, state="normal")

    def after_doubling_view(self, double_win):
        """Update GUI to show either win or no win view after
        doubling based on the double_win result."""
        if double_win:
            self.winning_hand_view()
        else:
            self.no_win_view()

        self.doubling_choice_active = False
        self.doubling_options.set("")
        self.rolling_double_options_label.place(x=2, y=20)
        self.bottom_bar.itemconfigure(self.rolling_double_options_window, state="hidden")
        self.bottom_bar.itemconfigure(self.rolling_double_options_left_mask_window, state="hidden")
        self.bottom_bar.itemconfigure(self.rolling_double_options_right_mask_window, state="hidden")

        self.dealt_hand = self.load_card_images(self.game.dealt_cards)
        self.middle_area.itemconfig(self.third_card, image=self.dealt_hand[2])

    def change_bet(self):
        """Event handler for bet button. Run change bet function
        from game module and update GUI accordingly."""
        self.game.change_bet()

        self.bet.set(f"Bet {self.game.bet_levels[self.game.bet_level]:.2f}")
        self.middle_area.itemconfigure(
            self.winning_table_text,
            text=self.game.change_win_table()
        )

    def deal(self):
        """Event handler for deal button. Run deal function from game
        module and update GUI elements for changed cards and possible
        winning hand view."""
        if self.game.current_win == 0:
            discarded_cards_indexes, discarded_cards = self.game.deal()
            self.clear_hold_labels()

            # Deal animations
            # Running initial deal function sets initial deal flag to false
            if not self.game.is_initial_deal:
                if not self.first_deal:
                    if self.doubling_active:
                        self.collect_doubling_card_back_animation()
                        self.doubling_active = False
                    else:
                        self.collect_cards_back_animation()
                self.dealt_hand = self.load_card_images(self.game.dealt_cards)
                self.deck_shuffle_animation(self.card_stack)
                self.initial_deal_animation(self.dealt_hand)
                self.first_deal = False
            else:
                self.dealt_hand = self.load_card_images(self.game.dealt_cards)
                self.additional_deal_animation(
                    self.dealt_hand, discarded_cards_indexes, discarded_cards)

            if self.game.current_win > 0:
                self.winning_hand_view()
            else:
                self.no_win_view()

    def hold(self, card_index):
        """Event handler for hold buttons. Change hold status of the
        card at given card index and update GUI accordingly."""
        self.game.hold(card_index)
        self.update_hold_labels(card_index)

    def activate_doubling(self):
        """Event handler for double button. Run doubling function from
        game module and update GUI elements to active doubling view."""
        if not self.game.is_doubling_active and self.game.current_win > 0:
            self.game.double()
            self.active_doubling_view()

            if self.doubling_active:
                self.collect_doubling_card_back_animation()
            else:
                self.collect_cards_back_animation()
                self.doubling_active = True

            self.deck_shuffle_animation(self.card_stack)
            self.deal_doubling_card_animation()

    def select_low(self):
        """Event handler for low button. Run doubling result check
        from game module with low card range selection and update
        GUI according to doubling result."""
        if self.game.is_doubling_active:
            double_choice = ["A", "2", "3", "4", "5", "6"]
            double_win = self.game.check_doubling_result(double_choice)
            self.after_doubling_view(double_win)

    def select_high(self):
        """Event handler for high button. Run doubling result check
        from game module with high card range selection and update
        GUI according to doubling result."""
        if self.game.is_doubling_active:
            double_choice = ["8", "9", "10", "J", "Q", "K"]
            double_win = self.game.check_doubling_result(double_choice)
            self.after_doubling_view(double_win)

    def collect_current_win(self):
        """Event handler for collect button. Collect current win with
        a GUI counting sequence animation and set GUI to base state."""
        self.collect_current_win_animation()
        self.no_win_view()

    def collect_current_win_animation(self):
        """Animation to transfer current win to overall winnings."""
        win_update = self.game.current_win
        decrement = win_update / 8
        self.game.collect_current_win()

        for i in range(7, -1, -1):
            win_update -= decrement
            self.after(250, self.wins.set(f"Wins {self.game.winnings - (i * decrement):.2f}"))
            # Occasional final result is -0.00, hence abs()
            self.current_win.set(f"{abs(win_update):.2f}")
            self.update()

    @staticmethod
    def get_coordinate_increments(
        coords_difference: tuple[int, int], steps: int
    ) -> tuple[int, int]:
        """Return a tuple holding increment for x and y coordinates
        for given amount of steps for the animation."""
        x_increment = coords_difference[0] / steps
        y_increment = coords_difference[1] / steps

        return (x_increment, y_increment)

    def update_dealt_card_position(self, card, x_pos, y_pos):
        """Update card (x, y) position during the card deal animation."""
        self.middle_area.move(card, x_pos, y_pos)
        self.update()

    def reveal_initial_cards_animation(
        self, dealt_cards, cards: list[ImageTk.PhotoImage]
    ) -> None:
        """Update dealt initial hand cards with their real face value images."""
        for i, card in enumerate(dealt_cards):
            self.after(150, self.middle_area.itemconfig(card, image=cards[i]))
            self.update()

    def reveal_last_card_animation(self, increment: int, steps: int) -> int:
        """Run animation for revealing last card being dealt."""
        frame_time_ms = round(2500 / steps)
        reset_y = 0

        for i in range(steps):
            self.after(frame_time_ms, self.update_dealt_card_position(
                self.card_in_transit, 0, increment * i
            ))
            reset_y += increment * i

        return reset_y

    def deck_shuffle_animation(self, card_deck: list) -> None:
        """Animate deck shuffling before dealing initial hand."""
        for i in range(4):
            modulo = 1 if i % 2 == 0 else 0
            for j in range(6):
                x_increment = 25 if j < 3 else -25
                y_increment = -6 if j < 3 else 6
                for val, card in enumerate(card_deck):
                    if val % 2 == modulo:
                        self.after(2, self.update_dealt_card_position(
                            card, x_increment, y_increment
                        ))
                    else:
                        self.after(2, self.update_dealt_card_position(
                            card, x_increment * -1/3, y_increment * -1/3
                        ))

    def animate_dealt_card(
        self, card_in_transit, coords_difference: tuple[int, int], steps: int,
        last_card = None, card: ImageTk.PhotoImage = None
    ) -> None:
        """
        Animate card deal from card stack to dealt card location. Last card is slowly
        revealed, if given as parameter. Reset dealt card back to card stack after animations.
        """
        increments = self.get_coordinate_increments(coords_difference, steps)
        frame_time_ms = round(200 / steps)
        self.middle_area.itemconfig(card_in_transit, image=self.card_back)
        self.middle_area.tag_raise(card_in_transit)

        for _ in range(steps):
            self.after(frame_time_ms, self.update_dealt_card_position(
                card_in_transit, increments[0], increments[1]
            ))

        if last_card:
            increment = 1
            self.middle_area.itemconfig(last_card, image=card)
            reset_y_additional = self.reveal_last_card_animation(increment, steps)
            reset_x = increments[0] * steps * -1
            reset_y = (increments[1] * steps + reset_y_additional) * -1
        else:
            reset_x = increments[0] * steps * -1
            reset_y = increments[1] * steps * -1

        self.middle_area.itemconfig(card_in_transit, image=self.empty_card)
        self.middle_area.move(card_in_transit, reset_x, reset_y)
        self.update()

    def initial_deal_animation(self, cards: list[ImageTk.PhotoImage]) -> None:
        """Run initial deal animations."""
        dealt_cards = [
            self.first_card, self.second_card, self.third_card, self.fourth_card, self.fifth_card
        ]

        self.animate_dealt_card(self.card_in_transit, (-14, 304), 10)
        self.middle_area.itemconfig(dealt_cards[0], image=self.card_back)
        self.animate_dealt_card(self.card_in_transit, (171, 304), 10)
        self.middle_area.itemconfig(dealt_cards[1], image=self.card_back)
        self.animate_dealt_card(self.card_in_transit, (356, 304), 10)
        self.middle_area.itemconfig(dealt_cards[2], image=self.card_back)
        self.animate_dealt_card(self.card_in_transit, (541, 304), 10)
        self.middle_area.itemconfig(dealt_cards[3], image=self.card_back)
        self.animate_dealt_card(self.card_in_transit, (726, 304), 10)
        self.middle_area.itemconfig(dealt_cards[4], image=self.card_back)

        self.reveal_initial_cards_animation(dealt_cards, cards)

    def discard_card_animation(self, card, steps: int) -> None:
        """Run animation for discarding card through the bottom of the screen."""
        increment = 40
        frame_time_ms = round(200 / steps)

        for _ in range(steps):
            self.after(frame_time_ms, self.update_dealt_card_position(card, 0, increment))

        empty_card = self.resize_and_create_image_object("./PlayingCards/empty.png")
        self.middle_area.itemconfig(card, image=empty_card)

        reset_y = increment * steps * -1
        self.middle_area.move(card, 0, reset_y)
        self.update()

    def additional_deal_animation(
        self, cards: list[ImageTk.PhotoImage],
        discarded_cards_indexes: list[int],
        discarded_cards: list[str]
    ) -> None:
        """Run animations for discarded cards out of the screen and deal new ones."""
        discarded_cards_images = []
        dealt_card_end_coordinates = [(-14, 304), (171, 304), (356, 304), (541, 304), (726, 304)]
        dealt_cards = [
            self.first_card, self.second_card, self.third_card,
            self.fourth_card, self.fifth_card
        ]

        # Update kept cards
        for i in range(5):
            if i not in discarded_cards_indexes:
                self.middle_area.itemconfig(dealt_cards[i], image=cards[i])

        # Recreate old images for the to be discarded cards
        discarded = 0
        for i in discarded_cards_indexes:
            discarded_cards_images.append(self.resize_and_create_image_object(
                f"./PlayingCards/{discarded_cards[discarded]}.png"))
            discarded += 1

        # Keep discarded cards with old images before discard animation
        discarded = 0
        for i in discarded_cards_indexes:
            self.middle_area.itemconfig(dealt_cards[i], image=discarded_cards_images[discarded])
            discarded += 1

        # Run discard animations
        for i in discarded_cards_indexes:
            self.discard_card_animation(dealt_cards[i], 8)

        # Update discarded cards with new ones
        discarded = 1
        for i in discarded_cards_indexes:
            if discarded == len(discarded_cards_indexes):
                self.animate_dealt_card(
                    self.card_in_transit, dealt_card_end_coordinates[i], 25,
                    dealt_cards[i], cards[i]
                )
            else:
                self.animate_dealt_card(self.card_in_transit, dealt_card_end_coordinates[i], 10)
                self.middle_area.itemconfig(dealt_cards[i], image=cards[i])

            discarded += 1

    def collect_cards_back_animation(self):
        """Animate collecting cards back to deck from table."""
        dealt_cards = [
            self.first_card, self.second_card, self.third_card, self.fourth_card, self.fifth_card
        ]

        # Target coordinates are at (84, 31) on top of card deck
        self.animate_dealt_card(dealt_cards[0], (14, -304), 10)
        self.animate_dealt_card(dealt_cards[1], (-171, -304), 10)
        self.animate_dealt_card(dealt_cards[2], (-356, -304), 10)
        self.animate_dealt_card(dealt_cards[3], (-541, -304), 10)
        self.animate_dealt_card(dealt_cards[4], (-726, -304), 10)

    def deal_doubling_card_animation(self) -> None:
        """
        Deal the card used with doubling and activate rolling doubling
        choices text animation after the doubling card has been dealt.
        """
        self.middle_area.move(self.third_card, -356, -304)
        self.animate_dealt_card(self.third_card, (356, 304), 10)
        self.middle_area.move(self.third_card, 356, 304)
        self.middle_area.itemconfig(self.third_card, image=self.card_back)

        self.bottom_bar.itemconfigure(self.rolling_double_options_window, state="normal")
        self.bottom_bar.itemconfigure(self.rolling_double_options_left_mask_window, state="normal")
        self.bottom_bar.itemconfigure(self.rolling_double_options_right_mask_window, state="normal")
        self.doubling_choice_active = True
        self.rolling_doubling_options_animation()

    def rolling_doubling_options_animation(self) -> None:
        """Animate the rolling doubling options text."""
        text1 = "A 2 3 4 5 6 OR 8 9 10 J Q K OR A 2 3 4 5 6"
        text2 = "8 9 10 J Q K OR A 2 3 4 5 6 OR 8 9 10 J Q K"
        self.doubling_options.set(text1)
        self.rolling_double_options_label.config(bg="DeepPink3")
        x_pos = 510

        while self.doubling_choice_active:
            if x_pos <= 180 and self.doubling_options.get() == text1:
                x_pos = 510
                self.doubling_options.set(text2)
            elif x_pos <= 160 and self.doubling_options.get() == text2:
                x_pos = 510
                self.doubling_options.set(text1)

            x_pos -= 5
            self.after(20, self.rolling_double_options_label.place(x=x_pos, y=20))
            self.update()

    def collect_doubling_card_back_animation(self) -> None:
        """Collect the card used with doubling back to deck."""
        self.animate_dealt_card(self.third_card, (-356, -304), 10)

    def create_layout(self):
        """Create the tkinter GUI layout for the PokerGUI class."""
        self.title("Jokeri Pokeri")
        self.geometry("1024x976")

        # Canvases
        self.top_bar = tk.Canvas(
            self, bd=0, bg="snow4", height=94, width=1024, highlightthickness=0
        )
        self.middle_area = tk.Canvas(
            self, bd=0, bg="blue4", height=588, width=1024, highlightthickness=0
        )
        self.bottom_bar = tk.Canvas(
            self, bd=0, bg="snow4", height=90, width=1024, highlightthickness=0
        )
        self.button_area = tk.Canvas(
            self, bd=0, bg="gray20", height=204, width=1024, highlightthickness=0
        )

        # StringVars
        self.credits = tk.StringVar()
        self.credits.set("Credits 4.20")
        self.bet = tk.StringVar()
        self.bet.set(f"Bet {self.game.bet_levels[self.game.bet_level]:.2f}")
        self.wins = tk.StringVar()
        self.wins.set(f"Wins {self.game.winnings:.2f}")

        self.current_win = tk.StringVar()
        self.current_win.set(f"{self.game.current_win:.2f}")

        self.doubling_options = tk.StringVar()
        self.doubling_options.set("")

        self.hold_button = tk.StringVar()
        self.hold_button.set("HOLD")

        # Labels
        self.credits_label = tk.Label(
            self.top_bar, bg="navy", fg="azure", font=("Courier", 30),
            textvariable=self.credits, anchor=tk.W, padx=20
        )
        self.bet_label = tk.Label(
            self.top_bar, bg="snow4", font=("Courier", 28),
            textvariable=self.bet, anchor=tk.W, padx=20
        )
        self.wins_label = tk.Label(
            self.top_bar, bg="navy", fg="azure", font=("Courier", 30),
            textvariable=self.wins, anchor=tk.W, padx=20
        )

        self.card_back_label = tk.Label(
            self.middle_area, bg="blue4", image=self.card_back
        )
        self.card_back_label.image = self.card_back

        self.first_card_hold_label = tk.Label(
            self.bottom_bar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19)
        )
        self.second_card_hold_label = tk.Label(
            self.bottom_bar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19)
        )
        self.third_card_hold_label = tk.Label(
            self.bottom_bar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19)
        )
        self.fourth_card_hold_label = tk.Label(
            self.bottom_bar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19)
        )
        self.fifth_card_hold_label = tk.Label(
            self.bottom_bar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19)
        )
        self.double_question_label = tk.Label(
            self.bottom_bar, bg="DeepPink3", text="WANT TO DOUBLE?", font=("Courier", 26)
        )
        self.rolling_double_options_label = tk.Label(
            self.bottom_bar, fg="navy", bg="DeepPink3",
            font=("Courier", 28), textvariable=self.doubling_options
        )
        self.rolling_double_options_left_mask_label = tk.Label(
            self.bottom_bar, bg="DeepPink3"
        )
        self.rolling_double_options_righ_mask_label = tk.Label(
            self.bottom_bar, bg="DeepPink3"
        )
        self.current_win_label = tk.Label(
            self.bottom_bar, bg="navy", fg="azure", font=("Courier", 24),
            textvariable=self.current_win
        )
        self.current_bet_label = tk.Label(
            self.bottom_bar, bg="DeepPink3", text="BET ", font=("Courier", 24), anchor="e"
        )

        # Buttons
        self.first_card_hold_button = tk.Button(
            self.button_area, bg="red3", activebackground="red4", font=("Courier", 20),
            textvariable=self.hold_button, command=lambda: [self.hold(0)]
        )
        self.second_card_hold_button = tk.Button(
            self.button_area, bg="red3", activebackground="red4", font=("Courier", 20),
            textvariable=self.hold_button, command=lambda: [self.hold(1)]
        )
        self.third_card_hold_button = tk.Button(
            self.button_area, bg="red3", activebackground="red4", font=("Courier", 20),
            textvariable=self.hold_button, command=lambda: [self.hold(2)]
        )
        self.fourth_card_hold_button = tk.Button(
            self.button_area, bg="red3", activebackground="red4", font=("Courier", 20),
            textvariable=self.hold_button, command=lambda: [self.hold(3)]
        )
        self.fifth_card_hold_button = tk.Button(
            self.button_area, bg="red3", activebackground="red4", font=("Courier", 20),
            textvariable=self.hold_button, command=lambda: [self.hold(4)]
        )
        self.bet_button = tk.Button(
            self.button_area, bg="blue", activebackground="medium blue",
            font=("Courier", 20), text="BET", command=lambda: [self.change_bet()]
        )
        self.collect_button = tk.Button(
            self.button_area, bg="yellow2", activebackground="yellow3",
            font=("Courier", 20), text="COLLECT", command=lambda: [self.collect_current_win()]
        )
        self.low_button = tk.Button(
            self.button_area, bg="DarkOrange1", activebackground="DarkOrange3",
            font=("Courier", 20), text="LOW", command=lambda: [self.select_low()]
        )
        self.high_button = tk.Button(
            self.button_area, bg="DarkOrange1", activebackground="DarkOrange3",
            font=("Courier", 20), text="HIGH", command=lambda: [self.select_high()]
        )
        self.double_button = tk.Button(
            self.button_area, bg="DarkOrange1", activebackground="DarkOrange3",
            font=("Courier", 20), text="DOUBLE", command=lambda: [self.activate_doubling()]
        )
        self.deal_button = tk.Button(
            self.button_area, bg="green3", activebackground="green4",
            font=("Courier", 20), text="DEAL", command=lambda: [self.deal()]
        )

        # Canvas images
        def card_stack_images(self, canvas: tk.Canvas) -> list:
            """Create card images for card stack on given canvas."""
            card_stack_images = []
            x_point = 70
            y_point = 45

            for _ in range(8):
                card_stack_images.append(canvas.create_image(
                    x_point, y_point, anchor=tk.NW, image=self.card_back
                ))

                x_point += 2
                y_point -= 2

            return card_stack_images

        self.card_stack = card_stack_images(self, self.middle_area)

        self.card_in_transit = self.middle_area.create_image(
            84, 31, anchor=tk.NW, image=self.empty_card,
        )
        self.first_card = self.middle_area.create_image(
            70, 335, anchor=tk.NW, image=self.dealt_hand[0]
        )
        self.second_card = self.middle_area.create_image(
            255, 335, anchor=tk.NW, image=self.dealt_hand[1]
        )
        self.third_card = self.middle_area.create_image(
            440, 335, anchor=tk.NW, image=self.dealt_hand[2]
        )
        self.fourth_card = self.middle_area.create_image(
            625, 335, anchor=tk.NW, image=self.dealt_hand[3]
        )
        self.fifth_card = self.middle_area.create_image(
            810, 335, anchor=tk.NW, image=self.dealt_hand[4]
        )

        # Canvas texts
        self.winning_table_text = self.middle_area.create_text(
            530, 162, text=self.game.change_win_table(), font=("Courier", 20), fill="DarkOrange2")

        # Canvas window objects
        self.credits_window = self.top_bar.create_window(
            20, 15, anchor=tk.NW, height=65, width=380, window=self.credits_label
        )
        self.bet_window = self.top_bar.create_window(
            512, 15, anchor=tk.N, height=65, width=200, window=self.bet_label
        )
        self.wins_window = self.top_bar.create_window(
            1004, 15, anchor=tk.NE, height=65, width=340, window=self.wins_label
        )

        self.first_card_hold_label_window = self.bottom_bar.create_window(
            80, 18, anchor=tk.NW, height=55, width=120,
            window=self.first_card_hold_label, state="hidden"
        )
        self.second_card_hold_label_window = self.bottom_bar.create_window(
            265, 18, anchor=tk.NW, height=55, width=120,
            window=self.second_card_hold_label, state="hidden"
        )
        self.third_card_hold_label_window = self.bottom_bar.create_window(
            450, 18, anchor=tk.NW, height=55, width=120,
            window=self.third_card_hold_label, state="hidden"
        )
        self.fourth_card_hold_label_window = self.bottom_bar.create_window(
            635, 18, anchor=tk.NW, height=55, width=120,
            window=self.fourth_card_hold_label, state="hidden"
        )
        self.fifth_card_hold_label_window = self.bottom_bar.create_window(
            820, 18, anchor=tk.NW, height=55, width=120,
            window=self.fifth_card_hold_label, state="hidden"
        )
        self.double_question_window = self.bottom_bar.create_window(
            230, 18, anchor=tk.NW, height=60, width=340,
            window=self.double_question_label, state="hidden"
        )
        self.current_win_window = self.bottom_bar.create_window(
            600, 18, anchor=tk.NW, height=60, width=180,
            window=self.current_win_label, state="hidden"
        )
        self.active_doubling_window = self.bottom_bar.create_window(
            1, 16, anchor=tk.NW, height=60, width=270,
            window=self.current_bet_label, state="hidden"
        )
        self.rolling_double_options_window = self.bottom_bar.create_window(
            540, 20, anchor=tk.NW, height=60, width=420,
            window=self.rolling_double_options_label, state="hidden"
        )
        self.rolling_double_options_left_mask_window = self.bottom_bar.create_window(
            430, 16, anchor=tk.NW, height=60, width=75,
            window=self.rolling_double_options_left_mask_label, state="hidden"
        )
        self.rolling_double_options_right_mask_window = self.bottom_bar.create_window(
            950, 16, anchor=tk.NW, height=60, width=75,
            window=self.rolling_double_options_righ_mask_label, state="hidden"
        )

        self.first_card_hold_button_window = self.button_area.create_window(
            25, 15, anchor=tk.NW, height=80, width=145, window=self.first_card_hold_button
        )
        self.second_card_hold_button_window = self.button_area.create_window(
            192, 15, anchor=tk.NW, height=80, width=145, window=self.second_card_hold_button
        )
        self.third_card_hold_button_window = self.button_area.create_window(
            357, 15, anchor=tk.NW, height=80, width=145, window=self.third_card_hold_button
        )
        self.fourth_card_hold_button_window = self.button_area.create_window(
            522, 15, anchor=tk.NW, height=80, width=145, window=self.fourth_card_hold_button
        )
        self.fifth_card_hold_button_window = self.button_area.create_window(
            687, 15, anchor=tk.NW, height=80, width=145, window=self.fifth_card_hold_button
        )

        self.bet_button_window = self.button_area.create_window(
            852, 15, anchor=tk.NW, height=80, width=145, window=self.bet_button
        )
        self.collect_button_window = self.button_area.create_window(
            25, 110, anchor=tk.NW, height=80, width=145, window=self.collect_button
        )
        self.low_button_window = self.button_area.create_window(
            192, 110, anchor=tk.NW, height=80, width=145, window=self.low_button
        )
        self.high_button_window = self.button_area.create_window(
            357, 110, anchor=tk.NW, height=80, width=145, window=self.high_button
        )
        self.double_button_window = self.button_area.create_window(
            522, 110, anchor=tk.NW, height=80, width=145, window=self.double_button
        )
        self.deal_button_window = self.button_area.create_window(
            852, 110, anchor=tk.NW, height=80, width=145, window=self.deal_button
        )

        # Packing
        self.top_bar.pack()
        self.middle_area.pack()
        self.bottom_bar.pack()
        self.button_area.pack()


if __name__ == "__main__":
    root = PokerGUI()
    root.mainloop()
