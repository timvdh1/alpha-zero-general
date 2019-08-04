import Arena
from MCTS import MCTS
from wondevwoman.WonDevGame import WonDevGame, display
from wondevwoman.WonDevPlayers import *
from wondevwoman.pytorch.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = WonDevGame(6)

# all players
rp = RandomPlayer(g).play
gp = GreedyWonDevPlayer(g).play
hp = HumanWonDevPlayer(g).play

#nnet players
n1 = NNet(g)
n1.load_checkpoint('./temp/','temp.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))


#n2 = NNet(g)
#n2.load_checkpoint('/dev/8x50x25/','best.pth.tar')
#args2 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
#mcts2 = MCTS(g, n2, args2)
#n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

arena = Arena.Arena(n1p, n1p, g, display=display)
print(arena.playGames(2, verbose=True))
