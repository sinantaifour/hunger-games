# Run the following in an interactive session.

from lib import *
from bots import *
from analyzers import *

# ps = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), FairHunter(), AverageHunter(), RandomHunter(0.2), RandomHunter(0.8)]
ps = [Freeloader(), Freeloader(), Freeloader(), Freeloader(), Grouper(), Grouper(), Grouper(), Grouper(), Grouper()]
g = Game(ps)
a = FoodAnalyzer(g)

g.step(100)
a.plot(True)
