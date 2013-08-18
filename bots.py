# Based on ChadAMiller/hungergames.

from lib import BasePlayer, Rand

class Pushover(BasePlayer):

  def __init__(self):
    self.name = "Pushover" # Always hunts.

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    return ['h'] * len(player_reputations)

    
class Freeloader(BasePlayer):

  def __init__(self):
    self.name = "Freeloader" # Always slack. 

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    return ['s']*len(player_reputations)
    

class Alternator(BasePlayer):

  def __init__(self):
    self.name = "Alternator"
    self.last_played = 's'

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    hunt_decisions = []
    for i in range(len(player_reputations)):
      self.last_played = 'h' if self.last_played == 's' else 's'
      hunt_decisions.append(self.last_played)
    return hunt_decisions


class MaxRepHunter(BasePlayer):

  def __init__(self):
    self.name = "MaxRepHunter" # Hunt only with people with max reputation.

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    threshold = max(player_reputations)
    return ['h' if rep == threshold else 's' for rep in player_reputations]

class DecayMaxRepHunter(BasePlayer):

  seed = 123

  def __init__(self):
    self.rand = Rand(DecayMaxRepHunter.seed)
    DecayMaxRepHunter.seed += 1
    self.name = "DecayMaxRepHunter" # Hunt only with people with max reputation.

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    threshold = max(player_reputations)
    # return ['h' if rep == threshold and (self.rand.random() < 1.0/round_number) else 's' for rep in player_reputations]
    return ['h' if rep == threshold and (len(player_reputations) > 4) else 's' for rep in player_reputations]


class RandomHunter(BasePlayer):

  seed = 144 # Base seed.

  def __init__(self, p_hunt):
    self.rand = Rand(RandomHunter.seed)
    RandomHunter.seed += 1
    assert p_hunt >= 0.00 and p_hunt <= 1.00, "p_hunt must be at least 0 and at most 1"
    self.name = "RandomHunter(" + str(p_hunt) + ")"
    self.p_hunt = p_hunt

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    return ['h' if self.rand.random() < self.p_hunt else 's' for p in player_reputations]


class FairHunter(BasePlayer):

  seed = 155 # Base seed.

  def __init__(self):
    self.rand = Rand(FairHunter.seed)
    FairHunter.seed += 1
    self.name = "FairHunter" # Hunt with same probability as each opponent.

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    return ['h' if self.rand.random() < rep else 's' for rep in player_reputations]


class BoundedHunter(BasePlayer):

  def __init__(self,lower,upper):
    self.name = "BoundedHunter(" + str(lower) + '-' + str(upper) + ")" # Hunt whenever the other's reputation is within some range.
    self.low = lower
    self.up = upper

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    return ['h' if self.low <= rep <= self.up else 's' for rep in player_reputations]


class AverageHunter(BasePlayer):

  seed = 166 # Base seed.

  def __init__(self):
    self.rand = Rand(AverageHunter.seed)
    AverageHunter.seed += 1
    self.name = "AverageHunter" # Maintain the average reputation, but spreads its hunts randomly.

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    avg_rep = sum(player_reputations) / float(len(player_reputations))
    return ['h' if self.rand.random() < avg_rep else 's' for rep in player_reputations]


class Grouper(BasePlayer):

  def __init__(self):
    self.name = "Grouper" # Groups with people who don't always slack.

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    if round_number == 1:
      return ['h'] * len(player_reputations)
    else:
      return ['h' if rep > 0 else 's' for rep in player_reputations]


class Confuser(BasePlayer):

  def __init__(self):
    self.name = "Confuser" # Tries to confuse the others by keep changing his reputation.
    self.decision = 'h'

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    if current_reputation > 0.75:
      self.decision = 's'
    if current_reputation < 0.25:
      self.decision = 'h'
    return [self.decision for rep in player_reputations]

class GlobalWatcher(BasePlayer):

  seed = 166 

  def __init__(self, constant):
    self.rand = Rand(FairHunter.seed)
    FairHunter.seed += 1
    self.name = "GlobalWatcher(" + str(constant) + ")"
    self.constant = constant

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    threshold = max(player_reputations)
    avg = float(sum(player_reputations)) / len(player_reputations)
    return ['h' if (rep > 2.0 * avg or (rep==threshold and 
                                        self.rand.random() < 1.0/round_number)
                   ) else 's' for rep in player_reputations]

class Poisson(BasePlayer):

  seed = 555

  def __init__(self, lambd = 0.05):
    self.rand = Rand(Poisson.seed)
    Poisson.seed += 1
    self.name = "Poisson"
    self.goal = 0.5
    self.dgoal = (0.5 - self.rand.random()) / 10
    self.next = 1 + int(self.rand.expovariate(lambd))

  def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
    if round_number == self.next:
      self.dgoal = (0.5 - self.rand.random()) / 10
    self.goal += self.dgoal
    self.goal = 0 if self.goal < 0 else self.goal
    self.goal = 1 if self.goal > 1 else self.goal
    return ['h' if self.rand.random() < self.goal else 's' for p in player_reputations]

