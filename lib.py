# Based on ChadAMiller/hungergames.

from random import randrange, shuffle, seed, getstate, setstate, random

def without(array, index):
  return array[:index] + array[index+1:]

class BasePlayer():
  def __str__(self):
    try:
      return self.name
    except AttributeError:
      return super(BasePlayer, self).__repr__() # Fall back on Python default

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    raise NotImplementedError("You must define a strategy!")
    
  def hunt_outcomes(self, food_earnings):
    pass
    
  def round_end(self, award, m, number_hunters):
    pass


class Random():
  def __init__(self, s):
    seed(s)
    random()
    self.state = getstate()

  def randrange(self, a, b):
    setstate(self.state)
    res = randrange(a, b)
    self.state = getstate()
    return res

  def shuffle(self, a):
    setstate(self.state)
    res = shuffle(a)
    self.state = getstate()
    return res

  def random(self):
    setstate(self.state)
    res = random()
    self.state = getstate()
    return res

class GamePlayer(): # Autonomously keeps track of food, hunts, and slacks.
    def __init__(self, player, food, hunts=0, slacks=0):
        self.player = player
        self.food = food
        self.hunts = hunts
        self.slacks = slacks

    def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
      res = self.player.hunt_choices(round_number, current_food, current_reputation, m, player_reputations)
      self.hunts += res.count('h')
      self.slacks += res.count('s')
      return res

    def hunt_outcomes(self, food_earnings):
      self.food += sum(food_earnings)
      self.player.hunt_outcomes(food_earnings)

    def round_end(self, award, m, number_hunters):
      self.food += award
      self.player.round_end(award, m, number_hunters)

    @property
    def rep(self):
      return self.hunts/(self.hunts + self.slacks) if self.hunts > 0 else 0

    @property
    def alive(self):
      return self.food > 0

    @property
    def name(self):
      return self.player.name

    def __repr__(self):
        return '{} {} {:.3f}'.format(self.player, self.food, self.rep)

    def __str__(self):
        return "Player {} now has {} food and a reputation of {:.3f}".format(self.player, self.food, self.rep)

class Game():
  def payout(self, a, b):
    return {
      'hh': (0, 0),
      'hs': (-3, 1),
      'ss': (-2, -2),
      'sh': (1, -3),
    }[a + b]

  def __init__(self, players):
    start_food = 300 * (len(players) - 1)
    self.players = [GamePlayer(p, start_food) for p in players]
    self.unshuffled = [p for p in self.players]
    self.round = 0
    self.history = {
      'strategies': [],
      'payouts': [],
      'm': [],
      'food': [[p.food for p in self.players], ], # Put the initial state of players in our history.
      'hunts': [[p.hunts for p in self.players], ],
      'slacks': [[p.slacks for p in self.players], ],
    }

  def active_players(self):
    return [p for p in self.players if p.alive]

  def step(self, max_num = 1):
    for i in range(max_num):
      self._step() # Will not step if the game is over.

  def _step(self):
    # Get the active players, and end if there are too few.
    players = self.active_players()
    shuffle(players)
    P = len(players)
    if P <= 1:
      return
    # Setup variables.
    self.round += 1
    m = randrange(1, P * (P - 1))
    reps = [p.rep for p in players]
    # Get strategies.
    strategies = []
    for i, p in enumerate(players):
      strategy = p.hunt_choices(self.round, p.food, p.rep, m, without(reps, i))
      strategy.insert(i, 'x')
      strategies.append(strategy)
    # Perform the hunts and find the resultant payouts.
    payouts = [[0 for __ in range(P)] for _ in range(P)]
    for i in range(P):
      for j in range(i+1, P):
        payouts[i][j], payouts[j][i] = self.payout(strategies[i][j], strategies[j][i])
    # Calculate the bonus.
    number_hunts = sum(s.count('h') for s in strategies)
    if number_hunts > m:
      bonus = 2 * (P - 1)
    else:
      bonus = 0
    # Let players run cleanup tasks.
    for i, p in enumerate(players):
      p.hunt_outcomes(without(payouts[i], i))
      p.round_end(bonus, m, number_hunts)
    # Record the history.
    self.record(players, strategies, payouts, m)

  def record(self, players, strategies, payouts, m):
    N = len(self.unshuffled)
    # Find the right order of business; we want our history to be represented with the original order of players.
    order = [None for _ in range(N)]
    for i, original in enumerate(self.unshuffled):
      for u, p in enumerate(players):
        if p == original:
          order[i] = u
          break
    # Fill in a temporary strategies and payout matrices, and append them to history.
    tmps = [['x' for __ in range(N)] for _ in range(N)]
    tmpp = [[ 0  for __ in range(N)] for _ in range(N)]
    for i in range(N):
      if order[i] == None: # This original player is dead.
        continue
      for u in range(N):
        if order[u] == None:
          continue
        tmps[i][u] = strategies[order[i]][order[u]]
        tmpp[i][u] = payouts[order[i]][order[u]]
    self.history['strategies'].append(tmps)
    self.history['payouts'].append(tmpp)
    # Record the value of m, and the states of players.
    self.history['m'].append(m)
    self.history['food'].append([p.food for p in self.unshuffled])
    self.history['hunts'].append([p.hunts for p in self.unshuffled])
    self.history['slacks'].append([p.slacks for p in self.unshuffled])
