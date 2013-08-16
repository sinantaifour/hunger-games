import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot
matplotlib.pyplot.ion()
from pylab import *

class BaseAnalyzer():
  def __init__(self, game):
    self.game = game
  def dataset(self):
    pass
  def plot(self, meta = False):
    figure()
    plot(self.dataset())
    if meta:
      legend([p.name for p in self.game.unshuffled])
    else:
      legend(['' for p in self.game.unshuffled])

class FoodAnalyzer(BaseAnalyzer):
  def dataset(self):
    return self.game.history['food']

class RepAnalyzer(BaseAnalyzer):
  def dataset(self):
    res = []
    for i in range(1, len(self.game.history['payouts']) + 1):
      res.append([self.rep(h, s) for (h, s) in zip(self.game.history['hunts'][i], self.game.history['slacks'][i])])
    return res
  def rep(self, h, s):
    return float(h)/(h+s) if h > 0 else 0
