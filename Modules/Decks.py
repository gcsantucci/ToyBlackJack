import numpy as np


def MakeDeck():
    values = [i if i < 11 else 10 for i in range(1, 14)]
    suites = ['H', 'S', 'C', 'D']
    # return np.array([(ivalue, inaipe) for inaipe in naipes for ivalue in values])
    return np.array([value for i, _ in enumerate(suites) for value in values])


def MakeDecks(ndecks=1):
    deck = np.array([MakeDeck() for i in range(ndecks)]).flatten()
    np.random.shuffle(deck)
    return deck
