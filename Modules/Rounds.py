import numpy as np
import Players


class Round:
    def __init__(self, deck, Nplayers=1, players=None, stacks=None, counts=None):
        self.deck = deck
        self.ncards = len(self.deck)
        self.Nplayers = Nplayers
        self.players = players
        if not players:
            self.players = self.InitializePlayers(stacks, counts)
        self.nplayers = self.players
        self.dealer = Players.Dealer()

    def InitializePlayers(self, stacks, counts):
        if not stacks:
            stacks = [1000] * self.Nplayers
        if not counts:
            counts = [0] * self.Nplayers
        players = []
        for i, (stack, count) in enumerate(zip(stacks, counts)):
            players.append(Players.Player(f'Player{i}', stack, count=count))
        return players

    def SetNPlayers(self, nplayers=1):
        self.nplayers = self.players[:nplayers]

    def GetPlayers(self):
        return self.players

    def GetDealer(self):
        return self.dealer

    def GetDeck(self):
        return self.deck

    def SetDeck(self, deck):
        self.deck = deck

    def MakeBets(self):
        for player in self.nplayers:
            player.SetBet(len(self.GetDeck()))

    def GiveCard(self):
        ncards = len(self.deck)
        icard = np.random.randint(ncards)
        card = self.deck[icard]
        mask = [True if i != icard else False for i in range(ncards)]
        self.deck = self.deck[mask]
        return card

    def SetUp(self):
        # deal players:
        for player in self.nplayers:
            player.ResetCards()
            player.AddCard(self.GiveCard())
            player.AddCard(self.GiveCard())
        # deal Dealer:
        self.dealer.ResetCards()
        self.dealer.AddCard(self.GiveCard())
        self.dealer.AddCard(self.GiveCard())

    def TakeActions(self):
        dealer_card = self.dealer.cards[0]
        for player in self.nplayers:
            player.CountTable(self.nplayers, dealer_card)
            action = player.TakeAction(dealer_card)
            while action:
                card = self.GiveCard()
                player.AddCard(card)
                player.CountCard(card)
                action = player.TakeAction(dealer_card)
        while self.dealer.TakeAction():
            card = self.GiveCard()
            self.dealer.AddCard(card)

    def PayOuts(self):
        for player in self.nplayers:
            player.CountCards(self.dealer.cards[1:])
            if player.BlackJack() and not self.dealer.BlackJack():
                player.stack += 1.5 * player.GetBet()
                continue
            if player.Win(self.dealer) > 0:
                player.stack += player.GetBet()
            elif player.Win(self.dealer) < 0:
                player.stack -= player.GetBet()
