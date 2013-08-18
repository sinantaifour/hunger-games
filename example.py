# Run the following in an interactive session.

from lib import *
from bots import *
from analyzers import *
from samm import Player as Samm

ps = [Pushover(), Freeloader(), Alternator(), MaxRepHunter(), FairHunter(), AverageHunter(), RandomHunter(0.2), RandomHunter(0.8), Confuser(), Samm(), GlobalWatcher(3), GlobalWatcher(2), Grouper(), Grouper(), Samm()]
# ps = [Alternator(), MaxRepHunter(), FairHunter(), AverageHunter(), RandomHunter(0.2), RandomHunter(0.8), Confuser(), Grouper(), GlobalWatcher(2), BoundedHunter(0.5, 1.0), BoundedHunter(0.75, 1.0), DecayMaxRepHunter(), Poisson(), Poisson(), Samm()]
# ps = [Freeloader(), Samm(), Confuser(), Grouper()]
# ps = [Freeloader(), Alternator(), MaxRepHunter(), FairHunter(), AverageHunter(), RandomHunter(0.2), RandomHunter(0.8), Grouper(), Confuser(), Samm(), Poisson(), Poisson(), GlobalWatcher(2)]
# ps = [Confuser(), Samm()]
g = Game(ps)
fa = FoodAnalyzer(g)
ra = RepAnalyzer(g)

g.step(5000)

fa.plot(True, 'upper right')
ra.plot(False)
fa.save()
ra.save()
