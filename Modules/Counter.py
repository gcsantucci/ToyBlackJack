import numpy as np

class Counter:
    # https://www.blackjackapprenticeship.com/how-to-count-cards/ 
    def __init__(self, count=0):
        self.count = count

    def ResetCount(self):
        self.count = 0

    def GetCount(self):
        return self.count

    def GetTrueCount(self, ncards):
        ndecks = np.ceil(ncards / 52)
        return self.count / ndecks

    def CountCard(self, card):
        if card > 1 and card < 7:
            self.count += 1
        elif card == 1 or card == 10:
            self.count -= 1

    def CountCards(self, cards):
        for card in cards:
            self.CountCard(card)

    def CountTable(self, players, dealer_card):
        for player in players:
            self.CountCards(player.cards)
        self.CountCard(dealer_card)
