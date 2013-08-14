# Based on ChadAMiller/hungergames.

from random import randrange, shuffle

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

  def step(self):
    # Setup.
    self.round += 1
    P = len(self.players)
    m = randrange(1, P * (P - 1))
    shuffle(self.players)
    reps = [p.rep for p in self.players]
    # Get strategies.
    strategies = []
    for i, p in enumerate(self.players):
      strategy = p.hunt_choices(self.round, p.food, p.rep, m, without(reps, i))
      strategy.insert(i, 'x')
      strategies.append(strategy)
    # Perform the hunts.
    payouts = [[0 for __ in range(P)] for _ in range(P)]
    for i in range(P):
      for j in range(i+1, P):
        print i, j, strategies[i][j], strategies[j][i]
        print self.payout(strategies[i][j], strategies[j][i])
        payouts[i][j], payouts[j][i] = self.payout(strategies[i][j], strategies[j][i])
    # Calculate the bonus.
    number_hunts = sum(s.count('h') for s in strategies)
    if number_hunts > m:
      bonus = 2 * (P - 1)
      print "Cooperation!"
    else:
      bonus = 0
    # Let players run cleanup tasks.
    for i, p in enumerate(self.players):
      p.hunt_outcomes(without(payouts[i], i))
      p.round_end(bonus, m, number_hunts)

