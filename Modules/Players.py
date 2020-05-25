import numpy as np
from Counter import Counter


class Player(Counter):
    def __init__(self, name='BasicPlayer', stack=100_000, count=0):
        Counter.__init__(self, count=count)
        self.name = name
        self.cards = []
        self.stack = stack
        self.bet = 0

    def SetBet(self, ncards=52):
        self.bet = 100

    def TakeAction(self, card=None):
        # https://bicyclecards.com/how-to-play/blackjack/
        total = self.GetTotal()
        if total >= 17:
            return 0
        if card in [1, 7, 8, 9, 10]:
            return 1
        elif card in [4, 5, 6]:
            return 1 if total < 12 else 0
        else:
            return 1 if total < 13 else 0

    def GetBet(self):
        return self.bet

    def ResetCards(self):
        self.cards = []

    def AddCard(self, card):
        self.cards.append(card)

    def GetTotal(self):
        return np.sum(self.cards) if 1 not in self.cards else self.TotalAce()

    def GetLoc(self):
        for i, icard in enumerate(self.cards):
            if icard == 1:
                return i

    def TotalAce(self):
        total = np.sum(self.cards)
        if total > 20:
            return total
        cardsA = [i for i in self.cards]
        cardsA[self.GetLoc()] = 11
        totalA = np.sum(cardsA)
        if totalA > 21:
            return total
        return totalA

    def Bust(self):
        return 1 if self.GetTotal() > 21 else 0

    def Win(self, dealer):
        if self.Bust():
            return -1
        if dealer.Bust():
            return 1
        if self.GetTotal() > dealer.GetTotal():
            return 1
        elif self.GetTotal() < dealer.GetTotal():
            return -1
        else:
            return 0

    def BlackJack(self):
        if self.GetTotal() == 21 and len(self.cards) == 2:
            return 1
        return 0


class Dealer(Player):
    def __init__(self):
        self.name = 'Dealer'

    def TakeAction(self, _=None):
        total = self.GetTotal()
        if total < 17:
            return 1
        elif total > 17:
            return 0
        else:
            return 1 if 1 in self.cards else 0  # soft vs hard 17


class BadPlayer(Player):
    def __init__(self, stack=10_000, count=0):
        Player.__init__(self, name='Bad', stack=stack, count=count)

    def TakeAction(self, card):
        return 0 if self.GetTotal() >= 17 else 1


class OKPlayer(Player):
    def __init__(self):
        self.name = 'OK'

    def SetBet(self, ncards):
        tcount = self.GetTrueCount(ncards)
        if tcount > 5:
            self.bet = 50
        elif tcount < -5:
            self.bet = 200
        else:
            self.bet = 100

    def TakeAction(self, _=None):
        total = self.GetTotal()
        if total < 17:
            return 1
        elif total > 17:
            return 0
        else:  # soft vs hard 17
            return 1 if 1 in self.cards else 0


class ChartPlayer(Player):
    # https://www.blackjackapprenticeship.com/blackjack-strategy-charts/
    def __init__(self, stack=10_000, count=0):
        Player.__init__(self, name='Chart', stack=stack, count=count)

    def SoftTotals(self, card):
        #    A, 2, 3, 4, 5, 6, 7, 8, 9, 10
        Decisions = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # A,A
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # A,2
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # A,3
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # A,4
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # A,5
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # A,6
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # A,7
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A,8
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A,9
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # A,10
        ])
        row = self.cards[0] if self.cards[1] == 1 else self.cards[1]
        row = row - 1
        col = card - 1
        return Decisions[row, col]

    def HardTotals(self, card):
        #    A, 2, 3, 4, 5, 6, 7, 8, 9, 10
        Decisions = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 0
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 2
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 3
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 4
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 5
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 6
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 7
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 8
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 9
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 10
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 11
            [1, 1, 1, 0, 0, 0, 1, 1, 1, 1],  # 12
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # 13
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # 14
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # 15
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],  # 16
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 17
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 18
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 19
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 20
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # 21
        ])
        row = self.GetTotal()
        col = card - 1
        return Decisions[row, col]

    def TakeAction(self, card):
        if len(self.cards) > 2:
            return Player.TakeAction(self, card)
        if 1 in self.cards:
            return self.SoftTotals(card)
        return self.HardTotals(card)
