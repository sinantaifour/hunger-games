# Run the following in an interactive session.

from lib import *
from bots import *
from analyzers import *

ps = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), Random(0.2), Random(0.8), FairHunter(), AverageHunter()]
g = Game(ps)
a = FoodAnalyzer(g)

g.step(100)
a.plot()
