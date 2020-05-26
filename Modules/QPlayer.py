import numpy as np
from Players import Player


class QPlayer(Player):
    # https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56
    # https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/
    def __init__(self, stack=10_000, count=0, eps=0.2, alpha=0.1, gamma=0.9, load=False, update=True):
        Player.__init__(self, name='Q', stack=stack, count=count)
        self.eps = eps  # percentage of exploration
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor, typically 0.8-0.99
        self.actions = [0, 1]  # 0: Stand, 1: Hit
        self.offset = 3
        self.load = load
        self.update = update
        if self.load:
            self.Q = np.load(self.load)
        else:
            self.Q = np.zeros((10, 20, 2))

    def ExploreOrExploit(self):
        d, t = self.GetState()
        if np.random.uniform(0., 1.) < self.eps:
            return np.random.choice(self.actions)
        else:
            return np.argmax(self.Q[d, t])

    def GetState(self):
        total = self.GetTotal()
        if total > 21:
            total = 22
        return self.dealer - 1, total - self.offset

    def Update(self, reward, action, new_state):
        d, s = self.d, self.s
        a, ns = action, new_state
        self.Q[d, s, a] = (1 - self.alpha) * self.Q[d, s, a] + \
            self.alpha * (reward + self.gamma * np.max(self.Q[d, ns, :]))

    def TakeAction(self, dealer):
        if self.GetTotal() > 21:
            return self.actions[0]
        self.dealer = dealer
        self.d, self.s = self.GetState()
        return self.ExploreOrExploit()

    def ActionResponse(self, action, win=None):
        if not self.update:
            return
        if action == 0:
            new_state = self.s
            if win >= 0:
                reward = 20.
            else:
                reward = -10.
        else:
            _, new_state = self.GetState()
            total = new_state + self.offset
            if total == 22:
                reward = -20.
            else:
                reward = 10.
        self.Update(reward, action, new_state)

    def Save(self, name='qtables/qtable.npy'):
        np.save(name, self.Q)
