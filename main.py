"""
Video Poker - Legendary Finnish Jokeri Pokeri by RAY
main.py: Main program file for Video Poker containing the tkinter GUI class
@author: Joonas Pietilä
"""

import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

from game import PokerGame

class PokerGUI(tk.Tk):
    """Tkinter GUI class for Video Poker"""

    def __init__(self):
        super().__init__()
        self.game = PokerGame()
        self.loadCardImages()
        self.createLayout()

    def loadCardImages(self):
        self.openCardStack = Image.open("./PlayingCards/cardBack.png")
        self.openCardStack = self.openCardStack.resize((140, 215), Image.ANTIALIAS)
        self.cardStack = ImageTk.PhotoImage(self.openCardStack)

        self.openFirstCard = Image.open("./PlayingCards/{}.png".format(self.game.dealtCards[0]))
        self.openFirstCard = self.openFirstCard.resize((140, 215), Image.ANTIALIAS)
        self.firstCard = ImageTk.PhotoImage(self.openFirstCard)

        self.openSecondCard = Image.open("./PlayingCards/{}.png".format(self.game.dealtCards[1]))
        self.openSecondCard = self.openSecondCard.resize((140, 215), Image.ANTIALIAS)
        self.secondCard = ImageTk.PhotoImage(self.openSecondCard)

        if self.game.doublingActive:
            self.openThirdCard = Image.open("./PlayingCards/cardBack.png")
        else:
            self.openThirdCard = Image.open("./PlayingCards/{}.png".format(self.game.dealtCards[2]))
        self.openThirdCard = self.openThirdCard.resize((140, 215), Image.ANTIALIAS)
        self.thirdCard = ImageTk.PhotoImage(self.openThirdCard)

        self.openFourthCard = Image.open("./PlayingCards/{}.png".format(self.game.dealtCards[3]))
        self.openFourthCard = self.openFourthCard.resize((140, 215), Image.ANTIALIAS)
        self.fourthCard = ImageTk.PhotoImage(self.openFourthCard)

        self.openFifthCard = Image.open("./PlayingCards/{}.png".format(self.game.dealtCards[4]))
        self.openFifthCard = self.openFifthCard.resize((140, 215), Image.ANTIALIAS)
        self.fifthCard = ImageTk.PhotoImage(self.openFifthCard)

    def updateCardLabels(self):
        self.firstCardLabel.configure(image=self.firstCard)
        self.secondCardLabel.configure(image=self.secondCard)
        self.thirdCardLabel.configure(image=self.thirdCard)
        self.fourthCardLabel.configure(image=self.fourthCard)
        self.fifthCardLabel.configure(image=self.fifthCard)

    def updateHoldLabels(self, index):
        self.holdLabels = {
            0: self.firstCardHoldLabelWindow,
            1: self.secondCardHoldLabelWindow,
            2: self.thirdCardHoldLabelWindow,
            3: self.fourthCardHoldLabelWindow,
            4: self.fifthCardHoldLabelWindow
        }

        if self.game.holdCards[index] == 0:
            self.bottomBar.itemconfigure(self.holdLabels.get(index), state="hidden")
        else:
            self.bottomBar.itemconfigure(self.holdLabels.get(index), state="normal")

    def clearHoldLabels(self):
        self.bottomBar.itemconfigure(self.firstCardHoldLabelWindow, state="hidden")
        self.bottomBar.itemconfigure(self.secondCardHoldLabelWindow, state="hidden")
        self.bottomBar.itemconfigure(self.thirdCardHoldLabelWindow, state="hidden")
        self.bottomBar.itemconfigure(self.fourthCardHoldLabelWindow, state="hidden")
        self.bottomBar.itemconfigure(self.fifthCardHoldLabelWindow, state="hidden")

    def updateCurrentWin(self):
        if self.game.currentWin > 0:
            self.currentWin.set("{:.2f}".format(self.game.currentWin))
            self.bottomBar.configure(bg="DeepPink3")
            self.bottomBar.itemconfigure(self.doubleQuestionWindow, state="normal")
            self.bottomBar.itemconfigure(self.currentWinWindow, state="normal")

    def collectWinnings(self):
        self.decrement = self.game.currentWin / 8
        self.currentWinUpdate = self.game.currentWin

        self.game.collectWin()

        for i in range(7, -1, -1):
            self.after(250, self.transferWinnings(i))

        self.bottomBar.configure(bg="snow4")
        self.bottomBar.itemconfigure(self.doubleQuestionWindow, state="hidden")
        self.bottomBar.itemconfigure(self.currentWinWindow, state="hidden")

    def transferWinnings(self, i):
        self.currentWinUpdate -= self.decrement
        self.wins.set("Wins {:.2f}".format(self.game.winnings - (i * self.decrement)))
        self.currentWin.set("{:.2f}".format(abs(self.currentWinUpdate))) # Results occasionally in -0.00, hence abs()
        self.update()

    def deal(self):
        """Event handler for deal button. Check that dealing
        is allowed in current game situation."""
        if self.game.currentWin == 0:
            self.game.deal()

            self.loadCardImages()
            self.updateCardLabels()
            self.clearHoldLabels()

            self.updateCurrentWin()

    def activateDoubling(self):
        """Event handler for double button. Update GUI elements to active
        doubling view and run doubling function from game module."""
        if self.game.isInitialDeal == True and self.game.currentWin > 0:
            self.game.double()
            self.loadCardImages()
            self.updateCardLabels() # make another function to draw only one card for the doubling scenario
            self.bottomBar.itemconfigure(self.doubleQuestionWindow, state="hidden")
            self.bottomBar.itemconfigure(self.activeDoublingWindow, state="normal") # add the rolling doubling options
            self.bottomBar.coords(self.currentWinWindow, 270, 18)
            self.currentWin.set("{:.2f}".format(self.game.currentWin))

    def selectLow(self):
        """Run doubling result check from game module with low card range
        selection and update GUI according to doubling result."""
        if self.game.doublingActive:
            doubleChoice = ["A", "2", "3", "4", "5", "6"]

            doubleWin = self.game.checkDoubling(doubleChoice)

            self.loadCardImages()
            self.updateCardLabels()
            
            if doubleWin:
                self.bottomBar.coords(self.currentWinWindow, 600, 18)
                self.bottomBar.itemconfigure(self.activeDoublingWindow, state="hidden")
                self.updateCurrentWin()
            else:
                self.bottomBar.configure(bg="snow4")
                self.bottomBar.itemconfigure(self.activeDoublingWindow, state="hidden") # add the rolling doubling options
                self.bottomBar.coords(self.currentWinWindow, 600, 18)
                self.bottomBar.itemconfigure(self.currentWinWindow, state="hidden")
                self.currentWin.set("{:.2f}".format(self.game.currentWin))

    def selectHigh(self):
        """Run doubling result check from game module with high card range
        selection and update GUI according to doubling result."""
        if self.game.doublingActive:
            doubleChoice = ["8", "9", "10", "J", "Q", "K"]

            doubleWin = self.game.checkDoubling(doubleChoice)

            self.loadCardImages()
            self.updateCardLabels()
            
            if doubleWin:
                self.bottomBar.coords(self.currentWinWindow, 600, 18)
                self.bottomBar.itemconfigure(self.activeDoublingWindow, state="hidden")
                self.updateCurrentWin()
            else:
                self.bottomBar.configure(bg="snow4")
                self.bottomBar.itemconfigure(self.activeDoublingWindow, state="hidden") # add the rolling doubling options to this
                self.bottomBar.coords(self.currentWinWindow, 600, 18)
                self.bottomBar.itemconfigure(self.currentWinWindow, state="hidden")
                self.currentWin.set("{:.2f}".format(self.game.currentWin))

    def createLayout(self):
        self.title("Jokeri Pokeri")
        self.geometry("1024x976")

        # Canvases
        self.topBar = tk.Canvas(self, bd=0, bg="snow4", height=90, width=1024)
        self.middleArea = tk.Canvas(self, bd=0, bg="blue4", height=588, width=1024) 
        self.bottomBar = tk.Canvas(self, bd=0, bg="snow4", height=90, width=1024)
        self.buttonArea = tk.Canvas(self, bd=0, bg="gray20", height=200, width=1024)

        # StringVars
        self.credits = tk.StringVar()
        self.credits.set("Credits 4.20")
        self.bet = tk.StringVar()
        self.bet.set("Bet {:.2f}".format(self.game.betLevels[self.game.betLevel]))
        self.wins = tk.StringVar()
        self.wins.set("Wins {:.2f}".format(self.game.winnings))

        self.winningTable = tk.StringVar()
        self.winningTable.set(self.game.changeWinTable())

        self.currentWin = tk.StringVar()
        self.currentWin.set("{:.2f}".format(self.game.currentWin))

        self.holdButton = tk.StringVar()
        self.holdButton.set("HOLD")

        # Labels
        self.creditsLabel = tk.Label(self.topBar, bg="navy", fg="azure", textvariable=self.credits, font=("Courier", 30), anchor=tk.W, padx=20)
        self.betLabel = tk.Label(self.topBar, bg="snow4", font=("Courier", 28), textvariable=self.bet, anchor=tk.W, padx=20)
        self.winsLabel = tk.Label(self.topBar, bg="navy", fg="azure", textvariable=self.wins, font=("Courier", 30), anchor=tk.W, padx=20)
        
        self.winningTableLabel = tk.Label(self.middleArea, bg="blue4", fg="DarkOrange2", textvariable=self.winningTable, font=("Courier", 19))
        self.cardStackLabel = tk.Label(self.middleArea, bg="blue4", image=self.cardStack)
        self.cardStackLabel.image = self.cardStack

        self.firstCardLabel = tk.Label(self.middleArea, bg="blue4", image=self.firstCard)
        self.secondCardLabel = tk.Label(self.middleArea, bg="blue4", image=self.secondCard)
        self.thirdCardLabel = tk.Label(self.middleArea, bg="blue4", image=self.thirdCard)
        self.fourthCardLabel = tk.Label(self.middleArea, bg="blue4", image=self.fourthCard)
        self.fifthCardLabel = tk.Label(self.middleArea, bg="blue4", image=self.fifthCard)

        self.firstCardHoldLabel = tk.Label(self.bottomBar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19))
        self.secondCardHoldLabel = tk.Label(self.bottomBar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19))
        self.thirdCardHoldLabel = tk.Label(self.bottomBar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19))
        self.fourthCardHoldLabel = tk.Label(self.bottomBar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19))
        self.fifthCardHoldLabel = tk.Label(self.bottomBar, bg="cyan2", fg="navy", text="hold", font=("Courier", 19))
        self.doubleQuestionLabel = tk.Label(self.bottomBar, bg="DeepPink3", text="WANT TO DOUBLE?", font=("Courier", 26))
        self.currentWinLabel = tk.Label(self.bottomBar, bg="navy", fg="azure", textvariable=self.currentWin, font=("Courier", 24))
        self.currentBetLabel = tk.Label(self.bottomBar, bg="DeepPink3", text="BET", font=("Courier", 24))

        # Buttons
        self.firstCardHoldButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.game.hold(0), self.updateHoldLabels(0)])
        self.secondCardHoldButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.game.hold(1), self.updateHoldLabels(1)])
        self.thirdCardHoldButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.game.hold(2), self.updateHoldLabels(2)])
        self.fourthCardHoldButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.game.hold(3), self.updateHoldLabels(3)])
        self.fifthCardHoldButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.game.hold(4), self.updateHoldLabels(4)])
        self.betButton = tk.Button(self.buttonArea, bg="blue", activebackground="medium blue", text="BET", font=("Courier", 20), command=lambda: [self.game.changeBet(), self.bet.set("Bet {:.2f}".format(self.game.betLevels[self.game.betLevel])), self.winningTable.set(self.game.changeWinTable())])
        self.collectButton = tk.Button(self.buttonArea, bg="yellow2", activebackground="yellow3", text="COLLECT", font=("Courier", 20), command=lambda: [self.collectWinnings()])
        self.lowButton = tk.Button(self.buttonArea, bg="DarkOrange1", activebackground="DarkOrange3", text="LOW", font=("Courier", 20), command=lambda: [self.selectLow()])
        self.highButton = tk.Button(self.buttonArea, bg="DarkOrange1", activebackground="DarkOrange3", text="HIGH", font=("Courier", 20), command=lambda: [self.selectHigh()])
        self.doubleButton = tk.Button(self.buttonArea, bg="DarkOrange1", activebackground="DarkOrange3", text="DOUBLE", font=("Courier", 20), command=lambda: [self.activateDoubling()])
        self.dealButton = tk.Button(self.buttonArea, bg="green3", activebackground="green4", text="DEAL", font=("Courier", 20), command=lambda: [self.deal()])

        # Canvas window objects
        self.creditsWindow = self.topBar.create_window(20, 15, anchor=tk.NW, height=65, width=380, window=self.creditsLabel)
        self.betWindow = self.topBar.create_window(512, 15, anchor=tk.N, height=65, width=200, window=self.betLabel)
        self.winsWindow = self.topBar.create_window(1004, 15, anchor=tk.NE, height=65, width=340, window=self.winsLabel)
        
        self.winningTableWindow= self.middleArea.create_window(960, 40, anchor=tk.NE, height=235, width=800, window=self.winningTableLabel)
        self.cardStackWindow = self.middleArea.create_window(70, 45, anchor=tk.NW, window=self.cardStackLabel)
        self.firstCardWindow = self.middleArea.create_window(70, 550, anchor=tk.SW, window=self.firstCardLabel)
        self.secondCardWindow = self.middleArea.create_window(255, 550, anchor=tk.SW, window=self.secondCardLabel)
        self.thirdCardWindow = self.middleArea.create_window(440, 550, anchor=tk.SW, window=self.thirdCardLabel)
        self.fourthCardWindow = self.middleArea.create_window(625, 550, anchor=tk.SW, window=self.fourthCardLabel)
        self.fifthCardWindow = self.middleArea.create_window(810, 550, anchor=tk.SW, window=self.fifthCardLabel)

        self.firstCardHoldLabelWindow = self.bottomBar.create_window(80, 18, anchor=tk.NW, height=55, width=120, window=self.firstCardHoldLabel, state="hidden")
        self.secondCardHoldLabelWindow = self.bottomBar.create_window(265, 18, anchor=tk.NW, height=55, width=120, window=self.secondCardHoldLabel, state="hidden")
        self.thirdCardHoldLabelWindow = self.bottomBar.create_window(450, 18, anchor=tk.NW, height=55, width=120, window=self.thirdCardHoldLabel, state="hidden")
        self.fourthCardHoldLabelWindow = self.bottomBar.create_window(635, 18, anchor=tk.NW, height=55, width=120, window=self.fourthCardHoldLabel, state="hidden")
        self.fifthCardHoldLabelWindow = self.bottomBar.create_window(820, 18, anchor=tk.NW, height=55, width=120, window=self.fifthCardHoldLabel, state="hidden")
        self.doubleQuestionWindow = self.bottomBar.create_window(230, 18, anchor=tk.NW, height=60, width=340, window=self.doubleQuestionLabel, state="hidden")
        self.currentWinWindow = self.bottomBar.create_window(600, 18, anchor=tk.NW, height=60, width=180, window=self.currentWinLabel, state="hidden")
        self.activeDoublingWindow = self.bottomBar.create_window(180, 18, anchor=tk.NW, height=60, width=80, window=self.currentBetLabel, state="hidden")

        self.firstCardHoldButtonWindow = self.buttonArea.create_window(25, 15, anchor=tk.NW, height=80, width=145, window=self.firstCardHoldButton)
        self.secondCardHoldButtonWindow = self.buttonArea.create_window(192, 15, anchor=tk.NW, height=80, width=145, window=self.secondCardHoldButton)
        self.thirdCardHoldButtonWindow = self.buttonArea.create_window(357, 15, anchor=tk.NW, height=80, width=145, window=self.thirdCardHoldButton)
        self.fourthCardHoldButtonWindow = self.buttonArea.create_window(522, 15, anchor=tk.NW, height=80, width=145, window=self.fourthCardHoldButton)
        self.fifthCardHoldButtonWindow = self.buttonArea.create_window(687, 15, anchor=tk.NW, height=80, width=145, window=self.fifthCardHoldButton)

        self.betButtonWindow = self.buttonArea.create_window(852, 15, anchor=tk.NW, height=80, width=145, window=self.betButton)
        self.collectButtonWindow = self.buttonArea.create_window(25, 110, anchor=tk.NW, height=80, width=145, window=self.collectButton)
        self.lowButtonWindow = self.buttonArea.create_window(192, 110, anchor=tk.NW, height=80, width=145, window=self.lowButton)
        self.highButtonWindow = self.buttonArea.create_window(357, 110, anchor=tk.NW, height=80, width=145, window=self.highButton)
        self.doubleButtonWindow = self.buttonArea.create_window(522, 110, anchor=tk.NW, height=80, width=145, window=self.doubleButton)
        self.dealButtonWindow = self.buttonArea.create_window(852, 110, anchor=tk.NW, height=80, width=145, window=self.dealButton)

        # Packing
        self.topBar.pack()
        self.middleArea.pack()
        self.bottomBar.pack()
        self.buttonArea.pack()


if __name__ == "__main__":
    root = PokerGUI()
    root.mainloop()
