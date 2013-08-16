# Run the following in an interactive session.

from lib import *
from bots import *
from analyzers import *

ps = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), FairHunter(), AverageHunter(), RandomHunter(0.2), RandomHunter(0.8), Grouper(), Grouper(), Confuser()]
g = Game(ps)
fa = FoodAnalyzer(g)
ra = RepAnalyzer(g)

g.step(100)

fa.plot(True)
ra.plot(True)
