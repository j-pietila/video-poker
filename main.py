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
        self.load_card_images()
        self.create_layout()

    def load_card_images(self):
        """Load card image files for dealt cards based on the
        dealt_cards list in the game module."""
        self.open_card_stack = Image.open("./PlayingCards/cardBack.png")
        self.open_card_stack = self.open_card_stack.resize((140, 215), Image.ANTIALIAS)
        self.card_stack = ImageTk.PhotoImage(self.open_card_stack)

        self.open_first_card = Image.open("./PlayingCards/{}.png".format(self.game.dealt_cards[0]))
        self.open_first_card = self.open_first_card.resize((140, 215), Image.ANTIALIAS)
        self.first_card = ImageTk.PhotoImage(self.open_first_card)

        self.open_second_card = Image.open("./PlayingCards/{}.png".format(self.game.dealt_cards[1]))
        self.open_second_card = self.open_second_card.resize((140, 215), Image.ANTIALIAS)
        self.second_card = ImageTk.PhotoImage(self.open_second_card)

        if self.game.is_doubling_active:
            self.open_third_card = \
                Image.open("./PlayingCards/cardBack.png")
        else:
            self.open_third_card = \
                Image.open("./PlayingCards/{}.png".format(self.game.dealt_cards[2]))
        self.open_third_card = self.open_third_card.resize((140, 215), Image.ANTIALIAS)
        self.third_card = ImageTk.PhotoImage(self.open_third_card)

        self.open_fourth_card = Image.open("./PlayingCards/{}.png".format(self.game.dealt_cards[3]))
        self.open_fourth_card = self.open_fourth_card.resize((140, 215), Image.ANTIALIAS)
        self.fourth_card = ImageTk.PhotoImage(self.open_fourth_card)

        self.open_fifth_card = Image.open("./PlayingCards/{}.png".format(self.game.dealt_cards[4]))
        self.open_fifth_card = self.open_fifth_card.resize((140, 215), Image.ANTIALIAS)
        self.fifth_card = ImageTk.PhotoImage(self.open_fifth_card)

    def update_card_labels(self):
        """Update tkinter labels for the dealt cards."""
        self.first_card_label.configure(image=self.first_card)
        self.second_card_label.configure(image=self.second_card)
        self.third_card_label.configure(image=self.third_card)
        self.fourth_card_label.configure(image=self.fourth_card)
        self.fifth_card_label.configure(image=self.fifth_card)

    def update_drawn_cards(self):
        """Load new card images and update GUI labels with them."""
        self.load_card_images()
        self.update_card_labels()

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
            self.update_drawn_cards()

            self.bottom_bar.configure(bg="DeepPink3")
            self.bottom_bar.coords(self.current_win_window, 600, 18)
            self.current_win.set("{:.2f}".format(self.game.current_win))
            self.bottom_bar.itemconfigure(self.current_win_window, state="normal")
            self.bottom_bar.itemconfigure(self.double_question_window, state="normal")
            self.bottom_bar.itemconfigure(self.active_doubling_window, state="hidden")

    def no_win_view(self):
        """Update GUI to show losing hand view."""
        self.update_drawn_cards()

        self.bottom_bar.configure(bg="snow4")
        self.bottom_bar.coords(self.current_win_window, 600, 18)
        self.current_win.set("{:.2f}".format(self.game.current_win))
        self.bottom_bar.itemconfigure(self.current_win_window, state="hidden")
        self.bottom_bar.itemconfigure(self.double_question_window, state="hidden")
        self.bottom_bar.itemconfigure(self.active_doubling_window, state="hidden")

    def active_doubling_view(self):
        """Update GUI to show active doubling view."""
        self.update_drawn_cards()

        self.bottom_bar.coords(self.current_win_window, 270, 18)
        self.current_win.set("{:.2f}".format(self.game.current_win))
        self.bottom_bar.itemconfigure(self.double_question_window, state="hidden")
        self.bottom_bar.itemconfigure(self.active_doubling_window, state="normal")

    def after_doubling_view(self, double_win):
        """Update GUI to show either win or no win view after
        doubling based on the double_win result."""
        self.update_drawn_cards()

        if double_win:
            self.winning_hand_view()
        else:
            self.no_win_view()

    def change_bet(self):
        """Event handler for bet button. Run change bet function
        from game module and update GUI accordingly."""
        self.game.change_bet()

        self.bet.set("Bet {:.2f}".format(self.game.bet_levels[self.game.bet_level]))
        self.winning_table.set(self.game.change_win_table())

    def deal(self):
        """Event handler for deal button. Run deal function from game
        module and update GUI elements for changed cards and possible
        winning hand view."""
        if self.game.current_win == 0:
            self.game.deal()
            self.clear_hold_labels()

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

    def select_low(self):
        """Event handler for low button. Run doubling result check
        from game module with low card range selection and update
        GUI according to doubling result."""
        if self.game.is_doubling_active:
            double_choice = ["A", "2", "3", "4", "5", "6"]

            double_win = self.game.check_doubling_result(double_choice)

            self.after_doubling_view(double_win)

            #self.update_drawn_cards()

            #if double_win:
            #    self.winning_hand_view()
            #else:
            #    self.no_win_view()

    def select_high(self):
        """Event handler for high button. Run doubling result check
        from game module with high card range selection and update
        GUI according to doubling result."""
        if self.game.is_doubling_active:
            double_choice = ["8", "9", "10", "J", "Q", "K"]

            double_win = self.game.check_doubling_result(double_choice)

            self.after_doubling_view(double_win)

            #self.update_drawn_cards()

            #if double_win:
            #    self.winning_hand_view()
            #else:
            #    self.no_win_view()

    def collect_current_win(self):
        """Event handler for collect button. Collect current win with
        a GUI counting sequence animation and set GUI to base state."""
        win_update = self.game.current_win
        decrement = win_update / 8

        self.game.collect_current_win()

        for i in range(7, -1, -1):
            win_update -= decrement
            self.after(250, self.transfer_animation_step(i, win_update, decrement))

        self.no_win_view()

    def transfer_animation_step(self, i, win_update, decrement):
        """Update the GUI elements for current win
        transfer animation step and update the view."""
        self.wins.set("Wins {:.2f}".format(self.game.winnings - (i * decrement)))
        # Occasional final result is -0.00, hence abs().
        self.current_win.set("{:.2f}".format(abs(win_update)))
        self.update()

    def create_layout(self):
        """Create the tkinter GUI layout for the PokerGUI class."""
        self.title("Jokeri Pokeri")
        self.geometry("1024x976")

        # Canvases
        self.top_bar = tk.Canvas(self, bd=0, bg="snow4", height=90, width=1024)
        self.middle_area = tk.Canvas(self, bd=0, bg="blue4", height=588, width=1024)
        self.bottom_bar = tk.Canvas(self, bd=0, bg="snow4", height=90, width=1024)
        self.button_area = tk.Canvas(self, bd=0, bg="gray20", height=200, width=1024)

        # StringVars
        self.credits = tk.StringVar()
        self.credits.set("Credits 4.20")
        self.bet = tk.StringVar()
        self.bet.set("Bet {:.2f}".format(self.game.bet_levels[self.game.bet_level]))
        self.wins = tk.StringVar()
        self.wins.set("Wins {:.2f}".format(self.game.winnings))

        self.winning_table = tk.StringVar()
        self.winning_table.set(self.game.change_win_table())

        self.current_win = tk.StringVar()
        self.current_win.set("{:.2f}".format(self.game.current_win))

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

        self.winning_table_label = tk.Label(
            self.middle_area, bg="blue4", fg="DarkOrange2",
            font=("Courier", 19), textvariable=self.winning_table
        )
        self.card_stack_label = tk.Label(
            self.middle_area, bg="blue4", image=self.card_stack
        )
        self.card_stack_label.image = self.card_stack

        self.first_card_label = tk.Label(
            self.middle_area, bg="blue4", image=self.first_card
        )
        self.second_card_label = tk.Label(
            self.middle_area, bg="blue4", image=self.second_card
        )
        self.third_card_label = tk.Label(
            self.middle_area, bg="blue4", image=self.third_card
        )
        self.fourth_card_label = tk.Label(
            self.middle_area, bg="blue4", image=self.fourth_card
        )
        self.fifth_card_label = tk.Label(
            self.middle_area, bg="blue4", image=self.fifth_card
        )

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
        self.current_win_label = tk.Label(
            self.bottom_bar, bg="navy", fg="azure", font=("Courier", 24),
            textvariable=self.current_win
        )
        self.current_bet_label = tk.Label(
            self.bottom_bar, bg="DeepPink3", text="BET", font=("Courier", 24)
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

        self.winning_table_window = self.middle_area.create_window(
            960, 40, anchor=tk.NE, height=235, width=800, window=self.winning_table_label
        )
        self.card_stack_window = self.middle_area.create_window(
            70, 45, anchor=tk.NW, window=self.card_stack_label
        )
        self.first_card_window = self.middle_area.create_window(
            70, 550, anchor=tk.SW, window=self.first_card_label
        )
        self.second_card_window = self.middle_area.create_window(
            255, 550, anchor=tk.SW, window=self.second_card_label
        )
        self.third_card_window = self.middle_area.create_window(
            440, 550, anchor=tk.SW, window=self.third_card_label
        )
        self.fourth_card_window = self.middle_area.create_window(
            625, 550, anchor=tk.SW, window=self.fourth_card_label
        )
        self.fifth_card_window = self.middle_area.create_window(
            810, 550, anchor=tk.SW, window=self.fifth_card_label
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
            180, 18, anchor=tk.NW, height=60, width=80,
            window=self.current_bet_label, state="hidden"
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
