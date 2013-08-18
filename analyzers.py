import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot
matplotlib.pyplot.ion()
from pylab import *
from itertools import product

class BaseAnalyzer():

  def __init__(self, game):
    self.game = game

  def dataset(self): # Dataset, to be overriden by the subclasses.
    pass

  def fname(self): # Default filename, to be overridden by the subclasses.
    pass

  def loc(self): # Location of legend, optionally to be overriden by the subclasses.
    return 'lower right'

  def plot(self, meta = True, loc = None):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    dashes = ['', '--', ':']
    combinations = [x for x in product(dashes, colors)]
    self.figure = figure()
    lines = plot(self.dataset())
    for i, line in enumerate(lines):
      dash, color = combinations[i]
      line.set_color(color)
      if dash:
        line.set_ls(dash)
    if meta:
      legend([p.name for p in self.game.unshuffled], loc=loc if loc else self.loc())

  def save(self, fname = None):
    if fname == None:
      fname = self.fname()
    figure(self.figure.number)
    savefig(fname)


class FoodAnalyzer(BaseAnalyzer):

  def dataset(self):
    return self.game.history['food']

  def fname(self):
    return "food.png"

  def loc(self):
    if max(self.game.history['food'][-1]) > max(self.game.history['food'][0]):
      return 'upper left'
    else:
      return 'lower left'


class RepAnalyzer(BaseAnalyzer):

  def dataset(self):
    res = []
    for i in range(1, len(self.game.history['payouts']) + 1):
      res.append([self.rep(h, s) for (h, s) in zip(self.game.history['hunts'][i], self.game.history['slacks'][i])])
    return res

  def fname(self):
    return "rep.png"

  def rep(self, h, s):
    return float(h)/(h+s) if h > 0 else 0
