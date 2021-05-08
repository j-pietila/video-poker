"""
Video Poker - Legendary Finnish Jokeri Pokeri by RAY
main.py: Main program file for Video Poker
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
        self.wins.set("Wins 0.00")

        self.winningTable = tk.StringVar()
        self.winningTable.set(self.game.changeWinTable())

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

        # Buttons
        self.firstCardButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.selectCard()])
        self.secondCardButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.selectCard()])
        self.thirdCardButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.selectCard()])
        self.fourthCardButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.selectCard()])
        self.fifthCardButton = tk.Button(self.buttonArea, bg="red3", activebackground="red4", textvariable=self.holdButton, font=("Courier", 20), command=lambda: [self.selectCard()])
        self.betButton = tk.Button(self.buttonArea, bg="blue", activebackground="medium blue", text="BET", font=("Courier", 20), command=lambda: [self.game.changeBet(), self.bet.set("Bet {:.2f}".format(self.game.betLevels[self.game.betLevel])), self.winningTable.set(self.game.changeWinTable())])
        self.collectButton = tk.Button(self.buttonArea, bg="yellow2", activebackground="yellow3", text="COLLECT", font=("Courier", 20), command=lambda: [self.collectWinnings()])
        self.lowButton = tk.Button(self.buttonArea, bg="DarkOrange1", activebackground="DarkOrange3", text="LOW", font=("Courier", 20), command=lambda: [self.selectLow()])
        self.highButton = tk.Button(self.buttonArea, bg="DarkOrange1", activebackground="DarkOrange3", text="HIGH", font=("Courier", 20), command=lambda: [self.selectHigh()])
        self.doubleButton = tk.Button(self.buttonArea, bg="DarkOrange1", activebackground="DarkOrange3", text="DOUBLE", font=("Courier", 20), command=lambda: [self.double()])
        self.dealButton = tk.Button(self.buttonArea, bg="green3", activebackground="green4", text="DEAL", font=("Courier", 20), command=lambda: [self.game.deal(), self.loadCardImages(), self.updateCardLabels()])

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

        self.firstCardHoldLabelWindow = self.bottomBar.create_window(80, 18, anchor=tk.NW, height=55, width=120, window=self.firstCardHoldLabel)
        self.secondCardHoldLabelWindow = self.bottomBar.create_window(265, 18, anchor=tk.NW, height=55, width=120, window=self.secondCardHoldLabel)
        self.thirdCardHoldLabelWindow = self.bottomBar.create_window(450, 18, anchor=tk.NW, height=55, width=120, window=self.thirdCardHoldLabel)
        self.fourthCardHoldLabelWindow = self.bottomBar.create_window(635, 18, anchor=tk.NW, height=55, width=120, window=self.fourthCardHoldLabel)
        self.fifthCardHoldLabelWindow = self.bottomBar.create_window(820, 18, anchor=tk.NW, height=55, width=120, window=self.fifthCardHoldLabel)

        self.firstCardButtonWindow = self.buttonArea.create_window(25, 15, anchor=tk.NW, height=80, width=145, window=self.firstCardButton)
        self.secondCardButtonWindow = self.buttonArea.create_window(192, 15, anchor=tk.NW, height=80, width=145, window=self.secondCardButton)
        self.thirdCardButtonWindow = self.buttonArea.create_window(357, 15, anchor=tk.NW, height=80, width=145, window=self.thirdCardButton)
        self.fourthCardButtonWindow = self.buttonArea.create_window(522, 15, anchor=tk.NW, height=80, width=145, window=self.fourthCardButton)
        self.fifthCardButtonWindow = self.buttonArea.create_window(687, 15, anchor=tk.NW, height=80, width=145, window=self.fifthCardButton)

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
